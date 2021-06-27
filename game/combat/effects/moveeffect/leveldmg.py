from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Leveldmg(BaseMoveEffect):
    def after_move(self):
        level = self.scene.board.get_actor(self.move.user).level
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, abs_dmg=level))
