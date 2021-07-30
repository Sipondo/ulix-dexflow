import pandas as pd


class PartyMove:
    def __init__(self, data):
        self.data = data.copy()
        # self.identifier = data.identifier
        # self.name = data["name"]
        # self.function = data.function
        # self.power = data.power
        # self.type = data.type
        # self.damagecat = data.damagecat
        # self.accuracy = data.accuracy
        # self.max_pp = int(data.pp)
        # self.pp = self.max_pp
        # self.chance = data.chance
        # self.target = data.target
        # self.priority = data.priority
        # self.flags = data.flags
        # self.description = data.description
        for k, v in data.items():
            setattr(self, k, v)

    @property
    def series(self):
        return self.data
