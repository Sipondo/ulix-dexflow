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
        # print("REGION CHECK")
        # pos = (pos[0] + self.game.m_col.offset[0], pos[1] + self.game.m_col.offset[1])
        for region in self.regions:
            region.check(entity)

    def flush_regions(self):
        self.regions.clear()


class Action:
    def __init__(self, game, tree, user, parent=None):
        # print("ACTION INIT")
        self.game = game
        self.tree = tree
        self.user = user
        self.parent = parent

        self.data = self.tree.data

        self.has_run = False

        self.pointer = 0
        self.funcs = []
        self.repeats = 0
        self.terminated = False

        self.children = []
        self.elsechildren = []

        self.trigger_else = False
        self.active_children = []

        # print("I AM:", self.tree.data)
        self.init_children(include_else=True)
        # else
        # self.run()

        # print("CHILDREN:", self.tree.data, self.children)

    def init_children(self, include_else=True):
        self.pointer = 0
        self.children = []
        if include_else:
            self.elsechildren = []

        if self.tree.data == "upl":
            for child in self.tree.children:
                self.children.append(Action(self.game, child, self.user, self))
        elif self.tree.data in ("control_group", "concurrent", "try"):
            self.children.append(
                Action(self.game, self.tree.children[0], self.user, self)
            )
        elif self.tree.data in (
            "control_if",
            "control_while",
            "control_repeat",
            "control_group",
        ):
            self.children.append(
                Action(self.game, self.tree.children[1], self.user, self)
            )
            if include_else and len(self.tree.children) > 2:
                self.elsechildren.append(
                    Action(self.game, self.tree.children[2], self.user, self)
                )
                # print("Elsechildren!", self.elsechildren)
            # print("CHILDREN OF IF:", [x.data for x in self.children])
            # print("CHILDREN OF IF:", [x.data for x in self.elsechildren])

    def run(self):
        self.has_run = True
        # print("Running:", self.data)
        if self.data == "upl":
            return True
        elif self.tree.data == "control_group":
            return True
        elif self.tree.data == "concurrent":
            return True
        elif self.tree.data == "try":
            return True
        elif self.tree.data == "control_repeat":
            self.repeats += 1
            # print(
            #     "Control repeat!", self.elsechildren
            # )  # [x.data for x in self.tree.children])
            con = self.game.m_upl.parse(self, self.user, self.tree.children[0])
            return self.repeats <= con[0]
        elif self.tree.data in ("control_if", "control_while",):
            # print("Control while!", self.elsechildren)
            con = self.game.m_upl.parse(self, self.user, self.tree.children[0])
            # print("Alive?")
            # print(self.data, con)
            return con[0]
        return self.game.m_upl.parse(self, self.user, self.tree)

    def terminate(self):
        self.terminated = True
        if self.parent is not None:
            self.parent.terminate()

    def on_tick(self, time=None, frame_time=None):
        # print("TICK ON", self.data)
        # print(self.funcs, self.active_children, [x.data for x in self.active_children])
        if self.terminated:
            return True
        self.current_time = time

        # Whether the current loop had any exceptions
        raised_exception = False

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
                self.run()
                return False

            # Children
            else:
                # Process running children
                children_to_clear = []
                for child in self.active_children:
                    if self.data == "try":
                        try:
                            if child.on_tick(time, frame_time):
                                children_to_clear.append(child)
                        except Exception as e:
                            raised_exception = True
                            children_to_clear.append(child)
                    else:
                        if child.on_tick(time, frame_time):
                            children_to_clear.append(child)

                for child in children_to_clear:
                    self.active_children.remove(child)

                if raised_exception:
                    return True

                # Visit elsechildren
                if self.trigger_else:
                    if not self.pointer < len(self.elsechildren):
                        #     return False

                        # Visits
                        take_next_child = not len(self.active_children)
                        while (
                            self.pointer < len(self.elsechildren)
                        ) and take_next_child:
                            print("NEXT ELSECHILD!!!")
                            if self.pointer < len(self.elsechildren):
                                child = self.elsechildren[self.pointer]
                                self.active_children.append(child)
                                if child.data != "concurrent":
                                    take_next_child = False
                                self.pointer += 1
                        return False

                # Visit normal children
                elif self.pointer < len(self.children):
                    # Check if new visit is required
                    if (
                        self.tree.data
                        in (
                            "control_if",
                            "control_while",
                            "control_repeat",
                            "control_group",
                            "concurrent",
                        )
                        and not self.has_run
                    ):
                        if not self.run():
                            if self.elsechildren:
                                self.trigger_else = True
                                self.pointer = 0
                                return False
                            else:
                                return True

                    # Visits
                    take_next_child = not len(self.active_children)
                    while (self.pointer < len(self.children)) and take_next_child:
                        if self.pointer < len(self.children):
                            child = self.children[self.pointer]
                            self.active_children.append(child)
                            if child.data != "concurrent":
                                take_next_child = False
                            self.pointer += 1
                    return False

                # Repeat when done
                elif self.has_run and self.data in ("control_while", "control_repeat",):
                    self.has_run = False
                    self.init_children(include_else=False)
                    return False

        # Return True (exit) if nothing left to process
        # if self.data == "control_repeat":
        #     print("REPEAT END-RETURNING:", not self.funcs and not self.active_children)
        return not self.funcs and not self.active_children


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
