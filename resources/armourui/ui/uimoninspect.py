from ulivy.interface.baseui import BaseUI

from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file("resources/armourui/ui/uimoninspect.kv")


class UIMonInspect(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.show_area = 3

        self.selection = 0

        self.icon_frame = 0

    def update(self, time=None, frame_time=None):
        if time is None:
            time = 0
            frame_time = 0.05
        self.icon_frame = int(time * 4 % 2)

        self.update_selected_mon()
        return False

    def update_selected_mon(self):
        mon = self.game.inventory.members[self.selection]

        self.ids.Splash.source = mon.image_static[1]
        self.ids.Name.text = mon.name
        self.ids.Level.text = f"Lv. {mon.level}"
        self.ids.Gender.source = (
            f"resources/armourui/graphics/interface/mon/{mon.gender}.png"
        )

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            self.game.r_uin.close_ui(self)
        elif key == "up":
            self.selection = (self.selection - 1) % self.max_selection
        elif key == "down":
            self.selection = (self.selection + 1) % self.max_selection

    def event_unicode(self, char):
        pass

    @property
    def max_selection(self):
        return len(self.game.inventory.members)
