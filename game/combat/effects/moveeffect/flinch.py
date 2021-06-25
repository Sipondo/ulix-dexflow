from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Flinch(BaseMoveEffect):
    def after_move(self):
        if self.move.move_cat == "Status":
            ApplyStatus(self.scene, statuseffect.FLINCH, self.move.user, self.move.target).apply()
            return
        if self.scene.board.random_roll() < self.move.chance:
            ApplyStatus(self.scene, statuseffect.FLINCH, self.move.user, self.move.target).apply()
