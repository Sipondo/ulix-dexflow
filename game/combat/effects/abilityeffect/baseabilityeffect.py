from game.combat.effects.baseeffect import BaseEffect

import abc


class BaseAbilityEffect(BaseEffect, abc.ABC):
    type = "AbilityEffect"

    def __init__(self, scene, holder):
        print("A NEW ABILITY!")
        super().__init__(scene)
        self.holder = holder
