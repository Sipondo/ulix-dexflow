from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Sethpequal(BaseMoveEffect):
    def before_action(self):
        user_hp = self.scene.board.get_data(self.move.user)["hp"]
        target_hp = self.scene.board.get_data(self.move.target)["hp"]
        if target_hp <= user_hp:
            return False

    def after_action(self):
        user_hp = self.scene.board.get_data(self.move.user)["hp"]
        target_hp = self.scene.board.get_data(self.move.target)["hp"]
        dmg = target_hp-user_hp
        self.scene.add_effect(DamageEffect(self.scene, self.move.target, abs_dmg=dmg))
        return True
