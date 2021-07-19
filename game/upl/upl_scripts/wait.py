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
