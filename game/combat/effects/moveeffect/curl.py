from .basemoveeffect import BaseMoveEffect
from game.combat.effects.statuseffect.curleffect import CurlEffect


class Curl(BaseMoveEffect):
    def after_action(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if "Curl" not in [x.name for x in target_effects]:
            self.scene.add_effect(CurlEffect(self.scene, self.target))
        return True, False, False
