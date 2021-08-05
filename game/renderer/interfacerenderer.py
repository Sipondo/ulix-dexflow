import numpy as np
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap as textwrap
import moderngl
from moderngl_window import geometry

LETTERBOX_TO = 0.121


class InterfaceRenderer:
    def __init__(self, game, ctx):
        self.game = game
        self.ctx = ctx

        self.width = self.game.resolution_interface_width
        self.height = int(self.width / 16 * 9)
        self.scale = self.width // 640

        self.letterbox_amount = 0.0
        self.fade_amount = 1

        self.letterbox = False
        self.fade = True

        self.rerender = True
        self.need_to_redraw = False

        self.font = self.game.m_res.get_font("Lexend-Regular", self.scale)
        self.font_bold = self.game.m_res.get_font("Lexend-SemiBold", self.scale)

        self.new_canvas()

        self.prog = self.game.m_res.get_program("interfacelayer")
        self.quad_fs = geometry.quad_fs()

        texture_bytes = self.canvas.tobytes()
        self.texture = self.ctx.texture(self.canvas.size, 4, texture_bytes)
        # self.texture.filter = moderngl.NEAREST, moderngl.NEAREST
        self.texture.write(texture_bytes)

    def on_tick(self, time, frame_time):
        frame_time = max(0.01, min(0.03, frame_time))
        if self.letterbox:
            if self.letterbox_amount < LETTERBOX_TO:
                self.letterbox_amount = min(
                    self.letterbox_amount + frame_time * 0.25, LETTERBOX_TO
                )
                self.game.m_gst.current_state.need_to_redraw = True
        else:
            if self.letterbox_amount > 0:
                self.letterbox_amount = max(
                    self.letterbox_amount - frame_time * 0.25, 0
                )
                self.game.m_gst.current_state.need_to_redraw = True

        if self.fade:
            if self.fade_amount < 1:
                self.fade_amount = min(self.fade_amount + frame_time * 3, 1)
                self.game.m_gst.current_state.need_to_redraw = True
        else:
            if self.fade_amount > 0:
                self.fade_amount = max(self.fade_amount - frame_time * 3, 0)
                self.game.m_gst.current_state.need_to_redraw = True

        # if self.need_to_redraw:
        #     self.need_to_redraw = False
        #     self.new_canvas()

    def update(self):
        if self.rerender:
            self.rerender = False
            self.texture.write(np.array(self.canvas).tobytes())

        self.prog["interface_layer"] = 0
        self.texture.use(location=0)
        self.ctx.enable(moderngl.BLEND)
        self.quad_fs.render(self.prog)
        self.ctx.disable(moderngl.BLEND)

    def new_canvas(self):
        self.rerender = True

        if self.fade_amount == 0:
            self.canvas = Image.new("RGBA", (self.width, self.height), "#00000000")
        else:
            self.canvas = Image.new(
                "RGBA",
                (self.width, self.height),
                "#000000" + (str(hex(int(self.fade_amount * 255)))[2:]).zfill(2),
            )
        self.draw = ImageDraw.Draw(self.canvas, "RGBA")
        self.draw_interface()

    def draw_rectangle(self, pos, to=None, size=None, col="white", centre=False):
        self.rerender = True
        pos = self.to_screen_coords(pos)

        if size:
            size = self.to_screen_coords(size)
            if centre:
                pos = (pos[0] - size[0] // 2, pos[1] - size[1] // 2)
            to = (pos[0] + size[0], pos[1] + size[1])
        else:
            to = self.to_screen_coords(to)

        self.draw.rectangle((pos, to), fill=col, outline=None, width=0)

    def draw_text(
        self,
        text,
        pos,
        to=None,
        size=None,
        bcol="white",
        centre=False,
        bold=True,
        align="left",
        fsize=12,
        col="black",
    ):
        self.rerender = True
        if bcol:
            self.draw_rectangle(pos, to=to, size=size, col=bcol, centre=centre)

        pos = (pos[0] + 0.004, pos[1])
        pos = self.to_screen_coords(pos)

        if size:
            size = (size[0] - 0.008, size[1])
            size = self.to_screen_coords(size)
            if centre:
                pos = (pos[0] - size[0] // 2, pos[1] - size[1] // 2)
            to = (pos[0] + size[0], pos[1] + size[1])
        else:
            to = self.to_screen_coords(to)

        font = self.font_bold[fsize] if bold else self.font[fsize]
        msg = "\n".join(textwrap(text, size[0] // fsize)) if size else text

        w, _ = self.draw.textsize(msg, font=font)

        if align == "centre":
            pos = (pos[0] + (to[0] - pos[0] - w) // 2, pos[1])
        elif align == "right":
            pos = (to[0] - w, pos[1])

        self.draw.multiline_text(
            pos, msg, font=font, fill=col, align=align,
        )

    def draw_image(self, img, pos, centre=False, size=1.0):
        self.rerender = True
        if size != 1.0:
            img = img.resize(
                (int(img.size[0] * size), int(img.size[1] * size)),
                resample=Image.NEAREST,
            )
        pos = self.to_screen_coords(pos)

        if centre:
            pos = (pos[0] - img.size[0] // 2, pos[1] - img.size[1] // 2)

        self.canvas.alpha_composite(img, pos)
        # self.canvas.paste(img, pos, img)

    def to_screen_coords(self, tup):
        return (int(tup[0] * self.width), int(tup[1] * self.height))

    def draw_interface(self):
        self.draw_rectangle((0, 0), to=(1, self.letterbox_amount), col="black")
        self.draw_rectangle((0, 1 - self.letterbox_amount), to=(1, 1), col="black")

