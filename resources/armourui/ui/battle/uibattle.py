from kivy.lang import Builder

from ulivy.interface.baseui import BaseUI

from resources.armourui.ui.battle.battlepanelmoves import BattlePanelMoves

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

        self.panel = None

    def update(self, time=None, frame_time=None):
        self.ids.Window.opacity = 1
        self.highlight_options()
        self.update_hud()

        if self.panel is not None:
            self.panel.update(time, frame_time)
        return False

    def update_hud(self):
        """Update HUD
        Update all HUD elements so that they correspond to the current battlestate"""
        bat = self.game.m_bat

        self.ids.OurMonFirstText.text = bat.state.name_1
        self.ids.TheirMonFirstText.text = bat.state.name_2

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
        if self.options[self.selection] == "fight":
            self.panel = BattlePanelMoves()
            self.ids.Window.add_widget(self.panel)
        elif self.options[self.selection] == "mon":
            self.game.r_uin.switch_ui("monview")
        elif self.options[self.selection] == "save":
            self.game.r_uin.switch_ui("save")
        elif self.options[self.selection] == "vs":
            self.game.r_uin.switch_ui("vsmain")

    def event_keypress(self, key, modifiers):
        if self.panel is not None:
            self.panel.event_keypress(key, modifiers)
            return

        if key == "backspace":
            pass
        elif key == "interact":
            self.select_option()
        elif key == "down":
            self.selection = (self.selection + 1) % len(self.options)
        elif key == "up":
            self.selection = (self.selection - 1) % len(self.options)

    def event_unicode(self, char):
        pass
