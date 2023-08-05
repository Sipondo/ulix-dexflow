from ulivy.manager.pluginmanager import Plugin


from resources.armourui.ui.uioverworld import UIOverworld
from resources.armourui.ui.uimainmenu import UIMainMenu
from resources.armourui.ui.uimonview import UIMonView
from resources.armourui.ui.uimoninspect import UIMonInspect


class Armourui(Plugin):
    def pre_load(self, **kwargs):
        print("ARMOURUI PRE")
        pass

    def post_load(self, **kwargs):
        print("ARMOURUI POST")
        self.game.r_uin.register_ui("overworld", UIOverworld)
        self.game.r_uin.register_ui("mainmenu", UIMainMenu)
        self.game.r_uin.register_ui("monview", UIMonView)
        self.game.r_uin.register_ui("moninspect", UIMonInspect)
        pass

    def update(self, time, frame_time):
        return self.lock

    @property
    def priority(self):
        return 0
