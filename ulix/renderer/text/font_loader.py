# Ported from qlibs by IntQuant (https://github.com/IntQuant/qlibs, qlibs/fonts/font_loader.py).

import warnings
from collections import defaultdict
from contextvars import ContextVar
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .kerning import KerningTable

FONT_DIR = Path(__file__).resolve().parents[3] / 'resources' / 'base' / 'font'
if not FONT_DIR.is_dir():
    FONT_DIR = Path('resources/base/font')
# Registered under these names; 'default' is DEFAULT_FONT. Lexend is SIL OFL (Lexend-OFL.txt);
# Silkscreen may only be redistributed unmodified (silkscreen-license.txt).
BUNDLED_FONTS = {
    'lexend-light': 'lexend-light.ttf',
    'lexend': 'lexend-regular.ttf',
    'lexend-medium': 'lexend-medium.ttf',
    'lexend-semibold': 'lexend-semibold.ttf',
    'lexend-bold': 'lexend-bold.ttf',
    'silkscreen': 'slkscr.ttf',
    'silkscreen-bold': 'slkscrb.ttf',
    'silkscreen-expanded': 'slkscre.ttf',
    'silkscreen-expanded-bold': 'slkscreb.ttf',
}
DEFAULT_FONT = 'lexend'
FALLBACK_CHARS = ('�', '?')


class Glyph:
    """A rasterized glyph at one pixel size; replaces FreeType's GlyphSlot.

    `advance` is in pixels (FreeType's was 26.6 fixed point). `bearing` is (left, top) relative to
    the pen position on the baseline. `bitmap` is 8-bit coverage with rows of `pitch` bytes, padded
    to a multiple of 4 because GL's default unpack alignment is 4.
    """

    __slots__ = ('advance', 'size', 'bearing', 'bitmap', 'pitch')

    def __init__(self, advance, size, bearing, bitmap, pitch):
        self.advance = advance
        self.size = size
        self.bearing = bearing
        self.bitmap = bitmap
        self.pitch = pitch


class GlyphProvider:
    def __init__(self):
        pass

    def get(self, char, size=48):
        raise NotImplementedError()

    def get_font_kerning(self, left_char, right_char, size=48):
        return None

    @property
    def priority(self):
        return 0


class PillowGlyphProvider(GlyphProvider):
    def __init__(self, file, priority=0):
        self._data = file if isinstance(file, bytes) else Path(file).read_bytes()
        self._priority = priority
        self._fonts = {}
        self._kerning = None

    @property
    def kerning(self):
        # Parsed on first use: a FontLoader is created at import time.
        if self._kerning is None:
            self._kerning = KerningTable(self._data)
        return self._kerning

    def _font(self, size):
        font = self._fonts.get(size)
        if font is None:
            font = ImageFont.truetype(BytesIO(self._data), size, layout_engine=ImageFont.Layout.BASIC)
            self._fonts[size] = font
        return font

    def get(self, char, size=48):
        # Returning None lets FontLoader fall through to lower-priority providers.
        if not self.kerning.has_char(char):
            return None
        font = self._font(size)
        x0, y0, x1, y1 = font.getbbox(char, anchor='ls')
        width, height = max(0, x1 - x0), max(0, y1 - y0)
        pitch = (width + 3) & ~3
        if width and height:
            image = Image.new('L', (pitch, height))
            ImageDraw.Draw(image).text((-x0, -y0), char, font=font, fill=255, anchor='ls')
            bitmap = image.tobytes()
        else:
            bitmap = b''
        return Glyph(font.getlength(char), (width, height), (x0, -y0), bitmap, pitch)

    def get_font_kerning(self, left_char, right_char, size=48):
        if not (self.kerning.has_char(left_char) and self.kerning.has_char(right_char)):
            return None
        units = self.kerning.get(left_char, right_char)
        return units * size / self.kerning.units_per_em

    @property
    def priority(self):
        return self._priority


class FontLoader:
    def __init__(self):
        self._mapping = defaultdict(list)
        for name, file in BUNDLED_FONTS.items():
            path = FONT_DIR / file
            if not path.exists():
                warnings.warn(RuntimeWarning(f'Bundled font missing: {path}'))
                continue
            self.load_font(name, path, priority=-1)
            if name == DEFAULT_FONT:
                self.load_font('default', path, priority=-1)

    def load_font(self, font_name, path, override=False, priority=0):
        """`path` may be a file path or the font file's bytes (e.g. from an asset loader)."""
        if override:
            self._mapping[font_name].clear()
        self._mapping[font_name].append(PillowGlyphProvider(path, priority=priority))
        self._mapping[font_name].sort(reverse=True, key=lambda x: x.priority)

    def get(self, font_name, char, pixel_size=48):
        for candidate in (char, *FALLBACK_CHARS):
            for provider in self._mapping[font_name]:
                v = provider.get(candidate, size=pixel_size)
                if v is not None:
                    return v
        raise RuntimeError(f"Character '{char}' in font '{font_name}' not found")

    def get_kerning(self, font_name, left_char, right_char, pixel_size=48):
        for provider in self._mapping[font_name]:
            v = provider.get_font_kerning(left_char, right_char, size=pixel_size)
            if v is not None:
                return v
        return 0.0


font_loader: ContextVar[FontLoader] = ContextVar('font_loader', default=FontLoader())
