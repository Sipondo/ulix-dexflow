from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Halfdmg(BaseMoveEffect):
    def after_action(self):
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, rel_dmg=0.5))
        return True
