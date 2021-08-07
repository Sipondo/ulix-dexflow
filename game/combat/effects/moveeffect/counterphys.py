from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Counterphys(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = int(mod)
        self.damage = 0
        self.fail = True

    def on_hit(self, move):
        if move.move_cat == "Physical":
            self.fail = False

    def on_damage(self, damage):
        self.damage = int(damage*self.mod)

    def before_move(self):
        if self.damage < 1:
            return False
        return not self.fail

    def after_move(self):
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, abs_dmg=self.damage))
        return True
