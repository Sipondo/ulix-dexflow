from collections import deque


class ActionManager:
    def __init__(self, game):
        self.game = game
        self.animations = []
        self.queue = deque()

        self.regions = []

    def on_tick(self, time, frame_time):
        locked = False
        self.queue.clear()
        for anim in self.animations:
            self.queue.append(anim)
        while len(self.queue) != 0:
            if self.queue.popleft().on_tick(time, frame_time):
                locked = True
        return locked

    def create_region(self, regiontype, pos, size, region):
        region = {k[2:]: v for k, v in region.items() if "f_" in k}
        print(
            "REGION CREATE:", regiontype, pos, size, region,
        )
        self.regions.append(
            RegionRectangle(self.game, pos[0], pos[1], size[0], size[1], region)
        )

    def check_regions(self, entity):
        # pos = (pos[0] + self.game.m_col.offset[0], pos[1] + self.game.m_col.offset[1])
        for region in self.regions:
            region.check(entity)


class RegionRectangle:
    def __init__(self, game, x, y, w, h, region):
        self.game = game
        self.x = x
        self.y = y
        self.x2 = x + w
        self.y2 = y + h

        for k, v in region.items():
            setattr(self, k, v)

        # print(
        #     self.x,
        #     self.x2,
        #     self.y,
        #     self.y2,
        #     self.target_level,
        #     self.target_coords,
        #     self.direction,
        #     self.on_enter_action,
        #     self.on_exit_action,
        # )

    def check(self, entity):
        pos = entity.get_pos()
        # print(pos, "versus", self.x, self.x2, self.y, self.y2)
        if (self.x < pos[0] <= self.x2) and (self.y < pos[1] <= self.y2):
            self.on_enter(entity)

    def on_enter(self, entity):
        self.game.m_upl.parse(self, self.on_enter_action)
        print("TRIGGER")
