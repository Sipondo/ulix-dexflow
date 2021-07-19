class Say:
    def __init__(self, act, src, user, obj):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.obj = obj
        self.src = src
        self.user = user
        self.act.game.m_gst.current_state.dialogue = self.obj
        self.act.game.m_gst.current_state.author = self.user.name
        print("PARSING TEXT", self.user, self.obj)

    def on_tick(self, time=None, frame_time=None):
        if self.act.game.m_gst.current_state.dialogue is not None:
            return False
        return True
