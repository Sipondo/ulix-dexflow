from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.damageeffect import DamageEffect


class Struggle(BaseMoveEffect):
    def after_action(self):
        DamageEffect(self.scene, self.move.user, rel_dmg=0.25)
        return True

