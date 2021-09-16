from game.player.partyitem import PartyItem

import dataclasses
from typing import Optional


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
        print(owner.items)
        self.items = []
        self.init_items(owner.items)

    def init_items(self, items):
        for i in items:
            item_data = self.game.m_pbs.get_item(i)
            item = PartyItem(self.game, item_data)
            quantity = None
            # remove key items from shop if player has them, or only give 1
            if item.pocket == 8:
                if self.game.inventory.count_item(item.identifier) > 0:
                    print("Existing key item!")
                    continue
                quantity = 1
            item_d = ShopItemData(data=item, name=item.itemname, price=item.price, quantity=quantity)
            for k, v in items[i].items():
                try:
                    setattr(item_d, k, v)
                except Exception as e:
                    pass
            self.items.append(item_d)

    def save_items(self):
        items = {}
        for item in self.items:
            items[item.name] = {}
            items[item.name]["price"] = item.price
            items[item.name]["quantity"] = item.quantity
        holder = self.game.m_sav.get_memory_holder(self.game.m_map.current_level_id, self.owner.entity_uid)
        setattr(holder, "items", items)
        self.owner.items = items

    def get_item(self, idx: int):
        return self.items[idx]

    def get_item_data(self, idx: int):
        return self.items[idx].data

    def get_quantity(self, idx: int):
        return self.items[idx].quantity

    def buy_item(self, idx: int, quantity: int) -> bool:
        # should never happen
        q = self.items[idx].quantity or 100
        if quantity > q:
            return False

        total = self.items[idx].price * quantity
        if total > self.game.inventory.money:
            return False

        self.game.inventory.add_item(
            self.items[idx].data.identifier,
            quantity,
        )
        self.game.inventory.money -= total
        if self.items[idx].quantity is not None:
            self.items[idx].quantity -= quantity
        if self.items[idx].quantity == 0:
            self.items.pop(idx)
        return True

    @property
    def size(self):
        return len(self.items)
