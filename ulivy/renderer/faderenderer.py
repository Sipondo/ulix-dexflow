from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.graphics import Color, Rectangle


class FadeRenderer(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(FadeRenderer, self).__init__(**kwargs)

        self.alpha = 1.0
        self.alpha_to = 1.0

        self.update_canvas()

    def update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0, self.alpha)
            self.rec1 = Rectangle(size=self.size, pos=self.pos)

    def redraw(self, *args):
        self.rec1.pos = self.pos
        self.rec1.size = self.size

    def update(self, time=None, dt=None):
        update_canvas = False
        if self.alpha > self.alpha_to:
            self.alpha -= dt * 2.6
            if self.alpha <= self.alpha_to:
                self.alpha = self.alpha_to
            update_canvas = True

        if self.alpha < self.alpha_to:
            self.alpha += dt * 2.6
            if self.alpha >= self.alpha_to:
                self.alpha = self.alpha_to
            update_canvas = True

        if update_canvas:
            self.update_canvas()

        self.redraw()

    def fade_done(self):
        return self.alpha == self.alpha_to

    def go_to(self, alpha):
        self.alpha_to = alpha
