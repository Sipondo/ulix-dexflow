from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Burnflinch(BaseMoveEffect):
    def after_move(self):
        ApplyStatus(self.scene, statuseffect.BURN, self.move.user, self.move.target).apply()
        if self.scene.board.random_roll() < self.move.chance:
            ApplyStatus(self.scene, statuseffect.FLINCH, self.move.user, self.move.target).apply()
