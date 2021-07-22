class Debug:
    def __init__(self, act, src, user, obj):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.obj = obj
        self.src = src
        self.user = user
        self = user
        print("DEBUG:", act.current_time, obj)

    def on_tick(self, time=None, frame_time=None):
        if time - self.init_time < 0:
            return False
        return True
