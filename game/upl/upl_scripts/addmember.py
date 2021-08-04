class AddMember:
    def __init__(self, act, src, user, s, l=5):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.s = s
        self.game.inventory.add_member(self.game.m_pbs.get_fighter_by_name(s), l)
        self.act.game.m_gst.current_state.dialogue = f"Received a {s}!"
        self.game.r_aud.play_effect("receive")

    def on_tick(self, time=None, frame_time=None):
        if self.act.game.m_gst.current_state.dialogue is not None:
            return False
        return True

    def on_read(self):
        return None
