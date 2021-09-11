from .baseabilityeffect import BaseAbilityEffect
from ..partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Stench(BaseAbilityEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.target = target

    def after_action(self, move):
        return ApplyStatus(self.scene, statuseffect.FLINCH, move.user, move.target).apply()
