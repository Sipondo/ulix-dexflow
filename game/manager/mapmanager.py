import numpy as np
from math import floor, ceil

from io import BytesIO
from pathlib import Path


class MapManager:
    def __init__(self, game):
        self.game = game
        self.levels = None
        self.current_level_id = self.game.m_sav.load("current_level_id") or 1000
        print("Initialised Map Manager")
        print("ID:", self.current_level_id)

    def load_world_data(self):
        print(self.game.m_res.get_world_data().files)
        data = self.game.m_res.get_world_data()
        level_data, self.world_data = [data[key][()] for key in data.files]
        self.levels = {int(key): level_data[key] for key in level_data.keys()}

        self.game.m_sav.settables.holder_is_frozen = False
        self.game.m_sav.switches.holder_is_frozen = False
        for value in self.world_data["settables"]:
            self.game.m_sav.set_new_settable(value, 0)

        for value in self.world_data["switches"]:
            self.game.m_sav.set_new_switch(value, False)

        self.game.m_sav.settables.holder_is_frozen = True
        self.game.m_sav.switches.holder_is_frozen = True

    def convert_mapstring_to_key(self, mapstr):
        if mapstr[-1] != "_":
            mapstr = mapstr + "_"
        id_e = [int(x[1:]) for x in mapstr.lower().split("_")[:-1]]
        return int(id_e[0] * 1000 + (len(id_e) > 1 and id_e[1] or 0))

    def set_level(self, id):
        self.game.m_sav.go_to_new_level()
        self.current_level_id = id
        self.game.m_sav.save("current_level_id", id)

        fields = self.current_level["fields"]
        self.filter = (
            fields["filter_red"],
            fields["filter_green"],
            fields["filter_blue"],
        )

    @property
    def current_level(self):
        return self.levels[self.current_level_id]  # [()]

    @property
    def level_index(self):
        return self.level_keys.index(self.current_level_id)

    @property
    def current_tiles(self):
        return self.current_level["layers"][0][1]

    @property
    def level_keys(self):
        return list(self.levels.keys())

    @property
    def enum_values(self):
        return self.world_data["enumValues"]

    @property
    def current_tilesets(self):
        return self.current_level["layers"]

    @property
    def current_connected_tilesets(self):
        return [
            (
                self.levels[self.convert_mapstring_to_key(x["f_target_level"])][
                    "layers"
                ],
                (floor(x["location"][0] / 16), ceil(x["location"][1] // 16)),
                x["f_target_location"],
                x["f_target_direction"],
            )
            for x in self.current_regions
            if x["identifier"] == "PortalConnection"
        ]

    @property
    def current_entities(self):
        return self.current_level["entities"]

    @property
    def current_regions(self):
        return self.current_level["regions"]
