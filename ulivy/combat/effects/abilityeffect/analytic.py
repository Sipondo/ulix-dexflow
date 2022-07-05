from .baseabilityeffect import BaseAbilityEffect


class Analytic(BaseAbilityEffect):
    name = "Analytic"

    def before_start(self):
        if self.active:
            action, effect = self.scene.get_action_effect(self.holder)
            target_action_effect = self.scene.get_action_effect(action.target)
            if self.scene.action_effects.index((action, effect)) > self.scene.action_effects.index(target_action_effect):
                effect.power = int(effect.power * 1.3)
