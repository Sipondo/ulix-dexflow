from .baseeffect import BaseEffect
from .leveleffect import LevelEffect


class ExperienceEffect(BaseEffect):
    def __init__(self, scene, target, exp_amount, ev_reward=None, cont=False):
        super().__init__(scene)
        self.spd_on_action = 100
        self.target = target
        self.amount = exp_amount
        self.ev_reward = ev_reward
        self.cont = cont

    def on_action(self):
        # TODO EV reward
        if self.cont:
            self.scene.board.no_skip(
                "",
                particle="",
            )
        else:
            self.scene.board.no_skip(
                f"{self.scene.board.get_actor(self.target).name} gained {self.amount} experience",
                particle="",
            )
        actor = self.scene.board.get_actor(self.target)
        xp_needed = actor.level_xp - actor.current_xp
        if xp_needed <= self.amount:
            self.amount -= xp_needed
            actor.current_xp += xp_needed
            self.scene.add_effect(LevelEffect(self.scene, self.target))
            self.scene.add_effect(
                ExperienceEffect(self.scene, self.target, self.amount, cont=True)
            )
        else:
            actor.current_xp += self.amount

        return True, False, False
