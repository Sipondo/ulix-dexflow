"""function
Take a step in the specified direction.

Take a step in the specified direction. Directions are given by single-letter capital-only strings `N` `W` `S` `E`.
`Step()` will throw an error if the step is blocked. Fou should excuse `Step()` if this is a possibility.

in:
- String: direction

"""


from game.animation.moveanimation.basemoveanimation import BaseMoveAnimation


class Step:
    def __init__(self, act, src, user, direction):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time

        if isinstance(direction, int):
            if direction == 0:
                self.direction = (1, 0)
            elif direction == 1:
                self.direction = (0, 1)
            elif direction == 2:
                self.direction = (-1, 0)
            elif direction == 3:
                self.direction = (0, -1)
        elif isinstance(direction, str):
            if direction == "E":
                self.direction = (1, 0)
            elif direction == "S":
                self.direction = (0, 1)
            elif direction == "W":
                self.direction = (-1, 0)
            elif direction == "N":
                self.direction = (0, -1)
        else:
            self.direction = direction

        self.init = False

    def on_tick(self, time=None, frame_time=None):
        if not self.init and time is not None:
            if self.user.moving:
                print("Entity is already moving!")
                raise Exception("Entity is already moving!")

            colcheck = self.user.check_collision(self.direction)

            self.anim = BaseMoveAnimation(self.game, time, self.direction, self.user)
            if self.act.game.m_ani.add_animation(self.anim):
                self.user.moving = True
                self.init = True

        if not self.anim.ended or not self.init:
            return False
        return True

    def on_read(self):
        return None
