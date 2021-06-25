from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Selfspatkspdefspeedup1(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Special Attack", 1).apply()
        StatChange(self.scene, self.move.user, "Special Defense", 1).apply()
        StatChange(self.scene, self.move.user, "Speed", 1).apply()
