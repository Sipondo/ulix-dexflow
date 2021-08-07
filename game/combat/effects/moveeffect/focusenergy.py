from .basemoveeffect import BaseMoveEffect
from game.combat.effects.critchanceeffect import CritChanceEffect


class Focusenergy(BaseMoveEffect):
    def after_move(self):
        user_effects = self.scene.get_effects_on_target(self.move.user)
        if effects := [x for x in user_effects if x.name == "Critmod"]:
            effects[0].update(2)
            return True
        effect = CritChanceEffect(self.scene, self.move.user, 2)
        self.scene.add_effect(effect)
        return True
