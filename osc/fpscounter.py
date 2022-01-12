from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.label import Label

class FPSCounter(AnchorLayout):
    # property to set the source code for fragment shader
    counter = NumericProperty()
    age = NumericProperty()

    def __init__(self, **kwargs):
        super(FPSCounter, self).__init__(anchor_x="left", anchor_y="top")
        Clock.schedule_interval(self.update_counter, 0)
        Clock.schedule_interval(self.update_label, 1 / 4)

    def update_counter(self, dt):
        self.counter += 1
        self.age += dt

    def update_label(self, dt):
        if self.age > 0.6:
            self.age = self.age / 2
            self.counter = self.counter / 2
        self.clear_widgets()
        self.add_widget(
            Label(
                text=f"[color=3333dd]{(self.counter+self.age) // self.age:.0f}[/color]",
                size=(50, 15),
                size_hint=(None, None),
                markup=True,
            )
        )
