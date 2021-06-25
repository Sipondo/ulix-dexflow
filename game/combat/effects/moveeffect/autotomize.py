from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange
from game.combat.effects.autotomizeeffect import AutotomizeEffect


class Autotomize(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Speed", 2).apply()
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if "Autotomize" not in [x.name for x in target_effects]:
            self.scene.add_effect(AutotomizeEffect(self.scene, self.move.target))


