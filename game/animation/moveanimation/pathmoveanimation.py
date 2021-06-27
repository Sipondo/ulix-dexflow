from .basemoveanimation import BaseMoveAnimation


class PathMoveAnimation(BaseMoveAnimation):
    def __init__(self, game, start, direction, entity, distance=1, lock=False, path=[]):
        self.path = path
        super().__init__(game, start, direction, entity, distance, lock=True)

    def continue_move(self, time, frame_time):
        self.start = time
        self.stop = self.start + self.duration
        # print(self.path)
        self.direction = self.path.pop(0)
        self.on_enter()

    def conditions(self):
        return self.entity.check_collision(self.path[0])
