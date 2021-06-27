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
        if self.entity.check_collision(self.path[0]):
            return True
        path = self.game.m_col.a_star(
            self.entity.game_position,
            (27 - self.game.m_col.offset[0], 12 - self.game.m_col.offset[1]),
            # (self.game_position[0] - 5, self.game_position[1] - 8),
            next_to=True,
        )
        if path is not None:
            self.path = path
            self.distance = len(self.path)
            return True
        return False
