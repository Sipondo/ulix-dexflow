from kivy.lang import Builder

from ulivy.interface.baseui import BaseUI

Builder.load_file("resources/armourui/ui/save/uisave.kv")


class UISave(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False

    def update(self, time=None, frame_time=None):
        self.ids.Window.opacity = 1
        return False

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            self.game.r_uin.close_ui(self)

    def event_unicode(self, char):
        pass
