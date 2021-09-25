from .basemoveeffect import BaseMoveEffect
from game.combat.effects.critchanceeffect import CritChanceEffect
from game.combat.effects.statuseffect.focusenergyeffect import FocusEnergyEffect


class Focusenergy(BaseMoveEffect):
    def before_action(self):
        if "FocusEnergy" in [eff.name for eff in self.scene.get_effects_on_target(self.move.user)]:
            self.move.fail = True
            return True, False, False
        return False, False, False

    def after_action(self):
        user_effects = self.scene.get_effects_on_target(self.move.user)
        if effects := [x for x in user_effects if x.name == "Critmod"]:
            effects[0].update(2)
            self.scene.add_effect(FocusEnergyEffect(self.scene, self.move.user))
            return True, False, False
        effect = CritChanceEffect(self.scene, self.move.user, 2)
        self.scene.add_effect(effect)
        self.scene.add_effect(FocusEnergyEffect(self.scene, self.move.user))
        return True, False, False
