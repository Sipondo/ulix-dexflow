from ulivy.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from ..basestatchangeeffect import *


class Avgbaseatk(BaseMoveEffect):
    def after_action(self):
        if self.scene.board.random_roll(self.move.chance):
            user_stats = self.scene.board.get_actor(self.move.target).stats
            target_stats = self.scene.board.get_actor(self.move.target).stats

            for stat in ("Attack", "Special Attack"):
                avg_stat = (
                    user_stats[STATMAP[stat]] + target_stats[STATMAP[stat]]
                ) // 2
                if swap_effects := [
                    x
                    for x in self.scene.get_effects_on_target(self.move.user)
                    if x.name == "Statswap"
                ]:
                    swap_effects[0].update(stat, avg_stat)
                else:
                    user_swap_effect = BaseStatChangeEffect(self.scene, self.move.user)
                    user_swap_effect.update(stat, avg_stat)
                    self.scene.add_effect(user_swap_effect)

                if swap_effects := [
                    x
                    for x in self.scene.get_effects_on_target(self.move.target)
                    if x.name == "Statswap"
                ]:
                    swap_effects[0].update(stat, avg_stat)
                else:
                    target_swap_effect = BaseStatChangeEffect(
                        self.scene, self.move.target
                    )
                    target_swap_effect.update(stat, avg_stat)
                    self.scene.add_effect(target_swap_effect)
        return True, False, False
