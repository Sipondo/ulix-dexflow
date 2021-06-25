from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Freezeflinch(BaseMoveEffect):
    def after_move(self):
        if self.scene.board.random_roll() < self.move.chance:
            ApplyStatus(self.scene, statuseffect.FREEZE, self.move.user, self.move.target).apply()
        if self.scene.board.random_roll() < self.move.chance:
            ApplyStatus(self.scene, statuseffect.FLINCH, self.move.user, self.move.target).apply()
