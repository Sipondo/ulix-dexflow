# import abc

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    NumericProperty,
    ListProperty,
)

from kivy.graphics.instructions import Callback


class PixelImage(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(texture=self._update_texture_filters)
        self.resized = False
        self.canvas.before.add(Callback(self.set_size))
        self.opacity = 0.0

    def set_size(self, instruction):
        self.opacity = 1.0
        if not self.resized:
            self.size_hint = (
                self.texture_size[0] / self.parent.size[0],
                self.texture_size[1] / self.parent.size[1],
            )

    # def set_size(self, instruction):
    #     try:
    #         size = self.parent.size
    #     except AttributeError:
    #         size = (1920.0, 1080.0)

    #     if not self.resized:
    #         self.size_hint = (
    #             self.texture_size[0] / size[0],
    #             self.texture_size[1] / size[1],
    #         )

    def _update_texture_filters(self, image, texture):
        try:
            texture.mag_filter = "nearest"
        except AttributeError:
            pass

    def update(self, time, frame_time):
        for child in self.children:
            child.update(time, frame_time)


class AliasImage(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(texture=self._update_texture_filters)
        self.resized = False
        self.canvas.before.add(Callback(self.set_size))
        self.opacity = 0.0

    def set_size(self, instruction):
        self.opacity = 1.0
        if not self.resized:
            self.size_hint = (
                self.texture_size[0] / self.parent.size[0],
                self.texture_size[1] / self.parent.size[1],
            )

    def _update_texture_filters(self, image, texture):
        try:
            texture.mag_filter = "nearest"
        except AttributeError:
            pass

    def update(self, time, frame_time):
        for child in self.children:
            child.update(time, frame_time)


class NormalImage(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #     self.bind(texture=self._update_texture_filters)

    # def _update_texture_filters(self, image, texture):
    #     texture.mag_filter = "nearest"

    def update(self, time, frame_time):
        for child in self.children:
            child.update(time, frame_time)


class BaseUI(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        self.block_input = False
        super().__init__(**kwargs)

    def on_enter(self, **kwargs):
        pass

    def update(self, time=None, frame_time=None):
        pass

    def on_exit(self):
        return True

    def event_keypress(self, key, modifiers):
        return

    def event_unicode(self, char):
        return
