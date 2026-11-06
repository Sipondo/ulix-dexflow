# Ported from qlibs by IntQuant (https://github.com/IntQuant/qlibs, qlibs/fonts/font_render.py).

import itertools
from array import array
from enum import Enum, auto
from functools import lru_cache
from html.parser import HTMLParser

from .font_loader import font_loader

SCALE_SAFETY_MARGIN = 8

# Per glyph instance: position, size, uv0, uv1, color.
INSTANCE_LAYOUT = '2f 2f 2f 2f 3f /i'
INSTANCE_FLOATS = 11

VERTEX_SHADER = '''
    #include "platform"

    layout (location = 0) in vec2 in_pos;
    layout (location = 1) in vec2 in_size;
    layout (location = 2) in vec2 in_uv0;
    layout (location = 3) in vec2 in_uv1;
    layout (location = 4) in vec3 in_color;

    uniform vec2 target_size;
    uniform float flip_y;

    out vec2 v_uv;
    out vec3 v_color;

    void main() {
        vec2 corner = vec2(float(gl_VertexID & 1), float(gl_VertexID >> 1));
        vec2 ndc = (in_pos + corner * in_size) / target_size * 2.0 - 1.0;
        if (flip_y > 0.5) {
            ndc.y = -ndc.y;
        }
        gl_Position = vec4(ndc, 0.0, 1.0);
        v_uv = mix(in_uv0, in_uv1, corner);
        v_color = in_color;
    }
'''

FRAGMENT_SHADER = '''
    #include "platform"

    uniform sampler2D atlas;

    in vec2 v_uv;
    in vec3 v_color;

    layout (location = 0) out vec4 out_color;

    void main() {
        out_color = vec4(v_color, texture(atlas, v_uv).r);
    }
'''


class TextAlign(Enum):
    LEFT = auto()
    CENTER = auto()

class FormattedTextToken(Enum):
    LINEBREAK = auto()
    POP_FORMAT = auto()


class FormattingData(dict):
    def __getattr__(self, name):
        return self.get(name, None)

    def copy(self):
        return FormattingData(**self)


class HTMLFormatParser(HTMLParser):
    CDATA_CONTENT_ELEMENTS = ("raw",)
    def __init__(self, color_converter):
        super().__init__()
        self.result = []
        self._color_converter = color_converter
        self._is_raw = False

    def handle_starttag(self, tag, attrs):
        attrs = {k: v for (k, v) in attrs}
        if tag == "br":
            self.result.append(FormattedTextToken.LINEBREAK)
        elif tag == "style":
            fmt = FormattingData()
            if "color" in attrs:
                color_str = attrs["color"]
                if color_str.startswith("#"):
                    color_val = int(color_str[1:], base=16)
                    r = (color_val & 0xFF0000) / 0xFF0000
                    g = (color_val & 0x00FF00) / 0x00FF00
                    b = (color_val & 0x0000FF) / 0x0000FF
                    fmt["color"] = (r, g, b)
                else:
                    if self._color_converter is not None:
                        fmt["color"] = self._color_converter(color_str)
                    else:
                        raise ValueError(f"Unknown color '{color_str}'")
            if "font" in attrs:
                fmt["font"] = attrs["font"]
            #Note: value only matters at line breaks or when there are no tokens anymore
            #You might want to consider adding addional linebreaks before the text align is switched
            if "align" in attrs:
                fmt["align"] = {
                    "left": TextAlign.LEFT,
                    "center": TextAlign.CENTER,
                }[attrs["align"]]
            self.result.append(fmt)
        elif tag == "raw":
            self._is_raw = True

    def handle_data(self, data):
        if self._is_raw:
            self.result.append(data)
        else:
            self.result.extend(data.split())

    def handle_endtag(self, tag):
        if tag == "style":
            self.result.append(FormattedTextToken.POP_FORMAT)
        elif tag == "raw":
            self._is_raw = False



class FormattedText:
    def __init__(self, text=None, tokens=None, **kwargs):
        self.tokens = tokens or list()
        if kwargs:
            self.tokens.insert(0, FormattingData(**kwargs))
        if text is not None:
            self.parse(text)

    def parse(self, text):
        for line in text.splitlines():
            self.tokens.extend(line.split())
            self.tokens.append(FormattedTextToken.LINEBREAK)

    @classmethod
    def from_html(cls, text, color_converter=None):
        parser = HTMLFormatParser(color_converter)
        parser.feed(text)
        return cls(tokens=parser.result)


class GGlyph:
    """
      Class for storing glyph data: *advance*, *size*, *bearing*, and its *uv* rectangle in the atlas
    """
    __slots__ = ("advance", "size", "bearing", "uv")
    def __init__(self, glyph, offset, atlas_side):
        self.advance = glyph.advance
        self.size = glyph.size
        self.bearing = glyph.bearing
        x, y = offset
        w, h = glyph.size
        self.uv = (x / atlas_side, y / atlas_side, (x + w) / atlas_side, (y + h) / atlas_side)


