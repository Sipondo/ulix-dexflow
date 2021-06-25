from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange
from game.combat.effects.curleffect import CurlEffect


class Defcurl(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Defense", 1).apply()
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if "Curl" not in [x.name for x in target_effects]:
            self.scene.add_effect(CurlEffect(self.scene, self.target))
