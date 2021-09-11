from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Attract(BaseMoveEffect):
    def after_action(self):
        ApplyStatus(self.scene, statuseffect.INFATUATION, self.move.user, self.move.target).apply()
        return True, False, False
