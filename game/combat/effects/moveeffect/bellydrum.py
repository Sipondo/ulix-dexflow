from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange
from game.combat.effects.damageeffect import DamageEffect


class Bellydrum(BaseMoveEffect):
    def before_action(self):
        if self.scene.board.get_relative_hp(self.move.user) <= 0.5:
            return False

    def after_action(self):
        self.scene.add_effect(DamageEffect(self.scene, self.move.user, rel_dmg=0.5))
        StatChange(self.scene, self.move.user, "Attack", 0, abs_mod=6).apply()
        return True
