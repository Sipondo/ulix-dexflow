from .basemoveanimation import BaseMoveAnimation


class PathMoveAnimation(BaseMoveAnimation):
    def __init__(self, game, start, direction, entity, distance=1, lock=False, path=[]):
        self.path = path
        super().__init__(game, start, direction, entity, distance, lock=lock)

    def continue_move(self, time, frame_time):
        self.start = time
        # print(self.path)
        self.direction = self.path.pop(0)
        self.entity.direction = self.direction
        self.on_enter()

    def conditions(self):
        self.single_move_distance = 1
        res = self.entity.check_collision(self.path[0], flags=True)
        if res:
            self.single_move_distance = res[0]

        self.get_anim_data()
        return bool(res)

    def check_continue(self):
        self.game.m_act.check_regions(self.entity)
        if self.distance > 0:
            return True
        return False
