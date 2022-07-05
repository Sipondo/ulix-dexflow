from .basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from ulivy.combat.effects import statuseffect


class Flinch(BaseMoveEffect):
    def after_action(self):
        if self.scene.board.random_roll(self.move.chance):
            ApplyStatus(
                self.scene, statuseffect.FLINCH, self.move.user, self.move.target
            ).apply()
        return True, False, False
