from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Growth(BaseMoveEffect):
    def after_action(self):
        mod = 1
        global_effects = self.scene.get_global_effects()
        if "Sun" in [x.name for x in global_effects]:
            mod = 2
        StatChange(self.scene, self.move.user, "Attack", mod).apply()
        StatChange(self.scene, self.move.user, "Defense", mod).apply()
        return True
