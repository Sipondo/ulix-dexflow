from game.combat.effects.partialeffect.basepartialeffect import BasePartialEffect
from game.combat.effects.statmodeffect import StatModEffect


class StatChange(BasePartialEffect):
    type = "Stat"

    def __init__(self, scene, target, stat_name, mod, abs_mod=None):
        super().__init__(scene)
        self.target = target
        self.name = stat_name
        self.modifier = mod
        self.absolute_modifier = abs_mod

    def apply(self):
        for effect in self.scene.get_effects_on_target(self.target):
            if effect.on_stat_change(self.target):
                return
        target_effects = self.scene.get_effects_on_target(self.target)
        if effects := [x for x in target_effects if x.name == "Statmod"]:
            for effect in effects:
                effect.update(self.name, self.modifier, self.absolute_modifier)
        else:
            effect = StatModEffect(self.scene, self.target)
            self.scene.add_effect(effect)
            effect.update(self.name, self.modifier, self.absolute_modifier)

    def before_start(self):
        self.apply()
        return True, False, False

    def before_action(self):
        self.apply()
        return True, False, False

    def on_action(self):
        self.apply()
        return True, False, False

    def after_action(self):
        self.apply()
        return True, False, False

    def before_end(self):
        self.apply()
        return True, False, False

    def on_faint(self, target):
        return self.target == target, False, False
