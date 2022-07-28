from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Mesh, RenderContext, BindTexture, Rectangle
from kivy.graphics.context_instructions import Color
from kivy.graphics.texture import Texture
from kivy.core.image import Image
from kivy.resources import resource_find, resource_add_path
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    ReferenceListProperty,
    ListProperty,
)


import os
import numpy as np

from ulivy.renderer.tilerenderer import TileRenderer


from kivy.graphics import Fbo, Color, Rectangle

from kivy.lang import Builder
from kivy.graphics.gl_instructions import ClearColor, ClearBuffers

Builder.load_file("ulivy/renderer/bufferrenderer.kv")


class BufferRenderer(FloatLayout):
    def __init__(self, game, **kwargs):
        super(BufferRenderer, self).__init__(**kwargs)

        self.game = game

        self.size = self.game.RENDER_SIZE
        self.r_til = TileRenderer(self.game, Window.size)
        self.fbo_layout = FloatLayout()

        with self.canvas:
            self.fbo = Fbo(size=self.size)
            # create the fbo

            self.ids.GameImage.texture = self.fbo.texture

        with self.fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers(clear_color=True, clear_depth=True)

        # self.fbo.add_reload_observer(self.populate_fbo)

        self.r_box = LetterboxRenderer(self.game)
        canvas = self.canvas
        self.canvas = self.fbo
        self.add_widget(self.fbo_layout)
        self.add_widget(self.r_box)
        self.canvas = canvas

        self.enable_overworld()

    def fbo_add_widget(self, widget):
        self.fbo_layout.add_widget(widget)

    def fbo_remove_widget(self, widget):
        self.fbo_layout.remove_widget(widget)

    def populate_fbo(self, fbo):
        pass

    def update(self, time, dt):
        self.r_til.update(time, dt)
        self.r_box.update(time, dt)

    def enable_overworld(self):
        self.fbo_add_widget(self.r_til)

    def disable_overworld(self):
        self.fbo_layout.clear_widgets()


class LetterboxRenderer(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(LetterboxRenderer, self).__init__(**kwargs)

        with self.canvas:
            Color(0, 0, 0)
            self.rec1 = Rectangle(size=self.size, pos=self.pos)
            self.rec2 = Rectangle(size=self.size, pos=self.pos)

        self.box = 0.0
        self.box_to = 0.0

    def redraw(self, *args):
        self.size = self.game.RENDER_SIZE
        w = self.size[0]
        h = (self.box ** 0.5) * self.size[1] * 0.15
        self.rec1.pos = (0, 0)
        self.rec1.size = (w, h)
        self.rec2.pos = (0, self.size[1] - h)
        self.rec2.size = (w, h)

    def update(self, time=None, dt=None):
        if self.box > self.box_to:
            self.box -= dt * 2.6
            if self.box <= self.box_to:
                self.box = self.box_to

        if self.box < self.box_to:
            self.box += dt * 2.6
            if self.box >= self.box_to:
                self.box = self.box_to

        self.redraw()

    def go_to(self, box, force=False):
        self.box_to = box
        if force:
            self.box = box
