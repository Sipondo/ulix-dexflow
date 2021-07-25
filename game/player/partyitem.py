import numpy as np


class PartyItem:
    def __init__(self, game, template, quantity=1):
        self.game = game
        self.id = template.name
        self.identifier = template.identifier
        self.name = template.single
        self.names = template.plural
        self.pocket = template.pocket
        self.price = template.price
        self.description = template.description
        self.use_outside = template.use_outside
        self.use_battle = template.use_battle
        self.special = template.special
        self.move = template.move
        self.icon = self.game.m_res.get_item_icon(self.identifier, size=0.5)

        self.price = 0
        self.quantity = quantity

        #         "id",
        #         "identifier",
        #         "name",
        #         "names",
        #         "pocket",
        #         "price",
        #         "description",
        #         "use_outside",
        #         "use_battle",
        #         "special",
        #         "move",
        # self.id = template.name
        # self.identifier = template.identifier

        # # if self.identifier[:2] in ["tm", "hm"]:
        # #     self.icon = self.game.m_res.get_item_icon("hm01")
        # # else:
        # #     self.icon = self.game.m_res.get_item_icon(self.identifier)
        # # self.sprite = self.game.m_res.get_sprite_from_anim(self.id, size=2.0)
        # # self.type_1 = fighter.type_1.values[0]
        # # self.type_2 = fighter.type_2.values[0]
        # # # self.id = fighter["id"]
        # # self.data = fighter.iloc[0].copy()
        # # self.moves = moveset
        # # self.level = 100
        # # self.flavor = self.game.m_dat.get_flavor(self.id)

        # # # TODO:

        # # self.exp_total = 560
        # # self.exp_next = 182

        # # self.nature = self.game.m_dat.get_nature()
        # # self.nature_name = self.nature.identifier.iloc[0].capitalize()

        # self.quantity = quantity
