"""function
Removes an item from the inventory.

Removes an item from the inventory.
Multiple copies of the item can be removed at once by varying the quantity parameter.

in:
- String: item name
- [Optional, 1] Numeric: quantity

"""


class RemoveItem:
    def __init__(self, act, src, user, s, q=1):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.s = s
        self.q = q

    def on_tick(self, time=None, frame_time=None):
        self.game.inventory.remove_item(self.s, self.q)
        return True

    def on_read(self):
        return None
