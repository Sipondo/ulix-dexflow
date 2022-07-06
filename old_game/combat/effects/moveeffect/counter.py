from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Counter(BaseMoveEffect):
    def __init__(self, scene, move, mod):
        super().__init__(scene, move)
        self.mod = float(mod)
        self.damage = 0
        self.fail = True

    def on_hit(self, move):
        if move.move_cat == "Physical" or move.move_cat == "Special":
            self.fail = False

    def on_damage(self, damage):
        self.damage = int(damage*self.mod)

    def before_action(self):
        self.move.fail = self.damage < 1 or self.fail
        return False, False, False

    def after_action(self):
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, abs_dmg=self.damage))
        return True, False, False
