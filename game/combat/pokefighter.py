from .combatfighter import CombatFighter

import numpy as np
import numbers


class PokeFighter(CombatFighter):
    def __init__(self, game, scene, fighter):
        super().__init__(game, scene, fighter)

        if isinstance(fighter, str):
            fighter = self.game.m_pbs.get_fighter_by_name(fighter)
            self.level = 5
            self.init_stats(fighter)
            self.current_hp = self.stats[0]
            self.current_xp = 0
        elif isinstance(fighter, numbers.Number):
            fighter = self.game.m_pbs.get_fighter(fighter)
            self.level = 5
            self.init_stats(fighter)
            self.current_hp = self.stats[0]
            self.current_xp = 0

        self.data = fighter.copy()

        try:
            self.level = fighter.level
        except AttributeError:
            self.level = 5

        try:
            self.stats_base = fighter.stats_base
            self.stats_reward = fighter.stats_reward
            self.stats_IV = fighter.stats_IV
            self.stats_EV = fighter.stats_EV
            self.nature = fighter.nature
        except AttributeError:
            self.init_stats(fighter)

        try:
            self.current_hp = fighter.current_hp
        except AttributeError:
            self.current_hp = self.stats[0]

        try:
            self.ability = self.data.ability
        except AttributeError:
            self.ability = self.data.abilities[0]
        try:
            self.current_xp = fighter.current_xp
            self.level_xp = fighter.level_xp
        except AttributeError:
            self.current_xp = 0
            self.level_xp = 0
            self.get_level_exp()

        if "actions" not in fighter:
            self.moves = fighter.moves
            l = self.moves.split(",")
            self.learnset = [tuple(l[i : i + 2]) for i in range(0, len(l), 2)]

            l = [(x, y) for x, y in reversed(self.learnset) if int(x) < self.level]
            k = [y for x, y in l]
            l = [l[i] for i in range(len(l)) if l[i] not in k[:i]]
            self.actions = [self.game.m_pbs.get_move_by_name(y) for x, y in l][:4]
        else:
            self.actions = [
                self.game.m_pbs.get_move(x) for x in self.data["actions"]
            ]

        try:
            self.status = fighter.status
        except AttributeError:
            self.status = None

        self.starting_hp = self.current_hp
        self.type1 = str(fighter["type1"])
        self.type2 = str(fighter["type2"])

        # Init actions starting from id:
        # start_id = 580
        # self.actions = [self.game.m_pbs.get_move(x) for x in [399, 1, 392, 462]]

    def init_stats(self, fighter):
        # HP - ATK - DEF - SPATK - SPDEF - SPEED
        self.nature = [1, 1, 1, 1, 1, 1]

        self.stats_base = np.asarray(fighter.basestats.split(","), dtype=int)

        # Reward EVs
        self.stats_reward = np.asarray(fighter.effortpoints.split(","), dtype=int)

        # TEMP
        self.stats_IV = np.random.randint(0, 32, 6)

        # TEMP
        self.stats_EV = np.zeros(6, dtype=np.int64)

    def get_level_exp(self):
        if self.level < 100:
            self.level_xp = int(
                self.game.m_pbs.get_level_exp(self.data["growthrate"], self.level)
            )
            return self.level_xp
        self.level_xp = 0
        return 0

    def gain_evs(self, evs):
        ev_np = np.array(evs)
        print("EV_REWARD", ev_np)
        if np.sum(self.stats_EV) >= 510:
            return
        self.stats_EV = np.add(ev_np, self.stats_EV)
        stat = 5
        while np.sum(self.stats_EV) >= 510:
            self.stats_EV[stat] -= 1 if ev_np[stat] > 0 else 0
            stat = (stat - 1) % 6
        print("NEW EVs", self.stats_EV)
        return

    @property
    def stats(self):
        hp_mod = np.asarray([self.level + 10, 5, 5, 5, 5, 5])
        return (
            self.nature
            * (
                (2 * self.stats_base + self.stats_IV + self.stats_EV // 4)
                * (self.level / 100)
                + hp_mod
            )
        ).astype(int)

    @property
    def series(self):
        self.data["level"] = self.level
        self.data["stats_EV"] = self.stats_EV
        self.data["current_hp"] = self.current_hp
        self.data["current_xp"] = self.current_xp
        self.data["level_xp"] = self.level_xp
        self.data["actions"] = [int(action.id) for action in self.actions]
        self.data["status"] = self.status

        return self.data
