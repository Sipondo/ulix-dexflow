from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange

import random


class Selfrandomstat(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = int(mod)

    def after_move(self):
        stat = random.choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed", "Accuracy", "Evasion"])
        StatChange(self.scene, self.move.user, stat, self.mod).apply()
