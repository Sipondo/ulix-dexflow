from .basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.partialeffect.statchange import StatChange
from ulivy.combat.effects.damageeffect import DamageEffect


class Bellydrum(BaseMoveEffect):
    def before_action(self):
        if self.scene.board.get_relative_hp(self.move.user) <= 0.5:
            return False, False, False
        return True, True, False

    def after_action(self):
        self.scene.add_effect(DamageEffect(self.scene, self.move.user, rel_dmg=0.5))
        self.scene.add_effect(
            StatChange(self.scene, self.move.user, "Attack", 0, abs_mod=6)
        )
        return True, False, False
