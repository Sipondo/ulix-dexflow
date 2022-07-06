"""function
Pause action execution.

Pause action execution by the specified amount of time. Input is in seconds and may be floating point.

in:
- Numeric: seconds to wait

"""


class Wait:
    def __init__(self, act, src, user, time):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.time = time

    def on_tick(self, time=None, frame_time=None):
        if time - self.init_time < self.time:
            return False
        return True

    def on_read(self):
        return None
