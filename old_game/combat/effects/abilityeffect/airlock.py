from .baseabilityeffect import BaseAbilityEffect


class Airlock(BaseAbilityEffect):
    name = "Air lock"

    def on_activate(self):
        for effect in self.scene.get_effects_by_type("Weather"):
            effect.active = False

    def on_deactivate(self):
        for effect in self.scene.get_effects_by_type("Weather"):
            effect.active = True
