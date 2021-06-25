from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Burn(BaseMoveEffect):
    def after_move(self):
        if self.move.move_cat == "Status":
            ApplyStatus(self.scene, statuseffect.BURN, self.move.user, self.move.target).apply()
            return True
        if self.scene.board.random_roll() < self.move.chance:
            ApplyStatus(self.scene, statuseffect.BURN, self.move.user, self.move.target).apply()

    # TODO if move is fusion flare, double the power of the next fusion bolt this round
