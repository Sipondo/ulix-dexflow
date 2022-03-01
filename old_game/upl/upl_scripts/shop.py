"""function
Open a shop.

Open a shop. Typically only used from within a shop entity.

in:
None

"""


class Shop:
    def __init__(self, act, src, user):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user

        self.act.game.m_gst.switch_state("shop", owner=self.user)

        if self.user.dialogue is not None:
            self.act.game.m_gst.current_state.dialogue = self.user.dialogue

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
