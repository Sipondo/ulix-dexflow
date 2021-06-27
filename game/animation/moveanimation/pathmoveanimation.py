from .basemoveanimation import BaseMoveAnimation


class PathMoveAnimation(BaseMoveAnimation):
    def __init__(self, game, start, direction, entity, distance=1, lock=False, path=[]):
        self.path = path
        super().__init__(game, start, direction, entity, distance, lock=True)

    def continue_move(self, time, frame_time):
        self.start = time
        self.stop = self.start + self.duration
        self.direction = self.path.pop()
        self.direction = (self.direction[0], -self.direction[1])
        self.on_enter()
