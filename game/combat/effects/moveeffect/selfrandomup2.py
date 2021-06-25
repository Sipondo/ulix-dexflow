from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange

import random


class Selfrandomup2(BaseMoveEffect):
    def after_move(self):
        stat = random.choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed", "Accuracy", "Evasion"])
        StatChange(self.scene, self.move.user, stat, 2).apply()
