"""function
Move to the specified location

Move to the specified location. The entity will automatically pathfind towards the location and stop early if anything actively blocks the entity. `Move()` will throw an error when there is no path available, including when the entity is already on the specified location.
In most situations `Move()` should be excused to prevent unwanted errors.

in:
- Numeric: x position
- Numeric: y position
- [DEPRECATED] Bool: whether to move to the position or next to the position (Use `MoveTo()` instead!)

"""


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
        self.x = int(x)
        self.y = int(y)
        self.init = False
        self.next_to = next_to

    def on_tick(self, time=None, frame_time=None):
        if not self.init and time is not None:
            # print(
            #     "MOVE:",
            #     (
            #         self.user.game_position[0] + self.game.m_col.offset[0],
            #         self.user.game_position[1] + self.game.m_col.offset[1],
            #         self.user.game_position[0],
            #         self.user.game_position[1],
            #     ),
            #     (
            #         self.x,
            #         self.y,
            #         self.x - self.game.m_col.offset[0],
            #         self.y - self.game.m_col.offset[1],
            #     ),
            # )
            if self.user.moving:
                print("Entity is already moving!")
                raise Exception("Entity is already moving!")

            path = self.game.m_col.a_star(
                self.user.game_position,
                (
                    self.x - self.game.m_col.offset[0],
                    self.y - self.game.m_col.offset[1],
                ),
                next_to=self.next_to,
                src_entity=self.user,
                height=self.user.height,
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

    def on_read(self):
        return None
