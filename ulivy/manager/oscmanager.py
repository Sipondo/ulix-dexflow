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

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.buttons = {
            "interact": False,
            "backspace": False,
            "walk": False,
            "run": False,
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

    def event_button(self, instance, pad, key):
        x, y = pad

        if x == 0 and y == 0 and self.buttons[key]:
            self.buttons[key] = False
            self.game.m_key.key_event(key, "up", [])
            return

        if (x != 0 or y != 0) and not self.buttons[key]:
            self.buttons[key] = True
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

        if x < -DEADZONE and not self.left:
            self.left = True
            self.game.m_key.key_event("left", "down", [])

        if x > DEADZONE and not self.right:
            self.right = True
            self.game.m_key.key_event("right", "down", [])

        if y < -DEADZONE and not self.up:
            self.up = True
            self.game.m_key.key_event("up", "down", [])

        if y > DEADZONE and not self.down:
            self.down = True
            self.game.m_key.key_event("down", "down", [])

        if x >= -DEADZONE and self.left:
            self.left = False
            self.game.m_key.key_event("left", "up", [])

        if x <= DEADZONE and self.right:
            self.right = False
            self.game.m_key.key_event("right", "up", [])

        if y >= -DEADZONE and self.up:
            self.up = False
            self.game.m_key.key_event("up", "up", [])

        if y <= DEADZONE and self.down:
            self.down = False
            self.game.m_key.key_event("down", "up", [])


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
