from .basemoveeffect import BaseMoveEffect
from game.combat.effects.statuseffect.minimizeeffect import MinimizeEffect


class Minimize(BaseMoveEffect):
    def after_move(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if "Minimize" not in [x.name for x in target_effects]:
            self.scene.add_effect(MinimizeEffect(self.scene, self.target))
