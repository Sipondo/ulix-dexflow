from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Freeze(BaseMoveEffect):
    def after_move(self):
        ApplyStatus(self.scene, statuseffect.FREEZE, self.move.user, self.move.target).apply()
        return True
