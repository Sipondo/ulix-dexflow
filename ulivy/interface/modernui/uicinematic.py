from ..baseui import BaseUI
from kivy.lang import Builder

Builder.load_file("ulivy/interface/modernui/uicinematic.kv")


class UICinematic(BaseUI):
    def on_enter(self, **kwargs):
        pass

    def update(self, time, frame_time):
        return False

    def on_exit(self):
        pass
