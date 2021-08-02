from .combatfighter import CombatFighter

import numpy as np
import numbers


class PokeFighter(CombatFighter):
    def __init__(self, game, fighter):
        super().__init__(game, fighter)

        if isinstance(fighter, str):
            fighter = self.game.m_pbs.get_fighter_by_name(fighter)
            self.level = 100
            self.init_stats(fighter)
            self.current_hp = self.stats[0]
            self.current_xp = 0
        elif isinstance(fighter, numbers.Number):
            fighter = self.game.m_pbs.get_fighter(fighter)
            self.level = 100
            self.init_stats(fighter)
            self.current_hp = self.stats[0]
            self.current_xp = 0
        else:
            if "level" in fighter:
                self.level = fighter.level
            else:
                self.level = 100

            if "stats_base" in fighter:
                self.stats_base = fighter.stats_base
                self.stats_reward = fighter.stats_reward
                self.stats_IV = fighter.stats_IV
                self.stats_EV = fighter.stats_EV
                self.nature = fighter.nature
            else:
                self.init_stats(fighter)

            if "current_hp" in fighter:
                self.current_hp = fighter.current_hp
                print(self.name, self.current_hp)
            else:
                self.current_hp = self.stats[0]

            if "current_xp" in fighter:
                self.current_xp = fighter.current_xp
                self.level_xp = fighter.level_xp
            else:
                self.current_xp = 0
                self.level_xp = 0

        self.starting_hp = self.current_hp
        self.type1 = str(fighter["type1"])
        self.type2 = str(fighter["type2"])

        # Init actions starting from id:
        # start_id = 580
        # self.actions = [self.game.m_pbs.get_move(x) for x in [399, 1, 392, 462]]
        self.actions = [self.game.m_pbs.get_move(x) for x in [87, 399, 399, 399]]

        self.data = fighter.copy()

    def init_stats(self, fighter, ivs=None):
        # HP - ATK - DEF - SPATK - SPDEF - SPEED
        self.nature = [1, 1, 1, 1, 1, 1]

        self.stats_base = np.asarray(fighter.basestats.split(","), dtype=int)

        # Reward EVs
        self.stats_reward = np.asarray(fighter.effortpoints.split(","), dtype=int)

        # TEMP
        self.stats_IV = np.random.randint(0, 32, 6)

        # TEMP
        self.stats_EV = np.unique(np.random.randint(0, 6, 510), return_counts=True)[1]

    def set_new_level_xp(self):
        # TODO exp function
        self.level_xp += 100

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

        return self.data
