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
        self.resized = False

    def _update_texture_filters(self, image, texture):
        try:
            texture.mag_filter = "nearest"
            if not self.resized:
                self.size_hint = (
                    self.texture_size[0] / 1920.0 * self.parent.size_hint[0],
                    self.texture_size[1] / 1080.0 * self.parent.size_hint[1],
                )
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

    def _update_texture_filters(self, image, texture):
        # try:
        # print(self.parent.id)
        texture.mag_filter = "linear"
        if not self.resized:
            self.size_hint = (
                self.texture_size[0] / 1920.0 * self.parent.size_hint[0],
                self.texture_size[1] / 1080.0 * self.parent.size_hint[1],
            )
        # except AttributeError:
        # pass

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
