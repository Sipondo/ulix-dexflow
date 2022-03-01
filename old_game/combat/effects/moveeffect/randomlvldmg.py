from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect

import random
import math


class Randomlvldmg(BaseMoveEffect):
    def after_action(self):
        level = self.scene.board.get_actor(self.move.user).level
        damage = math.ceil(level * (random.randint(0, 100) + 50) / 100)
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, abs_dmg=damage))
        return True, False, False
