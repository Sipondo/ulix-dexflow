from .basemoveeffect import BaseMoveEffect
from game.combat.effects import statuseffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus


class Snore(BaseMoveEffect):
    def before_action(self):
        user_effects = self.scene.get_effects_on_target(self.move.user)
        if sleep_effects := [x for x in user_effects if x.name == "Sleep"]:
            sleep_effects[0].skip = True
        return False, False, False

    def after_action(self):
        return ApplyStatus(self.scene, statuseffect.FLINCH, self.move.user, self.move.target).apply()


