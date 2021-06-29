from .combatfighter import CombatFighter

import numpy as np
import numbers


class PokeFighter(CombatFighter):
    def __init__(self, game, fighter):
        super().__init__(game, fighter)

        number = False
        if isinstance(fighter, numbers.Number):
            number = True
            fighter = self.game.m_pbs.get_fighter(fighter)
            self.level = 100
            self.stats = self.set_stats(fighter)
        else:
            self.level = fighter.level
            self.current_hp = fighter.current_hp
            self.current_xp = fighter.current_xp
            self.level_xp = fighter.level_xp
            self.stats = fighter.stats

        self.type_1 = str(fighter["type1"])
        self.type_2 = str(fighter["type2"])

        # Init actions starting from id:
        # start_id = 580
        self.actions = [
            self.game.m_pbs.get_move(x) for x in [399, 1, 392, 462]
        ]

        self.data = fighter.copy()
        if number:
            self.set_stats(fighter)
            self.current_hp = self.stats[0]

    def set_stats(self, fighter, ivs=None):
        # HP - ATK - DEF - SPATK - SPDEF - SPEED
        self.naturemod = [1, 1, 1, 1, 1, 1]

        self.stats_base = np.asarray(fighter.basestats.split(","), dtype=int)

        # Reward EVs
        self.stats_reward = np.asarray(fighter.effortpoints.split(","), dtype=int)

        # TEMP
        self.stats_individuals = np.random.randint(0, 32, 6)

        # TEMP
        self.stats_effort = np.unique(np.random.randint(0, 6, 510), return_counts=True)[
            1
        ]
        hp_mod = np.asarray([self.level + 10, 5, 5, 5, 5, 5])
        return (
                self.naturemod
                * (
                        (2 * self.stats_base + self.stats_individuals + self.stats_effort // 4)
                        * (self.level / 100)
                        + hp_mod
                )
        ).astype(int)

    @property
    def series(self):
        self.data["level"] = self.level
        self.data["stats"] = self.stats
        self.data["current_hp"] = self.current_hp
        self.data["current_xp"] = self.current_xp
        self.data["level_xp"] = self.level_xp

        return self.data
