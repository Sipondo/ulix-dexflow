from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Enemyacc(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = int(mod)

    def after_move(self):
        StatChange(self.scene, self.move.target, "Accuracy", self.mod).apply()
        return True
