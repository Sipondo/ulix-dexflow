from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Selfatkdefdown1(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Attack", -1).apply()
        StatChange(self.scene, self.move.user, "Defense", -1).apply()
