from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Flinch(BaseMoveEffect):
    def after_action(self):
        return ApplyStatus(self.scene, statuseffect.FLINCH, self.move.user, self.move.target).apply()
