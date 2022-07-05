from .basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from ulivy.combat.effects import statuseffect


class Paralyze(BaseMoveEffect):
    def before_action(self):
        if self.move.name == "Body slam":
            target_effects = self.scene.get_effects_on_target(self.move.target)
            if "Minimize" in [x.name for x in target_effects]:
                self.move.perfect_accuracy = True
                self.move.power *= 2
        return False, False, False

    def after_action(self):
        if self.scene.board.random_roll(self.move.chance):
            ApplyStatus(
                self.scene, statuseffect.PARALYSIS, self.move.user, self.move.target
            ).apply()
        return True, False, False

