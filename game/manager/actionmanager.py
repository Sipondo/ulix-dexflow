from collections import deque


class ActionManager:
    def __init__(self, game):
        self.game = game
        self.actions = []
        self.queue = deque()

        self.regions = []

    def on_tick(self, time, frame_time):
        self.queue.clear()
        to_clear = []
        for act in self.actions:
            self.queue.append(act)
        while len(self.queue) != 0:
            act = self.queue.popleft()
            if act.on_tick(time, frame_time):
                to_clear.append(act)

        for act in to_clear:
            self.actions.remove(act)
            del act

    def create_region(self, pos, size, region):
        region = {k[2:]: v for k, v in region.items() if "f_" in k}
        # print(
        #     "REGION CREATE:", regiontype, pos, size, region,
        # )
        self.regions.append(
            RegionRectangle(self.game, pos[0], pos[1], size[0], size[1], region)
        )

    def check_regions(self, entity):
        print("REGION CHECK")
        # pos = (pos[0] + self.game.m_col.offset[0], pos[1] + self.game.m_col.offset[1])
        for region in self.regions:
            region.check(entity)

    def flush_regions(self):
        self.regions.clear()


class Action:
    def __init__(self, game, tree, user):
        self.game = game
        self.tree = tree
        self.user = user

        self.pointer = 0
        self.funcs = []
        self.run()

    def run(self):
        self.game.m_upl.parse(self, self.user, self.tree)

    def on_tick(self, time=None, frame_time=None):
        # print("HEY!")
        return True


class RegionRectangle:
    def __init__(self, game, x, y, w, h, region):
        self.game = game
        self.x = x
        self.y = y
        self.containing = set()

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
            if entity not in self.containing:
                self.target = entity
                print("TRIGGER ENTER", self.x, pos[0], self.x2, self.y, pos[1], self.y2)
                self.on_enter(entity)
        else:
            if entity in self.containing:
                print("TRIGGER EXIT", self.x, pos[0], self.x2, self.y, pos[1], self.y2)
                self.on_exit(entity)

    def on_enter(self, entity):
        self.containing.add(entity)
        self.game.m_act.actions.append(Action(self.game, self.on_enter_action, self))
        # self.game.m_upl.parse(self, self.on_enter_action)

    def on_exit(self, entity):
        # print("on_exit:", self, entity)
        self.containing.remove(entity)
        self.game.m_act.actions.append(Action(self.game, self.on_exit_action, self))
        # self.game.m_upl.parse(self, self.on_exit_action)
