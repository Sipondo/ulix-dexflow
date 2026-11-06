class HotkeyManager:
    def __init__(self, game):
        self.game = game

        self.keys = []
        self.pressed_keys = set()

        # Movement keys
        self.register_key("up", "w")
        self.register_key("down", "s")
        self.register_key("left", "a")
        self.register_key("right", "d")

        self.register_key("up", "up")
        self.register_key("down", "down")
        self.register_key("left", "left")
        self.register_key("right", "right")

        # Speed / walk / run modifiers
        self.register_key("shift", "shift")
        self.register_key("shift", "rshift")
        self.register_key("alt", "alt")
        self.register_key("alt", "ralt")

        # Actions
        self.register_key("interact", "z")
        self.register_key("interact", "c")
        self.register_key("interact", "enter")
        self.register_key("interact", "return")
        self.register_key("interact", "space")

        self.register_key("backspace", "x")
        self.register_key("backspace", "backspace")

        self.register_key("maphack", "h")
        self.register_key("debug", "t")

        # Zoom
        self.register_key("zoom_out", ",")
        self.register_key("zoom_out", "q")
        self.register_key("zoom_in", ".")
        self.register_key("zoom_in", "e")

    def register_key(self, name, key, block=False):
        self.keys.append((key.lower(), name, block))

    def lookup_key(self, key):
        key = key.lower()
        if key == "return":
            key = "enter"
        r = []
        for t in self.keys:
            if key == t[0]:
                r.append(t[1])
        return r

    def event(self, event):
        if event.kind not in ("key_down", "key_up"):
            return

        action = "down" if event.kind == "key_down" else "up"
        self.key_event(event.key, action)

    def key_event(self, key, action, modifiers=None, unicode=None):
        request_list = self.lookup_key(key)

        for request in request_list:
            if action == "down":
                if request == "maphack":
                    if hasattr(self.game, "maphack"):
                        self.game.maphack = not self.game.maphack
                        print(f"Maphack is now {self.game.maphack}")

                if request == "zoom_in":
                    self.game.m_pan.zoom_in()
                elif request == "zoom_out":
                    self.game.m_pan.zoom_out()

                if request not in self.pressed_keys:
                    self.pressed_keys.add(request)
                    if hasattr(self.game, "m_gst") and self.game.m_gst:
                        self.game.m_gst.event_keypress(request, modifiers)
                    if hasattr(self.game, "r_uin") and self.game.r_uin:
                        self.game.r_uin.event_keypress(request, modifiers)

            elif action == "up":
                self.pressed_keys.discard(request)

    def get_movement_direction(self):
        """Returns the first active directional input, or None."""
        for d in ("up", "down", "left", "right"):
            if d in self.pressed_keys:
                return d
        return None
