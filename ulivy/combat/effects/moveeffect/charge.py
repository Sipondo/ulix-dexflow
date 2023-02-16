from .basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.statuseffect.chargeeffect import ChargeEffect


class Charge(BaseMoveEffect):
    def after_action(self):
        if self.scene.board.random_roll(self.move.chance):
            self.scene.add_effect(ChargeEffect(self.scene, self.move.target))
        return True, False, False

