from .basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.partialeffect.statchange import StatChange


class Selfatk(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = int(mod)

    def after_action(self):
        if self.scene.board.random_roll(self.move.chance):
            StatChange(self.scene, self.move.user, "Attack", self.mod).apply()
        return True, False, False