class _AtlasPage:
    """One R8 texture of glyphs at a single pixel size, filled shelf by shelf."""

    def __init__(self, ctx, pixel_size):
        self.side = min(2048, max(512, pixel_size * 16))
        self.image = ctx.image((self.side, self.side), 'r8unorm')
        self.glyphs = {}
        self.instances = array('f')
        self.capacity = 0
        self.buffer = None
        self.pipeline = None
        self.reset()

    def reset(self):
        self.glyphs.clear()
        self.x = self.y = self.row = 0

    def allocate(self, w, h):
        if not w or not h:
            return (0, 0)
        # One texel of gap so linear filtering never samples a neighbour.
        if self.x + w + 1 > self.side:
            self.x, self.y, self.row = 0, self.y + self.row + 1, 0
        if self.y + h > self.side:
            return None
        offset = (self.x, self.y)
        self.x += w + 1
        self.row = max(self.row, h)
        return offset


class DirectFontRender:
    """
      Render text using font

      Text is queued by render_string/render_multiline and drawn into *framebuffer* by draw().
      Coordinates are pixels of the framebuffer; with *flip_y* (the default) the origin is the
      top-left corner and *y* is the baseline, growing downwards.
    """
    def __init__(self, ctx, framebuffer, pixel_size=48, flip_y=True, default_font="default", adaptive_pixel_size=True, base_pixel_size=8):
        """
        *ctx* is a zengl context, *framebuffer* the list of images to draw into.
        *default_font* - name of default font.
        *adaptive_pixel_size* - whether to use different glyph sizes or not. True results in better quality.
        """
        self.ctx = ctx
        self.framebuffer = list(framebuffer)
        self.font = default_font
        self.base_pixel_size = base_pixel_size
        self.pixel_size = pixel_size
        self.adaptive_pixel_size = adaptive_pixel_size
        self.flip_y = flip_y
        self.pages = {}
        # Per instance rather than on the method, so a released renderer is not kept alive.
        self.calc_size = lru_cache(1024)(self._calc_size)
        self.calc_height = lru_cache(1024)(self._calc_height)

    def _pixel_size_for(self, scale):
        if not self.adaptive_pixel_size:
            return self.pixel_size
        #We always want to have a bit bigger texture for safety, so we add SCALE_SAFETY_MARGIN to scale
        larger_power_of_two = 2**max(8, int(scale+SCALE_SAFETY_MARGIN)).bit_length()
        return max(larger_power_of_two, self.base_pixel_size)

    def _page(self, pixel_size):
        page = self.pages.get(pixel_size)
        if page is None:
            page = self.pages[pixel_size] = _AtlasPage(self.ctx, pixel_size)
        return page

    def get_glyph(self, char, font_name=None, pixel_size=None):
        font_name = font_name or self.font
        pixel_size = pixel_size or self.pixel_size
        page = self._page(pixel_size)
        key = (font_name, char)
        glyph = page.glyphs.get(key)
        if glyph is None:
            raw = font_loader.get().get(font_name, char, pixel_size=pixel_size)
            offset = page.allocate(raw.pitch, raw.size[1])
            if offset is None:
                # Atlas full: draw what is queued while its glyphs are still there, then start over.
                self._flush(page)
                page.reset()
                offset = page.allocate(raw.pitch, raw.size[1])
                if offset is None:
                    raise ValueError(f"Glyph '{char}' at {pixel_size}px does not fit in the atlas")
            if raw.bitmap:
                page.image.write(raw.bitmap, size=(raw.pitch, raw.size[1]), offset=offset)
            glyph = page.glyphs[key] = GGlyph(raw, offset, page.side)
        return glyph

    def get_kerning(self, left_char, right_char, font_name=None, pixel_size=None):
        font_name = font_name or self.font
        pixel_size = pixel_size or self.pixel_size
        return font_loader.get().get_kerning(font_name, left_char, right_char, pixel_size=pixel_size)

    def render_string(self, text, x, y, scale=1, color=(1, 1, 1), font=None, kerning_enabled=True, **kwargs):
        """
        Queue text with given parameters; *scale* is the font size in pixels
        """
        pixel_size = self._pixel_size_for(scale)

        if len(color) != 3:
            raise ValueError("Invalid color - len 3 required")

        scale /= pixel_size
        page = self._page(pixel_size)

        pos_x = x
        for char, next_char in itertools.zip_longest(text, text[1:]):
            glyph = self.get_glyph(char, font_name=font, pixel_size=pixel_size)
            h = glyph.size[1] * scale
            w = glyph.size[0] * scale
            u0, v0, u1, v1 = glyph.uv

            if self.flip_y:
                posy = y - glyph.bearing[1]*scale
                uv = (u0, v0, u1, v1)
            else:
                posy = y - (glyph.size[1] - glyph.bearing[1]) * scale
                uv = (u0, v1, u1, v0)

            x_shift = glyph.bearing[0] * scale

            if w and h:
                page.instances.extend((pos_x + x_shift, posy, w, h, *uv, *color))
            if kerning_enabled and next_char is not None:
                kerning = self.get_kerning(char, next_char, font_name=font, pixel_size=pixel_size)
            else:
                kerning = 0
            pos_x += (glyph.advance + kerning) * scale

    def render_multiline(self, text, x, y, max_line_len, *, scale=32, vertical_advance=None, min_sep=15, **kwargs):
        if not isinstance(text, FormattedText):
            ftext = FormattedText()
            ftext.parse(text)
        else:
            ftext = text

        min_sep *= scale/32
        fmt_params = dict(align=TextAlign.LEFT)
        fmt_params.update(kwargs)
        formatting_data = FormattingData(**fmt_params)
        words = list(ftext.tokens)

        line = list()
        cur_line_len = 0
        words.reverse()
        cy = y
        format_stack = list()
        if vertical_advance is None:
            vertical_advance = scale * (1 if self.flip_y else -1)
        while words:
            is_word = isinstance(words[-1], str)
            if is_word:
                word_len = self.calc_size(words[-1], scale=scale, font=formatting_data.font)
            else:
                word_len = 0
            finish_line = word_len + cur_line_len > max_line_len
            if is_word and (word_len + cur_line_len <= max_line_len or cur_line_len == 0):
                cur_line_len += word_len + min_sep
                line.append((words.pop(), formatting_data))
            if not is_word:
                token = words.pop()
                if token is FormattedTextToken.LINEBREAK:
                    finish_line = True
                if token is FormattedTextToken.POP_FORMAT:
                    formatting_data = format_stack.pop()
                if isinstance(token, FormattingData):
                    format_stack.append(formatting_data)
                    formatting_data = formatting_data.copy()
                    formatting_data.update(token)

            if finish_line or not words:
                if formatting_data.align is TextAlign.CENTER:
                    cx = x + (max_line_len - cur_line_len + min_sep) // 2
                else:
                    cx = x
                for word, formatting in line:
                    self.render_string(word, cx, cy, scale=scale, **formatting)
                    cx += self.calc_size(word, scale=scale, font=formatting.font) + min_sep
                line.clear()
                cur_line_len = 0
                cy += vertical_advance

    def _calc_size(self, text, scale=1, font=None, kerning_enabled=True):
        pixel_size = self._pixel_size_for(scale)
        x = 0
        for char, next_char in itertools.zip_longest(text, text[1:]):
            if kerning_enabled and next_char is not None:
                kerning = self.get_kerning(char, next_char, font_name=font, pixel_size=pixel_size)
            else:
                kerning = 0
            x += self.get_glyph(char, font_name=font, pixel_size=pixel_size).advance + kerning
        return x * scale / pixel_size

    def _calc_height(self, text, scale=1, full=False, font=None):
        pixel_size = self._pixel_size_for(scale)
        max_y = 0
        min_y = 0
        for char in text:
            glyph = self.get_glyph(char, font_name=font, pixel_size=pixel_size)
            max_y = max(max_y, glyph.bearing[1])
            if full:
                min_y = min(min_y, glyph.bearing[1] - glyph.size[1])
        return abs(max_y - min_y) * scale / pixel_size

    def draw(self):
        """Render everything queued since the last draw()."""
        for page in self.pages.values():
            self._flush(page)

    def _flush(self, page):
        count = len(page.instances) // INSTANCE_FLOATS
        if not count:
            return
        if count > page.capacity:
            self._grow(page, count)
        page.buffer.write(page.instances.tobytes())
        page.pipeline.instance_count = count
        page.pipeline.render()
        page.instances = array('f')

    def _grow(self, page, count):
        import zengl

        for obj in (page.pipeline, page.buffer):
            if obj is not None:
                self.ctx.release(obj)
        page.capacity = max(256, 1 << (count - 1).bit_length())
        page.buffer = self.ctx.buffer(size=page.capacity * INSTANCE_FLOATS * 4)
        page.pipeline = self.ctx.pipeline(
            vertex_shader=VERTEX_SHADER,
            fragment_shader=FRAGMENT_SHADER,
            layout=[{'name': 'atlas', 'binding': 0}],
            resources=[{
                'type': 'sampler',
                'binding': 0,
                'image': page.image,
                'min_filter': 'linear',
                'mag_filter': 'linear',
                'wrap_x': 'clamp_to_edge',
                'wrap_y': 'clamp_to_edge',
            }],
            uniforms={'target_size': self.framebuffer[0].size, 'flip_y': 1.0 if self.flip_y else 0.0},
            blend={
                'enable': True,
                'src_color': 'src_alpha',
                'dst_color': 'one_minus_src_alpha',
                'src_alpha': 'one',
                'dst_alpha': 'one_minus_src_alpha',
            },
            framebuffer=self.framebuffer,
            topology='triangle_strip',
            vertex_buffers=zengl.bind(page.buffer, INSTANCE_LAYOUT, 0, 1, 2, 3, 4),
            vertex_count=4,
        )

    def release(self):
        """Free the atlases and pipelines; call before dropping the renderer (e.g. on resize)."""
        for page in self.pages.values():
            for obj in (page.pipeline, page.buffer, page.image):
                if obj is not None:
                    self.ctx.release(obj)
        self.pages.clear()
        self.calc_size.cache_clear()
        self.calc_height.cache_clear()
