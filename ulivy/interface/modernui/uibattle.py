from ..baseui import BaseUI
from kivy.lang import Builder

Builder.load_file("ulivy/interface/modernui/uibattle.kv")


class UIBattle(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = True

    def update(self, time=None, frame_time=None):
        return False

    def event_keypress(self, key, modifiers):
        pass

    def event_unicode(self, char):
        pass
