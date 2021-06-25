from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Selfatkup2(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Attack", 2).apply()
