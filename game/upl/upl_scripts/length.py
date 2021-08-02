class Length:
    def __init__(self, act, src, user, s):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.s = s

    def on_read(self):
        return len(self.s)
