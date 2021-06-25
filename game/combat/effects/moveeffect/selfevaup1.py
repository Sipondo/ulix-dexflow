from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Selfevaup1(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Evasion", 1).apply()
