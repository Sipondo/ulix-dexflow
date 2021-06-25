from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange
from game.combat.effects.chargeeffect import ChargeEffect


class Charge(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Special Defense", 1).apply()
        self.scene.add_effect(ChargeEffect(self.scene, self.move.target))

