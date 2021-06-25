from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Attract(BaseMoveEffect):
    def before_move(self):
        # TODO gender check
        return True

    def after_move(self):
        ApplyStatus(self.scene, statuseffect.INFATUATION, self.move.user, self.move.target).apply()
