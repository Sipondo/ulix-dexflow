class Prompt:
    def __init__(self, act, src, user, obj, length=15, filter="letters"):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.obj = obj
        self.src = src
        self.user = user
        self.filter = filter
        self.length = length
        # self.act.game.m_gst.current_state.dialogue = self.obj
        # self.act.game.m_gst.current_state.author = (
        #     "" if self.user == self.act.game else self.user.name
        # )
        # self.act.game.m_gst.current_state.options = self.options
        # if hasattr(self.user, "splash") and self.user.splash:
        #     self.act.game.m_gst.current_state.spr_talker = self.user.splash
        self.act.game.m_gst.switch_state(
            "prompt", length=self.length, filter=self.filter
        )

    def on_tick(self, time=None, frame_time=None):
        if self.act.game.m_gst.current_state_name == "Prompt":
            return False
        return True

    def on_read(self):
        return None
