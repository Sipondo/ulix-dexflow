from game.animation.moveanimation.pathmoveanimation import PathMoveAnimation


class Move:
    def __init__(self, act, src, user, x, y, next_to=False):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.x = x
        self.y = y
        self.init = False
        self.next_to = next_to

    def on_tick(self, time=None, frame_time=None):
        if not self.init and time is not None:
            path = self.game.m_col.a_star(
                self.user.game_position,
                (
                    self.x - self.game.m_col.offset[0],
                    self.y - self.game.m_col.offset[1],
                ),
                next_to=self.next_to,
            )
            self.anim = PathMoveAnimation(
                self.game,
                time,
                path.pop(0),
                self.user,
                distance=len(path) + 1,
                path=path,
            )
            if self.act.game.m_ani.add_animation(self.anim):
                self.user.moving = True
                self.init = True

        if not self.anim.ended or not self.init:
            return False
        return True
