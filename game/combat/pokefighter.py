from .combatfighter import CombatFighter

import numpy as np
import numbers
import random


class PokeFighter(CombatFighter):
    def __init__(self, game, fighter):
        super().__init__(game, fighter)

        if isinstance(fighter, numbers.Number):
            fighter = self.game.m_pbs.get_fighter(fighter)

        self.type_1 = str(fighter["type1"])
        self.type_2 = str(fighter["type2"])

        # Init actions starting from id:
        # start_id = 580
        self.actions = [
            self.game.m_pbs.get_move(x) for x in [399, 1, 392, 462]
        ]

        self.level = 100
        self.gender = random.choice(["Male", "Female", "Genderless"])

        self.set_stats(fighter)
        print(self.name, "HP:", self.stats[0])

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

    @property
    def stats(self):
        hp_mod = np.asarray([self.level + 10, 5, 5, 5, 5, 5])
        return (
            self.naturemod
            * (
                (2 * self.stats_base + self.stats_individuals + self.stats_effort // 4)
                * (self.level / 100)
                + hp_mod
            )
        ).astype(int)
