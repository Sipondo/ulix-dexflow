import numpy as np
from .partyitem import PartyItem
from .partymember import PartyMember


class Inventory:
    def __init__(self, game):
        self.game = game
        self.members = []
        self.storage = []
        self.items = []
        self.money = 3000

        self.sort_items()

    def init_random_member(self) -> PartyMember:
        mem = PartyMember(self.game, self.game.m_pbs.get_random_fighter())
        return mem

    def init_member(self, data, lvl: int = 5) -> PartyMember:
        new_member = PartyMember(self.game, data, lvl)
        return new_member

    def add_member(self, member: PartyMember):
        if len(self.members) == 6:
            self.storage.append(member)
        else:
            self.members.append(member)

    def add_member_to_storage(self, member: PartyMember):
        self.storage.append(member)

    def add_item(self, id, quantity):
        quantity = int(quantity)
        pre_exist = [x for x in self.items if x.identifier == id]
        if pre_exist:
            pre_exist[0].quantity += quantity
            return pre_exist[0]
        else:
            res = PartyItem(self.game, self.game.m_pbs.get_item(id))
            res.quantity = quantity
            self.items.append(res)
            return res

    def remove_item(self, id, quantity):
        pre_exist = [x for x in self.items if x.identifier == id]
        if pre_exist:
            pre_exist[0].quantity -= quantity
            if pre_exist[0].quantity < 1:
                self.items.remove(pre_exist[0])

    def count_item(self, id):
        pre_exist = [x for x in self.items if x.identifier == id]
        if pre_exist:
            return pre_exist[0].quantity
        return 0

    def get_item(self, id):
        return PartyItem(self.game, self.game.m_pbs.get_item(id))

    def sort_items(self):
        self.items.sort(key=lambda x: x.name)

    @property
    def fighter_names(self):
        return [x.name for x in self.members]

    @property
    def member_names(self):
        return [x.name for x in self.members]

    @property
    def member_icons(self):
        return [x.icon for x in self.members]

    def get_pocket_items(self, pocket):
        return [x for x in self.items if x.pocket == pocket]
