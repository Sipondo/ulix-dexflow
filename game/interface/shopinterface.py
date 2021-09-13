from game.player.partyitem import PartyItem

import dataclasses
from typing import Optional, Any


@dataclasses.dataclass
class ShopItemData:
    data: PartyItem
    name: str
    price: int
    quantity: Optional[int]


class ShopInterface:
    def __init__(self, game, owner):
        self.game = game
        self.owner = owner

        self.item_selected = False
        self.items = []
        self.init_items(owner.items)

    def init_items(self, items):
        for i in items:
            item_data = self.game.m_pbs.get_item(i)
            item = PartyItem(self.game, item_data)
            item_d = ShopItemData(data=item, name=item.id, price=item.price, quantity=None)
            try:
                item_d.name = i
                item_d.price = int(items[i]["price"])
                item_d.quantity = int(items[i]["quantity"])
            except Exception as e:
                pass
            print(item_d)
            self.items.append(item_d)

    def get_item(self, idx):
        return self.items[idx]

    def get_item_data(self, idx):
        return self.items[idx].data

    def get_quantity(self, idx):
        return self.items[idx].quantity

    @property
    def size(self):
        return len(self.items)
