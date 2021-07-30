import numpy as np


class PartyItem:
    def __init__(self, game, data, quantity=1):
        self.game = game
        self.data = data.copy()
        self.id = data.name
        # self.identifier = data.identifier
        # self.name = data.itemanme
        # self.names = data.itemplural
        # self.pocket = data.pocket
        # self.price = data.price
        # self.description = data.description
        # self.use_outside = data.use_outside
        # self.use_battle = data.use_battle
        # self.special = data.special
        # self.move = data.move
        self.price = 0
        self.quantity = quantity
        for k, v in data.items():
            setattr(self, k, v)
        self.icon = self.game.m_res.get_item_icon(self.identifier, size=0.5)

    @property
    def series(self):
        self.data["quantity"] = self.quantity
        self.data["price"] = self.price
        return self.data
