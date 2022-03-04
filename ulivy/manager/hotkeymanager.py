from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.utils import platform


class HotkeyManager(Widget):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game

        self.keys = []
        self.pressed_keys = set()

        self.register_key("ctrl", "ctrl")
        self.register_key("alt", "alt")
        self.register_key("shift", "shift")

        self.register_key("ctrl", "rctrl")
        self.register_key("alt", "ralt")
        self.register_key("shift", "rshift")

        self.register_key("alt", "walk")
        self.register_key("shift", "run")
        self.register_key("ctrl", "bike")

        self.register_key("up", "w")
        self.register_key("down", "s")
        self.register_key("left", "a")
        self.register_key("right", "d")

        self.register_key("up", "up")
        self.register_key("down", "down")
        self.register_key("left", "left")
        self.register_key("right", "right")

        self.register_key("backspace", "x")
        self.register_key("backspace", "backspace", True)
        self.register_key("interact", "interact")
        self.register_key("interact", "c")
        self.register_key("interact", "enter")
        self.register_key("interact", "z")
        self.register_key("interact", "space")

        self.register_key("enter", "enter", True)

        self.register_key("maphack", "h")
        self.register_key("debug", "t")

        self.register_key("zoom_out", "equal")
        self.register_key("zoom_out", "8")
        self.register_key("zoom_in", "-")
        self.register_key("zoom_in", "2")

        self.register_key("menu", "m")
        self.register_key("menu", "x")
        self.register_key("battle", "b")

        # self.register_key("fullscreen", game.wnd.keys.F11, True)
        self.register_key("fullscreen", "f11")

        self.bind_keyboard()

    def bind_keyboard(self):
        if platform == "android":
            return

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, "text")
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def register_key(self, name, key, block=False):
        self.keys.append((key, name, block))

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

        self.bind_keyboard()

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print("The key", keycode, "has been pressed")
        # print(" - text is %r" % text)
        # print(" - modifiers are %r" % modifiers)
        self.key_event(keycode[1], "down", modifiers)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        self.key_event(keycode[1], "up", None)
        return True

    def key_event(self, key, action, modifiers):
        request_list = self.lookup_key(key)
        print(f"keypress {key}\t{action}\t{modifiers}")

        for request in request_list:
            # print(f"--- REQUEST {key}\t{request}\t{action}\t{modifiers}")

            if key == "p" and action == "down":
                print(self.game.m_ent.player.get_pos())

            if request == "maphack" and action == "down":
                self.game.maphack = not self.game.maphack
                print(f"Maphack is now {self.game.maphack}")

            if request:
                # print(request)
                if action == "down":
                    if request == "fullscreen":
                        Window.fullscreen = not Window.fullscreen

                    if request not in self.pressed_keys:
                        self.game.m_gst.current_state.event_keypress(
                            request, modifiers,
                        )
                        self.pressed_keys.add(request)

                elif action == "up":
                    try:
                        self.pressed_keys.remove(request)
                    except Exception as e:
                        pass

    def unicode_char_entered(self, char):
        self.game.m_gst.current_state.event_unicode(char)

    def lookup_key(self, key):
        r = []
        for t in self.keys:
            if key == t[0]:
                if not self.game.m_gst.current_state.block_input or t[2]:
                    r.append(t[1])
        if r:
            return r
        return [""]
