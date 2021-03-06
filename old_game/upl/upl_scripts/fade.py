"""function
Fades the screen to black.

Fades the screen to black. Unfade by calling `Unfade()`.

in:
None

"""


class Fade:
    def __init__(self, act, src, user):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.act.game.r_int.fade = True

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
