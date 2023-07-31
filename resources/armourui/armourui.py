from ulivy.manager.pluginmanager import Plugin

from resources.armourui.ui.uioverworld import UIOverworld

class Armourui(Plugin):
    def pre_load(self, **kwargs):
        print("ARMOURUI PRE")
        pass

    def post_load(self, **kwargs):
        print("ARMOURUI POST")
        self.game.r_uin.register_ui("overworld", UIOverworld)
        pass

    def update(self, time, frame_time):
        return self.lock

    @property
    def priority(self):
        return 0
