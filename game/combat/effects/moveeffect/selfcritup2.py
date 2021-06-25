from .basemoveeffect import BaseMoveEffect
from game.combat.effects.critmodeffect import CritModEffect


class Selfcritup2(BaseMoveEffect):
    def after_move(self):
        user_effects = self.scene.get_effects_on_target(self.move.user)
        if effects := [x for x in user_effects if x.name == "Critmod"]:
            effects[0].update(2)
            return
        effect = CritModEffect(self.scene, self.move.user, 2)
        self.scene.add_effect(effect)

