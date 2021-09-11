from .basemoveeffect import BaseMoveEffect
from game.combat.effects import statuseffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus


class Fakeout(BaseMoveEffect):
    def before_action(self):
        _round = self.scene.board.get_active_round(self.move.user[0])
        if self.scene.round - _round > 1:
            return False
        return True

    def after_action(self):
        ApplyStatus(self.scene, statuseffect.FLINCH, self.move.user, self.move.target).apply()
        return True
