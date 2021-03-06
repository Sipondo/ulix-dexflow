from ..baseui import BaseUI
from kivy.lang import Builder

Builder.load_file("ulivy/interface/modernui/uiprompt.kv")


class UIPrompt(BaseUI):
    def on_enter(self, **kwargs):
        self.selection = 0
        self.input = ""
        self.block_input = True
        self.initialised = False

        self.cursor = "|"
        self.cursor_timer = 0

    def update(self, time=None, frame_time=None):
        if time is not None and time - self.cursor_timer > 0.4:
            self.cursor_timer = time
            self.cursor = "" if self.cursor else "|"

        if not self.initialised:
            self.initialised = True
            self.input = ""

        self.ids.PromptText.text = (self.input or "") + self.cursor

        return False

    def event_keypress(self, key, modifiers):
        if key == "enter":
            print("Input:", self.input)
            self.game.text_input = self.input
            self.game.m_gst.switch_to_previous_state()

    def event_unicode(self, char):
        if char.lower() == "backspace":
            if len(self.input):
                self.input = self.input[:-1]
            return
        if len(self.input) >= self.gstate.length:
            return
        if self.gstate.filter == "letters":
            if not char.isalpha():
                return
        self.input += char
