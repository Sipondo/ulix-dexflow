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
            lambda x: move_functions[x] if x in move_functions else "noeffect"
        )
        self.moves["power"] = self.moves["power"].map(lambda x: int(x))

        self.weather_changes = pd.read_csv(
            self.game.m_res.get_pbs_loc("weather_acc_moves.csv"), index_col=0
        )

        self.terrain_mods = pd.read_csv(
            self.game.m_res.get_pbs_loc("terrain_mod_moves.csv"), index_col=0
        )
        for terrain in ("Grassy", "Misty", "Electric", "Psychic"):
            self.terrain_mods[terrain].apply(lambda x: float(x))

        self.fighters = self.read_fighters()
        self.fighters["current_hp"] = 1.0

    def get_random_item(self):
        return self.items.sample().iloc[0]

    def get_item(self, id):
        s = self.items[self.items.identifier == id].iloc[0].copy()
        return s

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
        if not pth.is_file():
            self.read_text(self.game.m_res.get_pbs_loc("pokemon.txt")).to_csv(pth)

        return pd.read_csv(pth, index_col=0)

    def get_random_fighter(self):
        return self.fighters.iloc[1:600].sample().iloc[0]

    def get_fighter(self, id):
        return self.fighters.loc[id]

    def get_fighter_by_name(self, name):
        return self.fighters[self.fighters["name"].str.lower() == name.lower()].iloc[0]

    def get_move(self, id):
        return self.moves.loc[id]

    def get_random_move(self):
        return self.moves.sample().iloc[0]

    def get_terrain_mods(self, terrain):
        return self.terrain_mods.loc[terrain]

    def get_weather_acc_change(self, weather):
        return self.weather_changes.loc[weather]
