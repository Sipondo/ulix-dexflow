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

        for i in range(6):
            self.members.append(self.init_random_member())

        for i in range(400):
            # self.items.append(self.init_random_item())
            self.add_item(np.random.randint(1, 600), 1)

        self.sort_items()

    def init_random_item(self):
        rng = self.game.m_pbs.get_random_item()
        return PartyItem(self.game, rng)

    def init_random_member(self):
        mem = PartyMember(self.game, self.game.m_pbs.get_random_fighter())
        mem.moves = [PartyMove(self.game.m_pbs.get_random_move()) for _ in range(4)]
        return mem

    def init_bag(self):
        for name in ["Poke Ball", "Bla Ball", "Super Ball", "Great Ball"]:
            self.balls[name] = np.random.randint(9)

    def add_item(self, id, quantity):
        pre_exist = [x for x in self.items if x.id == id]
        if pre_exist:
            pre_exist[0].quantity += quantity
        else:
            self.items.append(PartyItem(self.game, self.game.m_pbs.get_item(id)))

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
