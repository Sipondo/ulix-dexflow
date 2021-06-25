from .combatboard import CombatBoard
from .effects.genericeffect import GenericEffect

import math


class PokeBoard(CombatBoard):
    def __init__(self, scene):
        super().__init__(scene)

    def copy(self):
        newstate = PokeBoard(self.scene)
        newstate.from_board(self)
        return newstate

    def first_init(self, *teams):
        for team in teams:
            self.teams.append([(x, math.floor(x.stats[0]*x.starting_hp)) for x in team])
            self.actives.append((0, 0))

    def inflict_damage(self, target, damage):
        x, hp = self.teams[target[0]][target[1]]
        hp -= damage
        self.teams[target[0]][target[1]] = (x, hp)

    def inflict_status(self, status, user, target):
        for effect in self.scene.get_effects_on_target(target):
            if not effect.on_status(target):
                return
        status_effect = status(self.scene, user, target)
        self.scene.add_effect(status_effect)
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

    def get_weather_acc_change(self, weather, move_name):
        return self.scene.game.m_pbs.get_weather_acc_change(weather, move_name)

    @property
    def actor_1(self):
        return self.teams[0][self.actives[0][0]]

    @property
    def actor_2(self):
        return self.teams[1][self.actives[0][0]]
