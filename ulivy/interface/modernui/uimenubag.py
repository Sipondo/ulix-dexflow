from ..baseui import BaseUI
from kivy.lang import Builder

Builder.load_file("ulivy/interface/modernui/uimenubag.kv")


class UIMenuBag(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.selection = 0
        self.max_selection = 9

        self.page = 0
        self.pages = [
            "menubag_items.png",
            "menubag_medicine.png",
            "menubag_pokeballs.png",
            "menubag_tmhm.png",
            "menubag_berries.png",
            "menubag_mail.png",
            "menubag_battleitems.png",
            "menubag_keyitems.png",
        ]
        self.highlight_page()

    @property
    def max_page(self):
        return len(self.pages)

    def update(self, time=None, frame_time=None):
        return False

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            self.game.m_gst.switch_state("overworld")
        if key == "down":
            self.selection = (self.selection + 1) % self.max_selection
            self.game.r_aud.effect("select")
        elif key == "up":
            self.selection = (self.selection - 1) % self.max_selection
            self.game.r_aud.effect("select")
        elif key == "right":
            self.page = (self.page + 1) % self.max_page
            self.game.r_aud.effect("select")
        elif key == "left":
            self.page = (self.page - 1) % self.max_page
            self.game.r_aud.effect("select")
        elif key == "interact":
            pass

        self.highlight_page()

    def highlight_page(self):
        self.ids.BagBackground.source = (
            f"ulivy/interface/modernui/{self.pages[self.page]}"
        )
