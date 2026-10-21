from ulivy.manager.joystick import Joystick
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.label import Label

DEADZONE = 0.5


class OscManager(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        super(OscManager, self).__init__(**kwargs)
        self._bind_joysticks()

        self.val_x = 0
        self.val_y = 0

        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

        self.buttons = {
            "interact": 0,
            "backspace": 0,
            "walk": 0,
            "run": 0,
        }

    def _bind_joysticks(self):
        joysticks = self._get_joysticks(self)
        for joystick in joysticks:
            joystick.bind(pad=self._update_pad_display)

    def _get_joysticks(self, parent):
        joysticks = []
        if isinstance(parent, Joystick):
            joysticks.append(parent)
        elif hasattr(parent, "children"):
            for child in parent.children:
                joysticks.extend(self._get_joysticks(child))
        return joysticks

    def _update_pad_display(self, instance, pad):
        if instance.parent == self.ids.movement:
            self.event_movement(instance, pad)
        elif instance.parent == self.ids.interact:
            self.event_button(instance, pad, "interact")
        elif instance.parent == self.ids.backspace:
            self.event_button(instance, pad, "backspace")
        elif instance.parent == self.ids.walk:
            self.event_button(instance, pad, "walk")
        elif instance.parent == self.ids.run:
            self.event_button(instance, pad, "run")
        # elif instance.parent == self.ids.bike:
        #     self.event_button(instance, pad, "bike")

    def update(self, time, frame_time):
        for k, v in self.buttons.items():
            if v < 0:
                v += frame_time
                if v >= 0:
                    self.game.m_key.key_event(k, "up", [])
                    v = 0
                self.buttons[k] = v

        if self.left < 0:
            self.left += frame_time
            if self.left >= 0:
                self.game.m_key.key_event("left", "up", [])
                self.left = 0

        if self.right < 0:
            self.right += frame_time
            if self.right >= 0:
                self.game.m_key.key_event("right", "up", [])
                self.right = 0

        if self.up < 0:
            self.up += frame_time
            if self.up >= 0:
                self.game.m_key.key_event("up", "up", [])
                self.up = 0

        if self.down < 0:
            self.down += frame_time
            if self.down >= 0:
                self.game.m_key.key_event("down", "up", [])
                self.down = 0

    def event_button(self, instance, pad, key):
        x, y = pad
        # print(pad)

        if x == 0 and y == 0 and self.buttons[key]:
            # print("up")
            self.buttons[key] = -0.1
            return

        if (x != 0 and y != 0) and not self.buttons[key]:
            # print("down")
            self.buttons[key] = 0.1
            self.game.m_key.key_event(key, "down", [])
            return

    def event_movement(self, instance, pad):
        x, y = pad
        # x, y = (("x: " + x), ("\ny: " + y))
        r = "radians: " + str(instance.radians)[0:5]
        m = "\nmagnitude: " + str(instance.magnitude)[0:5]
        a = "\nangle: " + str(instance.angle)[0:5]

        y = -y

        self.val_x = x
        self.val_y = y

        if abs(x) > abs(y):
            y = 0
        else:
            x = 0

        if x < -DEADZONE and not self.left:
            self.left = 0.05
            self.game.m_key.key_event("left", "down", [])

        elif x > DEADZONE and not self.right:
            self.right = 0.05
            self.game.m_key.key_event("right", "down", [])

        elif x >= -DEADZONE and self.left:
            self.left = -0.05
            # self.game.m_key.key_event("left", "up", [])

        elif x <= DEADZONE and self.right:
            self.right = -0.05
            # self.game.m_key.key_event("right", "up", [])

        if y < -DEADZONE and not self.up:
            self.up = 0.05
            self.game.m_key.key_event("up", "down", [])

        elif y > DEADZONE and not self.down:
            self.down = 0.05
            self.game.m_key.key_event("down", "down", [])

        elif y >= -DEADZONE and self.up:
            self.up = -0.05
            # self.game.m_key.key_event("up", "up", [])

        elif y <= DEADZONE and self.down:
            self.down = -0.05
            # self.game.m_key.key_event("down", "up", [])


class FPSCounter(AnchorLayout):
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
