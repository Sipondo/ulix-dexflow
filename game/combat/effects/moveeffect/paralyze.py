from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Paralyze(BaseMoveEffect):
    def before_move(self):
        if self.move.name == "Body slam":
            target_effects = self.scene.get_effects_on_target(self.move.target)
            if "Minimize" in [x.name for x in target_effects]:
                self.move.perfect_accuracy = True
                self.move.power *= 2
        return True

    def after_move(self):
        return ApplyStatus(self.scene, statuseffect.PARALYSIS, self.move.user, self.move.target).apply()

