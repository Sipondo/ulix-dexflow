# from kivy.config import Config

# Config.set("graphics", "window_state", "maximized")
from kivy.app import App
from osc.joystick import Joystick
from kivy.uix.floatlayout import FloatLayout


# class JoystickDemo(FloatLayout):
#     pass


class JoystickDemo(FloatLayout):
    def __init__(self, **kwargs):
        super(JoystickDemo, self).__init__(**kwargs)
        self._bind_joysticks()

        self.val_x = 0
        self.val_y = 0

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
        x, y = pad
        # x, y = (("x: " + x), ("\ny: " + y))
        r = "radians: " + str(instance.radians)[0:5]
        m = "\nmagnitude: " + str(instance.magnitude)[0:5]
        a = "\nangle: " + str(instance.angle)[0:5]

        self.val_x = x
        self.val_y = -y

        print(instance.radians)
