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
