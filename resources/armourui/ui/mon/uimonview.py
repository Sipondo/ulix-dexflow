from ulivy.interface.baseui import BaseUI

from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file("resources/armourui/ui/mon/uimonview.kv")

WHITE = (1, 1, 1, 1)
BLACK = (0, 0, 0, 1)


class MonCell(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UIMonView(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.show_area = 3

        self.options = [f"mon{i}" for i in range(1, 7)]
        self.selection = 0

        self.icon_frame = 0

    def update(self, time=None, frame_time=None):
        if time is None:
            time = 0
            frame_time = 0.05
        self.icon_frame = int(time * 4 % 2)

        self.update_mons()
        self.highlight_options()
        return False

    def update_mons(self):
        for i, option in enumerate(self.options):
            element = getattr(self.ids, option.capitalize())

            if i > len(self.game.inventory.members):
                element.opacity = 0
                continue

            element.opacity = 1
            mon = self.game.inventory.members[i]

            element.ids.Name.text = mon.name
            element.ids.Level.text = f"Lv. {mon.level}"
            element.ids.Icon.source = mon.icon[self.icon_frame]
            element.ids.Gender.source = (
                f"resources/armourui/graphics/interface/mon/{mon.gender}.png"
            )

            hp_ratio = mon.current_hp / mon.hp
            element.ids.Hp.text = f"{mon.current_hp}/{mon.hp}"
            element.ids.HpBar.size_hint = (float(0.6 * hp_ratio), 0.1)
            if hp_ratio < 0.2:
                element.ids.HpBar.source = (
                    "resources/armourui/graphics/interface/mon/bar_red.png"
                )
            elif hp_ratio < 0.5:
                element.ids.HpBar.source = (
                    "resources/armourui/graphics/interface/mon/bar_yellow.png"
                )
            elif hp_ratio < 0.2:
                element.ids.HpBar.source = (
                    "resources/armourui/graphics/interface/mon/bar_green.png"
                )

    def highlight_options(self):
        """Highlight menu options.
        We significantly reduce boilerplate by making the filenames
        and elementnames correspond to the options list.
        This allows us to get the element attribute in a for loop.
        """
        for i, option in enumerate(self.options):
            element = getattr(self.ids, option.capitalize())
            if option == self.options[self.selection]:
                element.ids.Background.source = (
                    f"resources/armourui/graphics/interface/mon/mon_cell_sel.png"
                )
                element.ids.Name.color = WHITE
                element.ids.Hp.color = WHITE
                element.ids.Level.color = WHITE

                self.ids.Arrow.pos_hint = {
                    "center_x": element.pos_hint["center_x"] - 0.15,
                    "center_y": element.pos_hint["center_y"],
                }

                mon = self.game.inventory.members[i]
                self.ids.Splash.source = mon.image_static[1]
            else:
                element.ids.Background.source = (
                    f"resources/armourui/graphics/interface/mon/mon_cell.png"
                )
                element.ids.Name.color = BLACK
                element.ids.Hp.color = BLACK
                element.ids.Level.color = BLACK

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            self.game.r_uin.close_ui(self)
        elif key == "interact":
            self.game.r_uin.switch_ui("moninspect")
        elif key == "up":
            self.selection = (self.selection - 1) % self.max_selection
        elif key == "down":
            self.selection = (self.selection + 1) % self.max_selection

    def event_unicode(self, char):
        pass

    @property
    def max_selection(self):
        return min(len(self.options), len(self.game.inventory.members))
