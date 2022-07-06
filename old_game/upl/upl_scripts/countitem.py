"""fobject
Counts how many the player has of an item.

Counts how many copies the player has of an item.
Remember that 0 is a false value in UPL and Python; use this function in a conditional to check for e.g. key items.

in:
- String: name of the item

out:
- Numeric: found quantity

"""


class CountItem:
    def __init__(self, act, src, user, s):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.s = s

    def on_read(self):
        return self.game.inventory.count_item(self.s)
