from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Enemydef(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = int(mod)

    def after_action(self):
        if self.scene.board.random_roll(self.move.chance):
            StatChange(self.scene, self.move.target, "Defense", self.mod).apply()
        return True, False, False
