from ..baseui import BaseUI
from kivy.lang import Builder

Builder.load_file("ulivy/interface/modernui/uimenumain.kv")


class UIMenuMain(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.selection = 0
        self.max_selection = 9
        self.highlight_selection()

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
        elif key == "interact":
            if self.selection == 2:
                self.game.m_gst.switch_state("menubag")
            pass

        self.highlight_selection()

    def highlight_selection(self):
        s = self.selection
        self.ids.PokedexMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_pokedex{"_high" if s==0 else ""}.png'
        )
        self.ids.PokemonMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_pokemon{"_high" if s==1 else ""}.png'
        )
        self.ids.BagMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_bag{"_high" if s==2 else ""}.png'
        )
        self.ids.PokegearMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_pokegear{"_high" if s==3 else ""}.png'
        )
        self.ids.CardMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_card{"_high" if s==4 else ""}.png'
        )
        self.ids.SaveMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_save{"_high" if s==5 else ""}.png'
        )
        self.ids.OptionsMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_options{"_high" if s==6 else ""}.png'
        )
        self.ids.ExitMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_exit{"_high" if s==7 else ""}.png'
        )
        self.ids.ReturnMenuBackground.source = (
            f'ulivy/interface/modernui/menumain_return{"_high" if s==8 else ""}.png'
        )
