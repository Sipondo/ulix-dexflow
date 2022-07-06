from .baseabilityeffect import BaseAbilityEffect
from ..statuseffect import Flinch
from ..partialeffect.applystatuseffect import ApplyStatus


class Stench(BaseAbilityEffect):
    name = "Stench"

    def after_action(self):
        if self.active:
            if self.scene.current_action.user == self.holder:
                if self.scene.board.random_roll(0.1):
                    ApplyStatus(self.scene, Flinch, self.holder, self.scene.current_action.target)
