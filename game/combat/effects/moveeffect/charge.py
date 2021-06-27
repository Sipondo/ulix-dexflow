from .basemoveeffect import BaseMoveEffect
from game.combat.effects.statuseffect.chargeeffect import ChargeEffect


class Charge(BaseMoveEffect):
    def after_move(self):
        self.scene.add_effect(ChargeEffect(self.scene, self.move.target))

