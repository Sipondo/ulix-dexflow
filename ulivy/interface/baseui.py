import abc

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


class BaseUI(FloatLayout, abc.ABC):
    def __init__(self, game):
        self.game = game

    @abc.abstractmethod
    def on_enter(self, **kwargs):
        pass

    @abc.abstractmethod
    def update(self, time, frame_time):
        return self.lock

    @abc.abstractmethod
    def on_exit(self):
        pass
