from ulivy.manager.pluginmanager import Plugin


from resources.armourui.ui.uioverworld import UIOverworld
from resources.armourui.ui.uicinematic import UICinematic
from resources.armourui.ui.battle.uibattle import UIBattle
from resources.armourui.ui.uimainmenu import UIMainMenu
from resources.armourui.ui.mon.uimonview import UIMonView
from resources.armourui.ui.mon.uimoninspect import UIMonInspect
from resources.armourui.ui.vs.uivsmain import UIVsMain
from resources.armourui.ui.save.uisave import UISave


class Armourui(Plugin):
    def pre_load(self, **kwargs):
        print("ARMOURUI PRE")
        pass

    def post_load(self, **kwargs):
        print("ARMOURUI POST")
        self.game.r_uin.register_ui("overworld", UIOverworld)
        self.game.r_uin.register_ui("cinematic", UICinematic)

        self.game.r_uin.register_ui("battle", UIBattle)

        self.game.r_uin.register_ui("mainmenu", UIMainMenu)

        self.game.r_uin.register_ui("monview", UIMonView)
        self.game.r_uin.register_ui("moninspect", UIMonInspect)

        self.game.r_uin.register_ui("vsmain", UIVsMain)

        self.game.r_uin.register_ui("save", UISave)
        pass

    def update(self, time, frame_time):
        return self.lock

    @property
    def priority(self):
        return 0
