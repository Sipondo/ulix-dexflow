"""function
Pushes a pillar, making the pillar fall down if above a gap.

Pushes a pillar in the given direction. The pillar becomes uninteractable and walkable if pushed into a hole.
Directions are given by single-letter capital-only strings `N` `W` `S` `E`.

in:
- String: direction to push to
- [Optional, 1] Numeric: distance that the movement should cover

"""


from ulivy.animation.moveanimation.basemoveanimation import BaseMoveAnimation


class Push:
    def __init__(self, act, src, user, direction, force=1):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.force = int(force)

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

        self.go_down = False

    def on_tick(self, time=None, frame_time=None):
        if not self.init and time is not None:
            if self.user.moving:
                print("Entity is already moving!")
                raise Exception("Entity is already moving!")

            colcheck = self.user.check_collision(self.direction)

            if not colcheck or colcheck[0] > 1:
                self.go_down = True

            self.anim = BaseMoveAnimation(
                self.game, time, self.direction, self.user, colcheck=False
            )
            if self.act.game.m_ani.add_animation(self.anim):
                self.user.moving = True
                self.init = True

        if not self.anim.ended or not self.init:
            return False

        if self.go_down:
            for _ in range(int(self.force) - 1):
                self.user.game_position = (
                    self.user.x_g + self.direction[0],
                    self.user.y_g + self.direction[1],
                )
            self.user.sprites = ["pillar_used"]
            self.user.render_priority = -1
            self.user.interactable = False
            self.user.col_override = True
        return True

    def on_read(self):
        return None
