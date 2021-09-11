from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange

import random


class Enemyrandomstat(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = int(mod)

    def after_action(self):
        stat = random.choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed", "Accuracy", "Evasion"])
        StatChange(self.scene, self.move.target, stat, self.mod).apply()
        return True
