class Debug:
    def __init__(self, act, user, obj):
        act.funcs.append(self)
        self = user
        print("DEBUG:", obj)

    def on_tick(self, time=None, frame_time=None):
        return True
