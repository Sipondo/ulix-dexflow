from game.player.partyitem import PartyItem

import dataclasses
from typing import Optional


@dataclasses.dataclass
class ShopItemData:
    name: str
    price: int
    quantity: Optional[int]


class ShopInterface:
    def __init__(self, game, options, owner):
        self.game = game
        self.owner = owner
        self.items = []
        print(options)
        self.init_items(options)

    def init_items(self, items):
        for i in items:
            item_data = self.game.m_pbs.get_item(i)
            item = PartyItem(self.game, item_data)
            item_d = ShopItemData(name=item.id, price=item.price, quantity=None)
            self.items.append(item_d)
