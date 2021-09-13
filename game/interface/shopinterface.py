from game.player.partyitem import PartyItem


class ShopInterface:
    def __init__(self, game, options, owner):
        self.game = game
        self.owner = owner
        self.items = []
        self.init_items(options)

    def init_items(self, items):
        for i in items:
            self.items.append(PartyItem(self.game, i, q))



