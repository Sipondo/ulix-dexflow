class Debug:
    def __init__(self, act, src, user, obj):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.obj = obj
        self.src = src
        self.user = user
        self = user

    def on_tick(self, time=None, frame_time=None):
        print("DEBUG:", self.act.current_time, self.obj)
        return True

    def on_read(self):
        return None
