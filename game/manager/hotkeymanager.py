class HotkeyManager:
    def __init__(self, game):
        self.game = game

        self.keys = {}
        self.pressed_keys = set()

        self.register_key("up", game.wnd.keys.W)
        self.register_key("down", game.wnd.keys.S)
        self.register_key("left", game.wnd.keys.A)
        self.register_key("right", game.wnd.keys.D)

        self.register_key("up", game.wnd.keys.UP)
        self.register_key("down", game.wnd.keys.DOWN)
        self.register_key("left", game.wnd.keys.LEFT)
        self.register_key("right", game.wnd.keys.RIGHT)

        self.register_key("backspace", game.wnd.keys.X)
        self.register_key("backspace", game.wnd.keys.BACKSPACE)
        self.register_key("interact", game.wnd.keys.C)
        self.register_key("interact", game.wnd.keys.ENTER)
        self.register_key("interact", game.wnd.keys.Z)
        self.register_key("interact", game.wnd.keys.SPACE)

        self.register_key("maphack", game.wnd.keys.H)

        self.register_key("zoom_out", game.wnd.keys.EQUAL)
        self.register_key("zoom_in", game.wnd.keys.MINUS)

        self.register_key("menu", game.wnd.keys.M)
        self.register_key("menu", game.wnd.keys.X)
        self.register_key("battle", game.wnd.keys.B)

        self.register_key("fullscreen", game.wnd.keys.F11)

    def register_key(self, name, key):
        self.keys[key] = name

    def key_event(self, key, action, modifiers):
        request = self.lookup_key(key)
        # print(f"keypress {key}\t{request}\t{action}\t{modifiers}")

        if key == self.game.wnd.keys.P and action == self.game.wnd.keys.ACTION_PRESS:
            print(self.game.m_ent.player.get_pos())

        if request == "maphack" and action == self.game.wnd.keys.ACTION_PRESS:
            self.game.maphack = not self.game.maphack
            print(f"Maphack is now {self.game.maphack}")

        if action == self.game.wnd.keys.ACTION_PRESS:
            self.game.m_gst.current_state.event_keypress(
                request, modifiers,
            )

        if request:
            print(request)
            if action == self.game.wnd.keys.ACTION_PRESS:
                if request == "fullscreen":
                    self.game.wnd.fullscreen = not self.game.wnd.fullscreen
                self.pressed_keys.add(request)

            elif action == self.game.wnd.keys.ACTION_RELEASE:
                self.pressed_keys.remove(request)

    def lookup_key(self, key):
        if key in self.keys.keys():
            return self.keys[key]
        return False
