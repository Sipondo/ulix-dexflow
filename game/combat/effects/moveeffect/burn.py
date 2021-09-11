from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Burn(BaseMoveEffect):
    def after_action(self):
        return ApplyStatus(self.scene, statuseffect.BURN, self.move.user, self.move.target).apply()

