import numpy as np
import random


class PartyMember:
    def __init__(self, game, data, l=5):
        self.game = game
        self.data = data.copy()
        self.name = str(data["name"])
        # self.species = self.name
        # self.id = data.name
        self.internalname = data.internalname
        self.type1 = data.type1
        self.type2 = data.type2
        self.level = int(l)
        self.gender = random.choice(["Male", "Female", "Genderless"])
        # self.flavor = data.pokedex

        for k, v in data.items():
            setattr(self, k, v)

        if hasattr(self, "actions"):
            self.actions = [int(i) for i in self.actions]

        self.icon = self.game.m_res.get_party_icon(self.internalname)
        self.sprite = self.game.m_res.get_sprite_from_anim(data.name, size=2.0)

        self.current_xp = 0
        self.level_xp = 5
        self.set_new_level_xp()

        self.nature = self.game.m_dat.get_nature()
        self.nature_name = self.nature.identifier.capitalize()

        self.init_stats(data)

        # LMAO
        for k, v in data.items():
            setattr(self, k, v)

        self.current_hp = self.stats[0]
        self.status = None

        self.abilities = [a for a in self.data.abilities.split(",")]
        hidden_abilities = [a for a in self.data.hiddenability.split(",")]
        self.abilities.extend(hidden_abilities)
        print(self.abilities)
        self.current_ability = 0  # default ability will be first listed

        if isinstance(self.moves, str):
            l = self.moves.split(",")
            self.learnset = [tuple(l[i : i + 2]) for i in range(0, len(l), 2)]

        if not hasattr(self, "actions"):
            l = [(x, y) for x, y in reversed(self.learnset) if int(x) <= self.level]
            k = [y for x, y in l]
            l = [l[i] for i in range(len(l)) if l[i] not in k[:i]]
            self.actions = [self.game.m_pbs.get_move_by_name(y).name for x, y in l][:4]

    def init_stats(self, data, ivs=None):
        # HP - ATK - DEF - SPATK - SPDEF - SPEED
        self.naturemod = [1, 1, 1, 1, 1, 1]

        self.stats_base = np.asarray(data.basestats.split(","), dtype=int)

        # Reward EVs
        self.stats_reward = np.asarray(data.effortpoints.split(","), dtype=int)

        # TEMP
        self.stats_IV = np.random.randint(0, 32, 6)

        # TEMP
        self.stats_EV = np.zeros(6, dtype=int)

        self.set_characteristic()

    def evolve(self, evolution_data):
        self.icon = self.game.m_res.get_party_icon(evolution_data.internalname)
        self.sprite = self.game.m_res.get_sprite_from_anim(evolution_data.name, size=2.0)
        self.data = evolution_data.copy()
        self.name = str(evolution_data["name"])

    def set_new_level_xp(self):
        self.level_xp = self.game.m_pbs.get_level_exp(
            self.data["growthrate"], self.level
        )

    def set_characteristic(self):
        best_id = np.argmax(self.stats_IV)
        self.characteristic_id = 6 * (self.stats_IV[best_id] % 5) + best_id
        self.characteristic = self.game.m_dat.get_characteristic(self.characteristic_id)

    def from_series(self, data):
        self.level = data.level
        self.current_xp = data.current_xp
        self.level_xp = data.level_xp
        self.current_hp = data.current_hp
        self.actions = [int(i) for i in data.actions]
        self.status = data.status

    @property
    def stats(self):
        hp_mod = np.asarray([self.level + 10, 5, 5, 5, 5, 5])
        return (
            self.naturemod
            * (
                (2 * self.stats_base + self.stats_IV + self.stats_EV // 4)
                * (self.level / 100)
                + hp_mod
            )
        ).astype(int)

    @property
    def series(self):
        self.data["level"] = self.level
        self.data["nature"] = self.naturemod
        self.data["stats_base"] = self.stats_base
        self.data["stats_reward"] = self.stats_reward
        self.data["stats_IV"] = self.stats_IV
        self.data["stats_EV"] = self.stats_EV
        self.data["current_hp"] = self.current_hp
        self.data["current_xp"] = self.current_xp
        self.data["level_xp"] = self.level_xp
        self.data["actions"] = self.actions
        self.data["learnset"] = self.learnset
        self.data["status"] = self.status
        self.data["ability"] = self.abilities[self.current_ability]

        return self.data
