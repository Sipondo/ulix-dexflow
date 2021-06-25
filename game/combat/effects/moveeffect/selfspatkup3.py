from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Selfspatkup3(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Special Attack", 3).apply()
