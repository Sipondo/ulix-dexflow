from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Selfspdefup2(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Special Defense", 2).apply()
