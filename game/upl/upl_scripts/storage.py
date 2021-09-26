"""function
Opens the battler storage.

Opens the battler storage. 

in:
None

"""


class Storage:
    def __init__(self, act, src, user):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.act.game.m_gst.switch_state("storage")

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
