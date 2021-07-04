from .combatboard import CombatBoard
from .effects.genericeffect import GenericEffect
from .effects.fainteffect import FaintEffect

import math
import pandas as pd


class PokeBoard(CombatBoard):
    def __init__(self, scene):
        super().__init__(scene)
        # self.legal = pd.DataFrame(columns=["Pokemon", "Team", "Action", "Legal"])
        self.switch = []

    def copy(self):
        newstate = PokeBoard(self.scene)
        newstate.from_board(self)
        newstate.switch = self.switch.copy()
        # newstate.legal = self.legal.copy()
        return newstate

    def first_init(self, *teams):
        for team in teams:
            self.teams.append([(x, x.current_hp) for x in team])
            self.actives.append((0, 0))
            self.switch.append(False)

    def inflict_damage(self, target, damage):
        x, hp = self.teams[target[0]][target[1]]
        damage = min(hp, damage)
        hp -= damage
        self.teams[target[0]][target[1]] = (x, hp)
        x.current_hp = hp
        for effect in self.scene.get_effects_on_target(target):
            effect.on_damage(damage)
        if self.teams[target[0]][target[1]][1] < 1:
            self.scene.add_effect(FaintEffect(self.scene, target))

    def inflict_status(self, status, user, target):
        for effect in self.scene.get_effects_on_target(target):
            if effect.on_status(target):
                return
        status_effect = status(self.scene, user, target)
        self.scene.add_effect(status_effect)
        if status_effect.apply_narration != "":
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.get_actor(target).name} {status_effect.apply_narration}!",
                    particle=status_effect.particle,
                )
            )

    def set_active(self, new_active):
        self.actives[new_active[0]] = (new_active[1], self.scene.round)

    def is_active(self, target):
        return target[1] == self.actives[target[0]][0]

    def get_active(self, team):
        return self.actives[team][0]

    def get_active_round(self, team):
        return self.actives[team][1]

    @property
    def actor_1(self):
        if self.actives[0][0] == -1:
            return -1
        return self.teams[0][self.actives[0][0]]

    @property
    def actor_2(self):
        if self.actives[1][0] == -1:
            return -1
        return self.teams[1][self.actives[1][0]]
