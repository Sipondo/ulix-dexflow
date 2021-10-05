from game.combat.effects.baseeffect import BaseEffect

import abc


class BaseAbilityEffect(BaseEffect, abc.ABC):
    type = "AbilityEffect"

    def __init__(self, scene, holder):
        print("A NEW ABILITY!")
        super().__init__(scene)
        self.holder = holder
        self.active = False

    def activate(self):
        self.active = True
        self.on_activate()

    def deactivate(self):
        self.active = False
        self.on_deactivate()

    def on_activate(self):
        """Happens when the holder of the ability is set to active"""

    def on_deactivate(self):
        """Happens when the holder of the ability is set to inactive"""

    def on_send_out(self, new_target):
        if new_target == self.holder:
            self.activate()

    def on_switch(self, target_old, target_new):
        if target_new == self.holder:
            self.activate()
        if target_old == self.holder:
            self.deactivate()

    def on_faint(self, target):
        if target == self.holder:
            self.deactivate()
