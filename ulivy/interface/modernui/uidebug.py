from ..baseui import BaseUI
from kivy.lang import Builder

Builder.load_file("ulivy/interface/modernui/uidebug.kv")


class UIDebug(BaseUI):
    def on_enter(self, **kwargs):
        self.selection = 0
        self.input = ""
        self.block_input = True
        self.initialised = False

    def update(self, time=None, frame_time=None):

        if not self.initialised:
            self.initialised = True
            self.input = ""

        self.ids.DebugText.text = self.input or ""

        return False

    def event_keypress(self, key, modifiers):
        if key == "enter":
            print("Debug:", self.input)
            try:
                self.game.debug_input = self.input.split(" ")
                mapstring = self.game.m_map.convert_mapstring_to_key(
                    self.game.debug_input[0]
                )
                y, x = self.game.m_map.get_level_size(mapstring)
                if len(self.game.debug_input) == 1:
                    self.game.debug_input.append(y // 2)
                if len(self.game.debug_input) == 2:
                    self.game.debug_input.append(x // 2)
                self.game.m_gst.switch_to_previous_state()
                self.game.m_act.create_prefab_action("debug_teleport", self.game)
            except Exception as e:
                self.game.debug_input = ""
                try:
                    upl = self.game.m_upl.parser.parse(self.input)
                    self.game.m_gst.switch_to_previous_state()
                    self.game.m_act.create_action(upl, self.game)
                except Exception as e:
                    try:
                        upl = self.game.m_upl.parser.parse(f"game: {self.input}")
                        self.game.m_gst.switch_to_previous_state()
                        self.game.m_act.create_action(upl, self.game)
                    except Exception as e:
                        print("\n\n>>>DEBUG COMMAND INVALID<<<", self.input, "\n" * 2)
                        self.game.m_gst.switch_to_previous_state()

    def event_unicode(self, char):
        if char.lower() == "backspace":
            if len(self.input):
                self.input = self.input[:-1]
            return
        self.input += char
