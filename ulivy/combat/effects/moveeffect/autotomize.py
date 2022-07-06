from .basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.statuseffect.autotomizeeffect import AutotomizeEffect


class Autotomize(BaseMoveEffect):
    def after_action(self):
        if self.scene.board.random_roll(self.move.chance):
            target_effects = self.scene.get_effects_on_target(self.move.target)
            if "Autotomize" not in [x.name for x in target_effects]:
                self.scene.add_effect(AutotomizeEffect(self.scene, self.move.target))
                return True, False, False
        return True, False, False

