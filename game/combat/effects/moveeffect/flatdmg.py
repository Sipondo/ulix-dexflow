from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Flatdmg(BaseMoveEffect):
    def __init__(self, scene, move, dmg):
        super().__init__(scene, move)
        self.dmg = int(dmg)

    def after_move(self):
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, abs_dmg=self.dmg))
        return True
