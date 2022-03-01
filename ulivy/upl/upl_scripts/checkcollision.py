"""fobject
Check collision at position.

Check the collision flags at the specified position.

in:
- Numeric: x position to check
- Numeric: y position to check
- Numeric: height to check

out:
- Bool: whether there is collision at the specified position

"""


class CheckCollision:
    def __init__(self, act, src, user, x, y, h):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.x = x
        self.y = y
        self.h = h

    def on_read(self):
        return self.game.m_col.get_col_flag(
            (int(self.x), int(self.y)), int(self.h), off=False, check_entities=False
        )
