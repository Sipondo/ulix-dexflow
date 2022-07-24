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

        # self.fbo.add_reload_observer(self.populate_fbo)

        canvas = self.canvas
        self.canvas = self.fbo
        self.add_widget(self.fbo_layout)
        self.canvas = canvas

        self.enable_overworld()

    def fbo_add_widget(self, widget):
        self.fbo_layout.add_widget(widget)

    def populate_fbo(self, fbo):
        pass

    def update(self, time, dt):
        self.r_til.update(time, dt)
        pass

    def enable_overworld(self):
        self.fbo_add_widget(self.r_til)

    def disable_overworld(self):
        self.fbo_layout.clear_widgets()
