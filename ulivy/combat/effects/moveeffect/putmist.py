from ulivy.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from ulivy.combat.effects import statuseffect


class Putmist(BaseMoveEffect):
    def after_action(self):
        if self.scene.board.random_roll(self.move.chance):
            ApplyStatus(
                self.scene, statuseffect.MIST, self.move.user, self.move.user
            ).apply()
        return True, False, False
