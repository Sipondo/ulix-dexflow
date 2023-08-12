from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file("resources/armourui/ui/paneltrivia.kv")


class PanelTrivia(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def on_enter(self, **kwargs):
    #     self.block_input = False
    #     self.show_area = 3

    #     self.selection_mon = 0
    #     self.selection_option = 0

    # def update(self, time=None, frame_time=None):
    #     if time is None:
    #         time = 0
    #         frame_time = 0.05
    #     self.icon_frame = int(time * 4 % 2)

    #     return False

    # def event_unicode(self, char):
    #     pass

    # @property
    # def max_selection_mon(self):
    #     return len(self.game.inventory.members)
