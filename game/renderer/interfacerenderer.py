import numpy as np
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap as textwrap
import moderngl
from moderngl_window import geometry


class InterfaceRenderer:
    def __init__(self, game, ctx):
        self.game = game
        self.ctx = ctx

        self.width = self.game.resolution_interface_width
        self.height = int(self.width / 16 * 9)
        self.scale = self.width // 640

        self.rerender = True

        self.font = self.game.m_res.get_font("Lexend-Regular", self.scale)
        self.font_bold = self.game.m_res.get_font("Lexend-SemiBold", self.scale)

        self.new_canvas()

        self.prog = self.game.m_res.get_program("interfacelayer")
        self.quad_fs = geometry.quad_fs()

        texture_bytes = self.canvas.tobytes()
        self.texture = self.ctx.texture(self.canvas.size, 4, texture_bytes)
        self.texture.filter = moderngl.NEAREST, moderngl.NEAREST
        self.texture.write(texture_bytes)

    def update(self, force=False):
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
        self.canvas = Image.new("RGBA", (self.width, self.height), "#00000000")
        self.draw = ImageDraw.Draw(self.canvas)

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
            pos, msg, font=font, fill="black", align=align,
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
