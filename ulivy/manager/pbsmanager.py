from ulivy.helpers.dataframe import read_csv, Series, DataFrame
import re


class PbsManager:
    def __init__(self, game):
        self.game = game
        self.dfs = {}

        self.items = read_csv(
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

        self.moves = read_csv(
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
        self.moves.map_attr("priority", lambda x: int(x))
        move_functions = read_csv(
            self.game.m_res.get_pbs_loc("move_functions_map.csv"), index_col=0,
        )["function"]
        move_functions = move_functions.apply(lambda x: re.sub("[\[\]]", "", x))
        move_functions = move_functions.apply(lambda x: x.split(","))
        self.moves.map_attr(
            "function",
            lambda x: move_functions[x] if x in move_functions else ["noeffect"],
        )
        # self.moves.map_attr("power", lambda x: int(x))

        self.abilities = read_csv(
            self.game.m_res.get_pbs_loc("abilities.csv"), index_col=0
        )

        self.weather_changes = read_csv(
            self.game.m_res.get_pbs_loc("weather_acc_moves.csv"), index_col=0
        )

        self.terrain_mods = read_csv(
            self.game.m_res.get_pbs_loc("terrain_mod_moves.csv"), index_col=0
        )
        for terrain in ("Grassy", "Misty", "Electric", "Psychic"):
            self.terrain_mods[terrain].apply(lambda x: float(x))

        self.fighters = self.read_fighters()
        # self.fighters["current_hp"] = 1.0

        self.move_anim = read_csv(
            self.game.m_res.get_pbs_loc("move_anim_map.csv", compressed=False),
            index_col=0,
        )

        # self.move_anim = self.move_anim.dropna(axis=1, how="all").dropna(
        #     axis=0, how="all"
        # )

        self.level_exp = read_csv(
            self.game.m_res.get_pbs_loc("level_exp.csv"), index_col=0
        )

        self.type_effectiveness = read_csv(
            self.game.m_res.get_pbs_loc("type_effectiveness.csv"), index_col=0,
        )

    def get_random_item(self):
        return self.items.sample().loc[0]

    def get_item(self, id):
        s = self.items[self.items["identifier"] == id.upper()].iloc[0].copy()
        return s

    def get_related_anim(self, type, power):
        if int(power) > 75:
            return self.move_anim.loc[type.upper(), "highpower"]
        return self.move_anim.loc[type.upper(), "lowpower"]

    def read_text(self, filename):
        frame = []

        with open(filename, "r", encoding="utf-8-sig") as file:
            series = Series()
            for line in file.readlines():
                if not len(line) or line.strip()[0] == "#":
                    continue
                if line.strip()[0] == "[":
                    frame.append(series)
                    series = Series()
                    continue
                split = line.split("=")
                series[split[0].strip().lower()] = "=".join(split[1:]).strip()
            frame.append(series)
        return DataFrame(frame)

    def read_fighters(self):
        # TODO: fix
        pth = self.game.m_res.get_pbs_loc("pokemon.csv", compressed=True)
        if pth is None:  # or not pth.is_file():
            self.read_text(self.game.m_res.get_pbs_loc("pokemon.txt")).to_csv(pth)
            pth = self.game.m_res.get_pbs_loc("pokemon.csv", compressed=True)

        return read_csv(pth, index_col=0)

    def get_random_fighter(self):
        return self.fighters.iloc[1:600].sample()

    def get_fighter(self, id):
        return self.fighters.loc[id]

    def get_fighter_by_name(self, name):
        return (
            self.fighters[self.fighters["name"].lower() == name.lower()].iloc[0].copy()
        )

    def get_move(self, id):
        # id = 201  # TODO: temp only tackle
        id = 201  # 399  # TODO: temp only tackle #xcissor 8
        # 142, 188, 663
        return self.moves.loc[id]

    def get_move_by_name(self, name):
        name = "tackle"  # TODO: temp only tackle
        name_s = name.replace(" ", "").upper()
        # print(self.moves)
        s = self.moves["identifier"]
        t = s == name_s
        # print(t)
        return self.moves[t].iloc[0]

    def get_random_move(self):
        return self.moves.sample().loc[0]

    def get_ability(self, ability_name):
        return self.abilities.loc[ability_name]

    def get_terrain_mods(self, terrain):
        return self.terrain_mods.loc[terrain]

    def get_weather_acc_change(self, weather):
        return self.weather_changes.loc[weather]

    def get_level_exp(self, growth_type, level):
        return self.level_exp[growth_type].loc[level]

    def get_type_effectiveness(self, atk_type, def_type):
        atk_type = atk_type.capitalize()
        def_type = def_type.capitalize()
        return self.type_effectiveness[def_type].loc[atk_type]
