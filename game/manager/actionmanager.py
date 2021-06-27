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

    def create_region(
        self, regiontype, pos, size, target_direction, target_level, target_location
    ):
        print(
            "REGION CREATE:",
            regiontype,
            pos,
            size,
            target_direction,
            target_level,
            target_location,
        )
        self.regions.append(RegionRectangle(pos[0], pos[1], size[0], size[1]))

    def check_regions(self, pos):
        # pos = (pos[0] + self.game.m_col.offset[0], pos[1] + self.game.m_col.offset[1])
        for region in self.regions:
            region.check(pos)


class RegionRectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.x2 = x + w
        self.y2 = y + h

        print(self.x, self.x2, self.y, self.y2)

    def check(self, pos):
        print(pos, "versus", self.x, self.x2, self.y, self.y2)
        if (self.x < pos[0] <= self.x2) and (self.y < pos[1] <= self.y2):
            print("TRIGGER")
