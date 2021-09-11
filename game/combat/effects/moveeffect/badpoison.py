from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Badpoison(BaseMoveEffect):
    def after_action(self):
        return ApplyStatus(self.scene, statuseffect.BADPOISON, self.move.user, self.move.target).apply()

