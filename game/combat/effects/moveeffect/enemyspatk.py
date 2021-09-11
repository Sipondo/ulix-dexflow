from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Enemyspatk(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = int(mod)

    def after_action(self):
        StatChange(self.scene, self.move.target, "Special Attack", self.mod).apply()
        return True, False, False
