import pandas as pd


class PartyMove:
    def __init__(self, move_info):
        self.data = move_info.copy()
        # print(move_info)
        self.identifier = move_info.identifier
        self.name = move_info["name"]
        self.function = move_info.function
        self.power = move_info.power
        self.type = move_info.type
        self.damagecat = move_info.damagecat
        self.accuracy = move_info.accuracy
        self.max_pp = int(move_info.pp)
        self.pp = self.max_pp
        self.chance = move_info.chance
        self.target = move_info.target
        self.priority = move_info.priority
        self.flags = move_info.flags
        self.description = move_info.description

        # ef = self.db.get_move_map(move_info.effect_id)

        # self.effect = ef.effect
        # self.effect_short = ef.short_effect
