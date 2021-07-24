class Concat:
    def __init__(self, act, src, user, *args):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.s = args

    def on_read(self):
        return "".join([str(x) for x in self.s])

