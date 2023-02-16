from ulivy.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.damageeffect import DamageEffect


class Struggle(BaseMoveEffect):
    def after_action(self):
        DamageEffect(self.scene, self.move.user, rel_dmg=0.25)
        return True, False, False

