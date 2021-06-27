from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Sethpequal(BaseMoveEffect):
    def before_move(self):
        user_hp = self.scene.board.get_hp(self.move.user)
        target_hp = self.scene.board.get_hp(self.move.target)
        if target_hp <= user_hp:
            return False

    def after_move(self):
        user_hp = self.scene.board.get_hp(self.move.user)
        target_hp = self.scene.board.get_hp(self.move.target)
        dmg = target_hp-user_hp
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, abs_dmg=dmg))
