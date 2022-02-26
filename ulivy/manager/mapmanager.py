import numpy as np
from math import floor, ceil

from io import BytesIO
from pathlib import Path


class MapManager:
    def __init__(self, game, level_override=False):
        self.game = game
        self.levels = None

        # if level_override:
        #     print(level_override)
        #     self.current_level_id = self.convert_mapstring_to_key(level_override)
        # else:
        #     self.current_level_id = self.game.m_sav.load("current_level_id") or 1000

        self.current_level_id = 1000

        print("Initialised Map Manager")
        print("ID:", self.current_level_id)
        self.allow_save = False
        self.allow_cycle = False
        self.environment = "forest"
        # self.hospital = self.game.m_sav.load("current_hospital") or "L1"

    def get_world_data(self):
        # TEMP!!!!!!! ULIVY
        pth = Path("world.ldtkc")
        with open(pth, "rb") as file:
            return np.load(BytesIO(file.read()), allow_pickle=True)

    def load_world_data(self):
        # print(self.game.m_res.get_world_data().files)
        # data = self.game.m_res.get_world_data()

        data = self.get_world_data()
        print(data.files)

        level_data, self.world_data = [data[key][()] for key in data.files]
        self.levels = {int(key): level_data[key] for key in level_data.keys()}

        # self.game.m_sav.settables.holder_is_frozen = False
        # self.game.m_sav.switches.holder_is_frozen = False
        # for value in self.world_data["settables"]:
        #     self.game.m_sav.set_new_settable(value, 0)

        # for value in self.world_data["switches"]:
        #     self.game.m_sav.set_new_switch(value, False)

        # self.game.m_sav.settables.holder_is_frozen = True
        # self.game.m_sav.switches.holder_is_frozen = True

    def convert_mapstring_to_key(self, mapstr):
        # Now also accepts integers
        mapstr = str(mapstr).strip()
        if mapstr[0] != "L":
            mapint = int(mapstr)
            if mapint < 1000:
                return 1000 * mapint
            return mapint
        if mapstr[-1] != "_":
            mapstr = mapstr + "_"
        id_e = [int(x[1:]) for x in mapstr.lower().split("_")[:-1]]
        return int(id_e[0] * 1000 + (len(id_e) > 1 and id_e[1] or 0))

    def set_level(self, id):
        self.current_level_id = id
        self.game.m_sav.go_to_new_level()
        self.game.m_sav.save("current_level_id", id)

        fields = self.current_level["fields"]
        self.filter = (
            fields["filter_red"],
            fields["filter_green"],
            fields["filter_blue"],
        )

        self.encounters = fields["encounters"]
        self.encounter_rate = fields["encounter_rate"]
        self.encounter_level_min = fields["encounter_level_min"]
        self.encounter_level_max = fields["encounter_level_max"]

        self.local_encounters = ""
        self.local_encounter_rate = 0
        self.local_encounter_level_min = 0
        self.local_encounter_level_max = 0

        self.allow_save = fields["allow_save"]
        self.allow_cycle = fields["allow_cycle"]
        self.environment = fields["environment"]
        if fields["hospital"]:
            self.hospital = fields["hospital"]
        self.game.m_sav.save("current_hospital", self.hospital)

    def get_encounter_level(self):
        if self.local_encounter_level_max > 0:
            return np.random.choice(
                [
                    int(x)
                    for x in range(
                        int(self.local_encounter_level_min),
                        int(self.local_encounter_level_max),
                    )
                ]
            )
        return np.random.choice(
            [
                int(x)
                for x in range(
                    int(self.encounter_level_min), int(self.encounter_level_max)
                )
            ]
        )

    def get_level_size(self, level_id):
        return self.levels[level_id]["orig_dimensions"]

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
