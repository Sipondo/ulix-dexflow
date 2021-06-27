from .basemoveeffect import BaseMoveEffect
from game.combat.effects import statuseffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus


class Antiminimize(BaseMoveEffect):
    def before_move(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if "Minimize" in [x.name for x in target_effects]:
            self.move.perfect_accuracy = True
            self.move.power *= 2
            return True

    def after_move(self):
        ApplyStatus(self.scene, self.move.target, self.move.user, statuseffect.FLINCH).apply()

