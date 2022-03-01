"""fobject
Calculates the Manhattan distance between two points.

Calculates the Manhattan distance between two points. The points have to be supplied as tuples.

in:
- Tuple of numerics of length two: point a
- Tuple of numerics of length two: point b

out:
- Numeric: Manhattan distance between points a and b

"""


class Manhattan:
    def __init__(self, act, src, user, a, b):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.a = a
        self.b = b

    def on_read(self):
        return abs(self.a[0] - self.b[0]) + abs(self.a[1] - self.b[1])

