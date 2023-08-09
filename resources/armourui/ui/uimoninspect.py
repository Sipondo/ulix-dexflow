from ulivy.interface.baseui import BaseUI

from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

from resources.armourui.ui.paneloverview import PanelOverview

Builder.load_file("resources/armourui/ui/uimoninspect.kv")


class UIMonInspect(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.show_area = 3

        self.options = ("overview", "stats", "moves", "trivia", "ribbons")

        self.selection_mon = 0
        self.selection_option = 0

        self.pane_name = None
        self.pane = None

    def update(self, time=None, frame_time=None):
        if time is None:
            time = 0
            frame_time = 0.05
        self.icon_frame = int(time * 4 % 2)

        self.update_selected_mon()
        self.highlight_options()
        return False

    def update_selected_mon(self):
        mon = self.game.inventory.members[self.selection_mon]

        self.ids.Splash.source = mon.image_static[1]
        self.ids.Name.text = mon.name
        self.ids.Level.text = f"Lv. {mon.level}"
        self.ids.Gender.source = (
            f"resources/armourui/graphics/interface/mon/{mon.gender}.png"
        )

    def highlight_options(self):
        """Highlight menu options.
        We significantly reduce boilerplate by making the filenames
        and elementnames correspond to the options list.
        This allows us to get the element attribute in a for loop.
        """
        for option in self.options:
            element = getattr(self.ids, f"Option{option.capitalize()}")
            if option == self.options[self.selection_option]:
                element.source = f"resources/armourui/graphics/interface/mon/inspect/option_{option}_sel.png"

                if self.pane_name != option:
                    self.pane_name = option

                    if self.pane is not None:
                        self.ids.Window.remove_widget(self.pane)
                        del self.pane

                    if option == "overview":
                        self.pane = PanelOverview()
                        self.ids.Window.add_widget(self.pane)
                    else:
                        self.pane = None
            else:
                element.source = f"resources/armourui/graphics/interface/mon/inspect/option_{option}.png"

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            self.game.r_uin.close_ui(self)
        elif key == "up":
            self.selection_mon = (self.selection_mon - 1) % self.max_selection_mon
        elif key == "down":
            self.selection_mon = (self.selection_mon + 1) % self.max_selection_mon
        elif key == "left":
            self.selection_option = (self.selection_option - 1) % len(self.options)
        elif key == "right":
            self.selection_option = (self.selection_option + 1) % len(self.options)

    def event_unicode(self, char):
        pass

    @property
    def max_selection_mon(self):
        return len(self.game.inventory.members)
