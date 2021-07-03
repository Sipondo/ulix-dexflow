import random


class CombatBoard:
    def __init__(self, scene):
        self.scene = scene
        self.actives = []
        self.teams = []
        self.actor = -1
        self.action = None
        self.narration = "Board state undefined."
        self.particle = ""
        self.user = None
        self.target = None
        self.skip = True
        self.particle_miss = False
        self.battle_end = False

    def first_init(self, *teams):
        for team in teams:
            self.teams.append([(x, x.current_hp) for x in team])
            self.actives.append(0)

    def from_board(self, board):
        for index, team in enumerate(board.teams):
            self.teams.append([])
            for member in team:
                member = (member[0], member[1])
                self.teams[index].append(member)
        self.actives = board.actives.copy()
        self.action = board.action
        self.user = board.user
        self.target = board.target

    def copy(self):
        newstate = CombatBoard(self.scene)
        newstate.from_board(self)
        return newstate

    def reset_action(self):
        self.action = None
        self.user = None
        self.target = None

    def set_direction(self, action):
        # Mostly for particles
        # TODO: possibly move into particle attribute
        if hasattr(action, "user"):
            self.user = action.user
        if hasattr(action, "target"):
            self.target = action.target

    def get_actor(self, target):
        # Get actor from (action) tuple
        return self.teams[target[0]][target[1]][0]

    def get_hp(self, target):
        return self.teams[target[0]][target[1]][1]

    def get_action_priority(self, action):
        # TODO: not just priority
        return action.priority

    def random_int(self, a, b):
        return random.randint(a, b)

    def random_roll(self):
        return random.random()

    def no_skip(self, narration, particle=None, battle_end=False, particle_miss=False):
        self.narration = narration
        self.skip = False
        self.particle = particle
        self.battle_end = battle_end
        self.particle_miss = particle_miss

    def set_hp(self, target, hp):
        self.teams[target[0]][target[1]][1] = hp

    def set_active(self, new_active):
        self.actives[new_active[0]] = new_active[1]

    def set_particle(self, particle):
        self.particle = particle

    def is_active(self, target):
        return target[1] == self.actives[0]

    def is_user(self, user):
        return self.user[0] == user[0] and self.user[1] == user[1]

    def get_active(self, team):
        return self.actives[team]

    def get_team_size(self, team):
        return len(self.teams[team])

    def get_relative_hp(self, target):
        return (
            self.teams[target[0]][target[1]][1]
            / self.teams[target[0]][target[1]][0].stats[0]
        )

    def get_relative_xp(self, target):
        return (
            self.teams[target[0]][target[1]][0].current_xp
            / self.teams[target[0]][target[1]][0].level_xp
        )

    @property
    def actor_1(self):
        return self.teams[0][self.actives[0]]

    @property
    def actor_2(self):
        return self.teams[1][self.actives[0]]
