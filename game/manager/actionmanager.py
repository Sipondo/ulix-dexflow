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
        print("ACTION INIT")
        self.game = game
        self.tree = tree
        self.user = user

        self.has_run = False

        self.pointer = 0
        self.funcs = []

        self.children = []

        print("I AM:", self.tree.data)
        if self.tree.data == "upl":
            for child in self.tree.children:
                self.children.append(Action(self.game, child, self.user))
        if self.tree.data == "control":
            print(self.tree.pretty())
            raise Exception
        # else
        # self.run()

        print("FUNCS ARE:", self.tree.data, self.funcs)

    def run(self):
        self.has_run = True
        self.game.m_upl.parse(self, self.user, self.tree)

    def on_tick(self, time=None, frame_time=None):
        self.current_time = time

        if self.funcs:
            # Need funcs to clear
            funcs_to_clear = []
            for func in self.funcs:
                if func.on_tick(time, frame_time):
                    funcs_to_clear.append(func)

            for func in funcs_to_clear:
                self.funcs.remove(func)
                del func

        # If no functions left
        if not self.funcs:
            # No children
            if not (self.children or self.has_run):
                self.has_run = True
                self.run()
                return False

            # Children
            elif self.pointer < len(self.children):
                while (self.pointer < len(self.children)) and self.children[
                    self.pointer
                ].on_tick(time, frame_time):
                    print("NEXT CHILD!!!")
                    self.pointer += 1
                return False

        return not self.funcs


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
