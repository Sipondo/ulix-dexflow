from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Sethpequal(BaseMoveEffect):
    def before_action(self):
        user_hp = self.scene.board.get_data(self.move.user).current_hp
        target_hp = self.scene.board.get_data(self.move.target).current_hp
        if target_hp <= user_hp:
            self.move.fail = True
        return False, False, False

    def after_action(self):
        user_hp = self.scene.board.get_data(self.move.user).current_hp
        target_hp = self.scene.board.get_data(self.move.target).current_hp
        dmg = target_hp-user_hp
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, abs_dmg=dmg))
        return True, False, False
