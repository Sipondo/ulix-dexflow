"""function
Jump up and down.

The user does a small jump out of excitement, fear or surprise.

in:
None

"""


from ulivy.animation.jumpanimation import JumpAnimation


class Jump:
    def __init__(self, act, src, user):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.init = False

    def on_tick(self, time=None, frame_time=None):
        if not self.init and time is not None:
            self.anim = JumpAnimation(self.game, time, self.user)
            if self.act.game.m_ani.add_animation(self.anim):
                self.user.moving = True
                self.init = True

        if not self.anim.ended or not self.init:
            return False
        return True

    def on_read(self):
        return None
