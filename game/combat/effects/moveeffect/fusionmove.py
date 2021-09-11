from .basemoveeffect import BaseMoveEffect
from ..environmenteffect.fusioneffect import FusionEffect


class Fusionmove(BaseMoveEffect):
    def before_action(self):
        global_effects = self.scene.get_global_effects()
        if fusion_effect := [x for x in global_effects if x.name == "Fusioneffect"]:
            if fusion_effect[0].move != self.move.name:
                self.move.power *= 2
            return True

    def after_action(self):
        self.scene.add_effect(FusionEffect(self.scene, self.move.name))
        return True
