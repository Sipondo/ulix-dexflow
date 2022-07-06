from .baseabilityeffect import BaseAbilityEffect
from ..partialeffect.statchange import StatChange


class Angerpoint(BaseAbilityEffect):
    name = "Anger Point"

    def on_crit(self, target):
        if self.active:
            if target == self.holder:
                self.scene.add_effect(StatChange(self.scene, self.holder, "Attack", 0, abs_mod=6))

