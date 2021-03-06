from .baseeffect import BaseEffect
from .leveleffect import LevelEffect


class ExperienceEffect(BaseEffect):
    spd_on_action = 90

    def __init__(self, scene, target, fainted, cont=None):
        super().__init__(scene)
        self.target = target
        self.fainted = fainted
        if self.scene.board.get_actor(self.target).level > 99:
            self.amount = 0
        else:
            if cont is None:
                self.amount = self.get_flat_experience_reward()
            else:
                self.amount = cont
        self.cont = False if cont is None else True

    def get_flat_experience_reward(self):
        b_type = 1
        if self.scene.battle_type == "trainer":
            b_type = 1.5
        base_exp = float(self.fainted.data["baseexp"])
        # if mon is holding lucky egg
        lucky_egg = 1
        # affection mod
        aff = 1
        level_fainted = self.fainted.level
        # roto powers ???
        power = 1
        exp_share = 1
        # if traded 1.5
        trade = 1
        # if past evolution level 1.2
        nevolved = 1
        return int(
            b_type
            * base_exp
            * lucky_egg
            * aff
            * level_fainted
            * power
            * trade
            * nevolved
            // (7 * exp_share)
        )

    def get_ev_reward(self):
        ev_reward = self.fainted.data["effortpoints"]
        evs = list(map(lambda x: int(x), ev_reward.split(",")))
        return evs

    def on_action(self):
        actor = self.scene.board.get_actor(self.target)
        if self.cont:
            self.scene.board.no_skip(
                "", particle="",
            )
        else:
            self.scene.board.no_skip(
                f"{self.scene.board.get_actor(self.target).name} gained {self.amount} experience",
                particle="",
            )
            # EV reward here (don't repeat after levelup)
            actor.gain_evs(self.get_ev_reward())

            # after EV gain, check if the HP has increased
            current_hp = self.scene.board.get_data(self.target).current_hp
            old_max_hp = self.scene.board.get_data(self.target).max_hp
            new_max_hp = actor.stats[0]
            self.scene.board.get_data(self.target).max_hp = new_max_hp
            self.scene.board.set_hp(self.target, current_hp + (new_max_hp - old_max_hp))

        current_xp = self.scene.board.get_data(self.target).current_exp
        xp_needed = actor.level_xp - current_xp
        if xp_needed <= self.amount:
            self.amount -= xp_needed
            self.scene.board.set_exp(self.target, current_xp + xp_needed)
            self.scene.add_effect(LevelEffect(self.scene, self.target))
            self.scene.add_effect(
                ExperienceEffect(
                    self.scene, self.target, self.fainted, cont=self.amount
                )
            )
        else:
            self.scene.board.set_exp(self.target, current_xp + self.amount)
        return True, False, False
