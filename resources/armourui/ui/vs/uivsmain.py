from kivy.lang import Builder

from ulivy.interface.baseui import BaseUI

Builder.load_file("resources/armourui/ui/vs/uivsmain.kv")


class UIVsMain(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False

        self.options = ["linkbattle", "linktrade", "surprisetrade"]
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
                element.source = (
                    f"resources/armourui/graphics/interface/vs/main/{option}_sel.png"
                )
                # self.ids.Arrow.pos_hint = {
                #     "center_x": element.pos_hint["center_x"] - 0.055,
                #     "center_y": element.pos_hint["center_y"],
                # }
            else:
                element.source = (
                    f"resources/armourui/graphics/interface/vs/main/{option}.png"
                )

    def select_option(self):
        if self.options[self.selection] == "linkbattle":
            self.game.r_uin.switch_ui("monview")

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            self.game.r_uin.close_ui(self)
        elif key == "interact":
            self.select_option()
        elif key == "up":
            self.selection = (self.selection - 1) % len(self.options)
        elif key == "down":
            self.selection = (self.selection + 1) % len(self.options)

    def event_unicode(self, char):
        pass
