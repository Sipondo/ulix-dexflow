from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    ReferenceListProperty,
    ListProperty,
)
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle


class Game(FloatLayout):
    pass


class Background(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)


class Bounds(RelativeLayout):
    pass


class test(App):
    game = ObjectProperty(None)

    def build(self):
        self.game = Game()
        return self.game


if __name__ == "__main__":
    test().run()
