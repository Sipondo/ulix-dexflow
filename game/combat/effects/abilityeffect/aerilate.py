from .baseabilityeffect import BaseAbilityEffect


class Aerilate(BaseAbilityEffect):
    name = "Aerilate"

    def before_action(self):
        if self.active:
            if self.scene.current_action.user == self.holder:
                current_effect = self.scene.current_action_effect
                if current_effect.type == "NORMAL":
                    current_effect.type = "FLYING"
                    current_effect.power = int(current_effect.power * 1.2)
