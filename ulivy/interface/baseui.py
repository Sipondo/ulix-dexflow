# import abc

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    NumericProperty,
    ListProperty,
)


class PixelImage(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(texture=self._update_texture_filters)

    def _update_texture_filters(self, image, texture):
        texture.mag_filter = "nearest"

    def update(self, time, frame_time):
        for child in self.children:
            child.update(time, frame_time)


class BaseUI(FloatLayout):
    def __init__(self, game, gstate, **kwargs):
        self.game = game
        self.gstate = gstate
        self.block_input = False
        super().__init__(**kwargs)

        print("BASEUI", self.pos, self.size)

    def on_enter(self, **kwargs):
        pass

    def update(self, time=None, frame_time=None):
        pass

    def on_exit(self):
        pass

    def event_keypress(self, key, modifiers):
        return

    def event_unicode(self, char):
        return
