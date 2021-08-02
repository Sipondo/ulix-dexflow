class Face:
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
        self.user.direction = self.direction
        self.user.current_sprite = (0, self.user.get_offset())
        return True

    def on_read(self):
        return None
