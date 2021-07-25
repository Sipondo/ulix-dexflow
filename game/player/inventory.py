import numpy as np
from .partyitem import PartyItem
from .partymember import PartyMember
from .partymove import PartyMove


class Inventory:
    def __init__(self, game):
        self.game = game
        self.balls = {}
        self.init_bag()

        self.members = []
        self.items = []

        for i in range(3):
            self.members.append(self.init_random_member())

        # for i in range(400):
        #     self.add_item(self.game.m_pbs.get_random_item().identifier, 1)

        self.sort_items()

    def init_random_member(self):
        mem = PartyMember(self.game, self.game.m_pbs.get_random_fighter())
        mem.moves = [PartyMove(self.game.m_pbs.get_random_move()) for _ in range(4)]
        return mem

    def init_bag(self):
        for name in ["Poke Ball", "Bla Ball", "Super Ball", "Great Ball"]:
            self.balls[name] = np.random.randint(9)

    def add_item(self, id, quantity):
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
