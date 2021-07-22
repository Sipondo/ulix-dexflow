class SetMovement:
    def __init__(self, act, src, user, movement):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.movement = movement

    def on_tick(self, time=None, frame_time=None):
        self.user.set_movement_type(int(self.movement))
        return True
