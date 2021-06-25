from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Paraburnze(BaseMoveEffect):
    def after_move(self):
        if self.scene.board.random_roll() < self.move.chance:
            rnd = self.scene.board.random_roll
            if rnd < 1/3:
                ApplyStatus(self.scene, statuseffect.PARALYSIS, self.move.user, self.move.target).apply()
            elif rnd < 2/3:
                ApplyStatus(self.scene, statuseffect.BURN, self.move.user, self.move.target).apply()
            else:
                ApplyStatus(self.scene, statuseffect.FREEZE, self.move.user, self.move.target).apply()
