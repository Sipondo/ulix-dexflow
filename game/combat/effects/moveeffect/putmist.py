from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Putmist(BaseMoveEffect):
    def after_move(self):
        return ApplyStatus(self.scene, statuseffect.MIST, self.move.user, self.move.user).apply()
