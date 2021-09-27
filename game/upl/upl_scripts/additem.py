"""function
Add an item to the inventory.

Add an item to the inventory.
Multiple copies of the item can be added at once by varying the quantity parameter.

in:
- String: item name
- [Optional, 1] Numeric: quantity

"""


class AddItem:
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
        item = self.game.inventory.add_item(self.s, self.q)
        self.act.game.m_gst.current_state.dialogue = f"Received {q}x {item.itemname}"
        self.game.r_aud.play_effect("receive")

    def on_tick(self, time=None, frame_time=None):
        if self.act.game.m_gst.current_state.dialogue is not None:
            return False
        return True

    def on_read(self):
        return None
