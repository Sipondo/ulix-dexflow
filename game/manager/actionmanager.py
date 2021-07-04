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

    def create_region(self, pos, size, region):
        region = {k[2:]: v for k, v in region.items() if "f_" in k}
        # print(
        #     "REGION CREATE:", regiontype, pos, size, region,
        # )
        self.regions.append(
            RegionRectangle(self.game, pos[0], pos[1], size[0], size[1], region)
        )

    def check_regions(self, entity):
        # pos = (pos[0] + self.game.m_col.offset[0], pos[1] + self.game.m_col.offset[1])
        for region in self.regions:
            region.check(entity)

    def flush_regions(self):
        self.regions.clear()


class RegionRectangle:
    def __init__(self, game, x, y, w, h, region):
        self.game = game
        self.x = x
        self.y = y

        for k, v in region.items():
            # print(type(v), v)
            if isinstance(v, (int, float, str)):
                setattr(self, k, eval(str(v)) if "[" in str(v) else v)
            else:
                setattr(self, k, v)

        if hasattr(self, "target_direction"):
            if self.target_direction == "E":
                self.x = self.x + 1
                self.target_location = (
                    self.target_location[0] - 1,
                    self.target_location[1],
                )
            elif self.target_direction == "S":
                self.y = self.y + 1
                self.target_location = (
                    self.target_location[0],
                    self.target_location[1] - 1,
                )
            elif self.target_direction == "W":
                self.x = self.x - 1
                self.target_location = (
                    self.target_location[0] + 1,
                    self.target_location[1],
                )
            elif self.target_direction == "N":
                self.y = self.y - 1
                self.target_location = (
                    self.target_location[0],
                    self.target_location[1] + 1,
                )

        self.x2 = self.x + w - 1
        self.y2 = self.y + h - 1

    def check(self, entity):
        pos = entity.get_pos()
        if (self.x <= pos[0] <= self.x2) and (self.y <= pos[1] <= self.y2):
            self.target = entity
            print("TRIGGER")
            self.on_enter(entity)

    def on_enter(self, entity):
        self.game.m_upl.parse(self, self.on_enter_action)
