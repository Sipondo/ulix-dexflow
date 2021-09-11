from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Poison(BaseMoveEffect):
    def after_action(self):
        return ApplyStatus(self.scene, statuseffect.POISON, self.move.user, self.move.target).apply()
