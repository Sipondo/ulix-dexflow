"""function
Unfades the screen.

Unfades the screen.

in:
None

"""


class Unfade:
    def __init__(self, act, src, user):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.act.game.r_fad.go_to(0.0)
        self.act.game.r_fad.blocking = False

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
