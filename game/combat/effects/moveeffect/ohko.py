from .basemoveeffect import BaseMoveEffect
from ..damageeffect import DamageEffect


class Ohko(BaseMoveEffect):
    def before_move(self):
        user_level = self.scene.board.get_actor(self.move.user).level
        target_level = self.scene.board.get_actor(self.move.target).level
        if user_level < target_level:
            return False
        self.move.acc += user_level-target_level
        self.move.abs_acc = True

    def after_move(self):
        damage = self.scene.board.get_actor(self.move.target).stats[0]
        self.scene.add_effect(
            DamageEffect(self.scene, self.move.target, abs_dmg=damage)
        )
        return True
