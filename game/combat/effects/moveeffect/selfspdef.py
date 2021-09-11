from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Selfspdef(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = int(mod)

    def after_action(self):
        StatChange(self.scene, self.move.user, "Special Defense", self.mod).apply()
        return True
