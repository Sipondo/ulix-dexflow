import numpy as np


class PartyMember:
    def __init__(self, game, fighter):
        self.game = game
        self.name = str(fighter["name"])
        self.species = self.name
        self.id = fighter.name
        self.internalname = fighter.internalname
        self.icon = self.game.m_res.get_party_icon(self.internalname)
        self.sprite = self.game.m_res.get_sprite_from_anim(self.id, size=2.0)
        self.type_1 = fighter.type1
        self.type_2 = fighter.type2
        self.data = fighter.copy()
        self.level = 100
        self.flavor = fighter.pokedex
        self.current_hp = 0.6

        self.moves = []
        # TODO:

        self.exp_total = 560
        self.exp_next = 182

        self.nature = self.game.m_dat.get_nature()
        self.nature_name = self.nature.identifier.capitalize()

        self.set_stats(fighter)

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

        self.set_characteristic()

    def set_characteristic(self):
        best_id = np.argmax(self.stats_individuals)
        self.characteristic_id = 6 * (self.stats_individuals[best_id] % 5) + best_id
        self.characteristic = self.game.m_dat.get_characteristic(self.characteristic_id)

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

    @property
    def series(self):
        self.data.current_hp = self.current_hp
        self.data.level = self.level
        self.data["stats"] = self.stats

        return self.data
