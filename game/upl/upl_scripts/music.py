class Music:
    def __init__(self, act, src, user, s):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.s = s

    def on_tick(self, time=None, frame_time=None):
        self.game.r_aud.play_music(self.s)
        return True

    def on_read(self):
        return None
