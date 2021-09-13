import pandas as pd
import re


class PbsManager:
    def __init__(self, game):
        self.game = game
        self.dfs = {}

        self.items = pd.read_csv(
            self.game.m_res.get_pbs_loc("items.csv"),
            header=None,
            names=[
                "id",
                "identifier",
                "itemname",
                "itemplural",
                "pocket",
                "price",
                "description",
                "use_outside",
                "use_battle",
                "special",
                "move",
            ],
            index_col=0,
            comment="#",
        )

        self.moves = pd.read_csv(
            self.game.m_res.get_pbs_loc("moves.csv"),
            header=None,
            names=[
                "id",
                "identifier",
                "name",
                "function",
                "power",
                "type",
                "damagecat",
                "accuracy",
                "pp",
                "chance",
                "target",
                "priority",
                "flags",
                "description",
            ],
            index_col=0,
            comment="#",
        )
        move_functions = pd.read_csv(
            self.game.m_res.get_pbs_loc("move_functions_map.csv"), index_col=0,
        )["function"]
        move_functions = move_functions.apply(lambda x: re.sub("[\[\]]", "", x))
        move_functions = move_functions.apply(lambda x: x.split(","))
        self.moves["function"] = self.moves["function"].map(
            lambda x: move_functions[x] if x in move_functions else ["noeffect"]
        )
        self.moves["power"] = self.moves["power"].map(lambda x: int(x))

        self.abilities = pd.read_csv(self.game.m_res.get_pbs_loc("abilities.csv"), index_col=0)

        self.weather_changes = pd.read_csv(
            self.game.m_res.get_pbs_loc("weather_acc_moves.csv"), index_col=0
        )

        self.terrain_mods = pd.read_csv(
            self.game.m_res.get_pbs_loc("terrain_mod_moves.csv"), index_col=0
        )
        for terrain in ("Grassy", "Misty", "Electric", "Psychic"):
            self.terrain_mods[terrain].apply(lambda x: float(x))

        self.fighters = self.read_fighters()
        # self.fighters["current_hp"] = 1.0

        self.move_anim = pd.read_csv(
            self.game.m_res.get_pbs_loc("move_anim_map.csv", compressed=False),
            index_col=0,
        )

        self.move_anim = self.move_anim.dropna(axis=1, how="all").dropna(
            axis=0, how="all"
        )

        self.level_exp = pd.read_csv(self.game.m_res.get_pbs_loc("level_exp.csv"), index_col=0)

        self.type_effectiveness = pd.read_csv(self.game.m_res.get_pbs_loc("type_effectiveness.csv"), index_col=0)

    def get_random_item(self):
        return self.items.sample().iloc[0]

    def get_item(self, id):
        s = self.items[self.items.identifier.str.lower() == id.lower().replace(" ", "")].iloc[0].copy()
        return s

    def get_related_anim(self, type, power):
        if power > 75:
            return self.move_anim.loc[type, "highpower"]
        return self.move_anim.loc[type, "lowpower"]

    def read_text(self, filename):
        frame = []

        with open(filename, "r", encoding="utf-8-sig") as file:
            serie = pd.Series()
            for line in file.readlines():
                if not len(line) or line.strip()[0] == "#":
                    continue
                if line.strip()[0] == "[":
                    frame.append(serie)
                    serie = pd.Series()
                    continue
                split = line.split("=")
                serie[split[0].strip().lower()] = "=".join(split[1:]).strip()
            frame.append(serie)
        return pd.DataFrame(frame)

    def read_fighters(self):
        # TODO: fix
        pth = self.game.m_res.get_pbs_loc("pokemon.csv", compressed=True)
        if pth is None or not pth.is_file():
            self.read_text(self.game.m_res.get_pbs_loc("pokemon.txt")).to_csv(pth)
            pth = self.game.m_res.get_pbs_loc("pokemon.csv", compressed=True)

        return pd.read_csv(pth, index_col=0)

    def get_random_fighter(self):
        return self.fighters.iloc[1:600].sample().iloc[0]

    def get_fighter(self, id):
        return self.fighters.loc[id]

    def get_fighter_by_name(self, name):
        return self.fighters[self.fighters["name"].str.lower() == name.lower()].iloc[0]

    def get_move(self, id):
        return self.moves.loc[id]

    def get_move_by_name(self, name):
        name = name.strip()
        return self.moves[
            self.moves["identifier"].str.lower().str.strip() == name.lower()
        ].iloc[0]

    def get_random_move(self):
        return self.moves.sample().iloc[0]

    def get_ability(self, ability_name):
        return self.abilities.loc[ability_name]

    def get_terrain_mods(self, terrain):
        return self.terrain_mods.loc[terrain]

    def get_weather_acc_change(self, weather):
        return self.weather_changes.loc[weather]

    def get_level_exp(self, growth_type, level):
        return self.level_exp[growth_type].loc[level]

    def get_type_effectiveness(self, atk_type, def_type):
        atk_type = atk_type.lower().capitalize()
        def_type = def_type.lower().capitalize()
        return self.type_effectiveness[def_type].loc[atk_type]
