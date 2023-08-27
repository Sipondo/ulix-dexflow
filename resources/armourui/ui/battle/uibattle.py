from kivy.lang import Builder

from ulivy.interface.baseui import BaseUI

Builder.load_file("resources/armourui/ui/battle/uibattle.kv")


class UIBattle(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.show_area = 3

        self.options = [
            "fight",
            "mon",
            "bag",
            "run",
        ]
        self.selection = 0

    def update(self, time=None, frame_time=None):
        self.ids.Window.opacity = 1
        self.highlight_options()
        return False

    def highlight_options(self):
        """Highlight menu options.
        We significantly reduce boilerplate by making the filenames
        and elementnames correspond to the options list.
        This allows us to get the element attribute in a for loop.
        """
        for option in self.options:
            element = getattr(self.ids, f"Option{option.capitalize()}")
            if option == self.options[self.selection]:
                element.source = f"resources/armourui/graphics/interface/battle/option_{option}_sel.png"
                self.ids.Arrow.pos_hint = {
                    "center_x": element.pos_hint["center_x"] - 0.09,
                    "center_y": element.pos_hint["center_y"],
                }
            else:
                element.source = (
                    f"resources/armourui/graphics/interface/battle/option_{option}.png"
                )

    def select_option(self):
        if self.options[self.selection] == "mon":
            self.game.r_uin.switch_ui("monview")
        if self.options[self.selection] == "save":
            self.game.r_uin.switch_ui("save")
        if self.options[self.selection] == "vs":
            self.game.r_uin.switch_ui("vsmain")

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            self.game.r_uin.close_ui(self)
        elif key == "interact":
            self.select_option()
        elif key == "down":
            self.selection = (self.selection + 1) % len(self.options)
        elif key == "up":
            self.selection = (self.selection - 1) % len(self.options)

    def event_unicode(self, char):
        pass
