from .basemoveeffect import BaseMoveEffect
from ..statmodeffect import StatModEffect
from ..genericeffect import GenericEffect


class Swapallstats(BaseMoveEffect):
    def after_action(self):
        if statmod_effect := [
            x
            for x in self.scene.get_effects_on_target(self.move.user)
            if x.name == "Statmod"
        ]:
            user_stat_mods = statmod_effect
        else:
            user_stat_mods = StatModEffect(self.scene, self.move.user)
        if statmod_effect := [
            x
            for x in self.scene.get_effects_on_target(self.move.target)
            if x.name == "Statmod"
        ]:
            target_stat_mods = statmod_effect
        else:
            target_stat_mods = StatModEffect(self.scene, self.move.target)
        for stat in (
            "Attack",
            "Defense",
            "Special Attack",
            "Special Defense",
            "Speed",
            "Accuracy",
            "Evasion",
        ):
            user_stat = user_stat_mods.stats[stat]
            target_stat = target_stat_mods.stats[stat]
            user_stat_mods.update(stat, 0, abs_change=target_stat)
            user_stat_mods.update(stat, 0, abs_change=user_stat)
        self.scene.add_effect(
            GenericEffect(self.scene, "The pokemon swapped stat changes")
        )
        return True, False, False
