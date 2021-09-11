from .basemoveeffect import BaseMoveEffect
from ..basestatchangeeffect import *


class Swapbaseatkdef(BaseMoveEffect):
    def after_action(self):
        user_stats = self.scene.board.get_actor(self.move.target).stats
        target_stats = self.scene.board.get_actor(self.move.target).stats

        for stat in ("Attack", "Defense"):
            if swap_effects := [x for x in self.scene.get_effects_on_target(self.move.user) if x.name == "Statchange"]:
                swap_effects[0].update(stat, target_stats[STATMAP[stat]])
            else:
                user_swap_effect = BaseStatChangeEffect(self.scene, self.move.user)
                user_swap_effect.update(stat, target_stats[STATMAP[stat]])
                self.scene.add_effect(user_swap_effect)

            if swap_effects := [x for x in self.scene.get_effects_on_target(self.move.target) if x.name == "Statchange"]:
                swap_effects[0].update(stat, user_stats[STATMAP[stat]])
            else:
                target_swap_effect = BaseStatChangeEffect(self.scene, self.move.target)
                target_swap_effect.update(stat, user_stats[STATMAP[stat]])
                self.scene.add_effect(target_swap_effect)
        return True, False, False
