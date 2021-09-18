from qlibs.gui.window import Window
from qlibs.fonts.font_loader import FreetypeGlyphProvider, font_loader
from qlibs.fonts.font_render import DirectFontRender, FormattedText, FormattedTextToken
from qlibs.resources.resource_loader import ImageData
from qlibs.gui.basic_shapes import ShapeDrawer
from qlibs.highlevel.graphics import SpriteMaster
from qlibs.math import Matrix4


import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap as textwrap
import moderngl
from moderngl_window import geometry

LETTERBOX_TO = 0.121
# https://github.com/IntQuant/qlibs/blob/master/qlibs/highlevel/graphics.py


COLOR_DICT = {
    "black": (0, 0, 0),
    "white": (1, 1, 1),
    "grey": (0.7, 0.7, 0.7),
    "red": (1, 0, 0),
    "green": (0, 1, 0),
    "blue": (0, 0, 1),
    "yellow": (1, 1, 0),
}


class InterfaceRenderer:
    def __init__(self, game, ctx):
        self.game = game
        self.ctx = ctx

        self.font = self.game.m_res.get_font("lexend-semibold", 1)
        self.rend_text = DirectFontRender(ctx)
        font_loader.get().mapping["default"] = [FreetypeGlyphProvider(self.font)]
        self.shape = ShapeDrawer(ctx)
        self.sprite = SpriteMaster(ctx)
        self.spritesize = {}

        self.width = self.game.resolution_interface_width
        self.height = int(self.width / 16 * 9)
        self.scale = self.width // 640

        self.mvp = Matrix4.orthogonal_projection(0, self.width, 0, self.height)

        self.letterbox_amount = 0.0
        self.fade_amount = 1

        self.letterbox = False
        self.fade = True

    def on_tick(self, time, frame_time):
        frame_time = max(0.001, min(0.06, frame_time))
        if self.letterbox:
            if self.letterbox_amount < LETTERBOX_TO:
                self.letterbox_amount = min(
                    self.letterbox_amount + frame_time * 0.35, LETTERBOX_TO
                )
        else:
            if self.letterbox_amount > 0:
                self.letterbox_amount = max(
                    self.letterbox_amount - frame_time * 0.35, 0
                )

        if self.fade:
            if self.fade_amount < 1:
                self.fade_amount = min(self.fade_amount + frame_time * 3, 1)
        else:
            if self.fade_amount > 0:
                self.fade_amount = max(self.fade_amount - frame_time * 3, 0)

    def update(self):
        self.draw_interface()

    def draw_rectangle(self, pos, to=None, size=None, col="white", centre=False):
        pos = self.to_screen_coords(pos)

        if size:
            size = self.to_screen_coords(size, flip=False)
            if centre:
                pos = (pos[0] - size[0] // 2, pos[1] + size[1] // 2)
        else:
            to = self.to_screen_coords(to)
            size = (to[0] - pos[0], to[1] - pos[1])

        self.shape.add_rectangle(
            pos[0], pos[1], size[0], size[1], color=COLOR_DICT[col]
        )
        self.shape.render(self.mvp)

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
        if bcol:
            self.draw_rectangle(pos, to=to, size=size, col=bcol, centre=centre)

        pos = (pos[0] + 0.005, pos[1])
        pos = self.to_screen_coords(pos)

        pos = (pos[0], pos[1] - fsize * 2)

        if size:
            size = self.to_screen_coords(size, flip=False)
            if centre:
                pos = (pos[0] - size[0] // 2, pos[1] + size[1] // 2)
        else:
            to = self.to_screen_coords(to)
            size = (to[0] - pos[0], to[1] - pos[1])

        size = (size[0] - 0.01, size[1])

        # if align == "centre":
        #     pos = (pos[0] + (to[0] - pos[0] - w) // 2, pos[1])
        # elif align == "right":
        #     pos = (to[0] - w, pos[1])

        tokens = []

        for line in text.splitlines():
            tokens.extend(line.split())
            tokens.append(FormattedTextToken.LINEBREAK)

        formattext = FormattedText(
            tokens=tokens, color=COLOR_DICT[col]
        )  # FormattedText(tokens=[FormattingData(color=COLOR_DICT[col]), x] for x in text.split())
        self.rend_text.render_multiline(
            formattext,
            pos[0],
            pos[1],
            max_line_len=size[0],
            scale=fsize * 2,
            mvp=self.mvp,
        )

    def draw_image(self, img, pos, centre=False, size=1.0, safe=False):
        if not isinstance(img, str):
            raise Exception("DEPRECATED IMAGE CALL")

        img = img.lower()
        if safe:
            self.load_sprite(img, init=True)

        pos = self.to_screen_coords(pos)
        w, h = self.spritesize[img]

        w *= size
        h *= size

        if centre:
            pos = (pos[0] - w // 2, pos[1] + h // 2)

        self.sprite.add_sprite_rect(img, pos[0], pos[1] - h, w, h)
        self.ctx.enable(moderngl.BLEND)
        self.sprite.render(self.mvp)
        return

    def to_screen_coords(self, tup, flip=True):
        if flip:
            return (int(tup[0] * self.width), int((1 - tup[1]) * self.height))
        else:
            return (int(tup[0] * self.width), -int((tup[1]) * self.height))

    def draw_interface(self):
        self.draw_rectangle((0, 0), to=(1, self.letterbox_amount), col="black")
        self.draw_rectangle((0, 1 - self.letterbox_amount), to=(1, 1), col="black")

    def load_sprite(self, name, size=0.5, init=False):
        # TODO: Cl
        name = name.lower()
        if "icon/" in name:
            if name not in self.spritesize:
                imgs = self.game.m_res.get_interface(name[:-2], size)

                img = imgs[0]
                n = f"{name[:-2]}_0"

                img = img.transpose(Image.FLIP_TOP_BOTTOM)
                self.sprite.images[n] = ImageData(img.size, img.tobytes())
                self.spritesize[n] = img.size

                img = imgs[1]
                n = f"{name[:-2]}_1"

                img = img.transpose(Image.FLIP_TOP_BOTTOM)
                self.sprite.images[n] = ImageData(img.size, img.tobytes())
                self.spritesize[n] = img.size

                if init:
                    self.init_sprite_drawer()
            return

        if name not in self.spritesize:
            img = self.game.m_res.get_interface(name, size)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            self.sprite.images[name] = ImageData(img.size, img.tobytes())
            self.spritesize[name] = img.size

            if init:
                self.init_sprite_drawer()

    def init_sprite_drawer(self):
        self.sprite.init()
        for drawer in self.sprite.drawers:
            drawer.texture.filter = moderngl.NEAREST, moderngl.NEAREST
