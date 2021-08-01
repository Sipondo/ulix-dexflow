from numpy.random import rand


class Random:
    def __init__(self, act, src, user):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time

    def on_read(self):
        return rand()
