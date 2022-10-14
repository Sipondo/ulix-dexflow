from copy import deepcopy
import enum


class Input(enum.Enum):
    NONE = enum.auto()
    TURN = enum.auto()


class CombatBoard:
    def __init__(self):
        self.change = "No change description available."
        self.parent = None
        self.required_input = Input.NONE

        self.teams = []
        t = [
            {
                "name": "-",
            }
        ] * 6
        self.teams.append(t)

        t = [
            {
                "name": "-",
            }
        ] * 6
        self.teams.append(t)

        self.actives = (0, 0)

    def copy(self):
        b = CombatBoard()
        b.teams = deepcopy(self.teams)
        b.actives = self.actives
        b.required_input = self.required_input
        b.parent = self
        return b

    def set_team(self, team_id, team):
        entry = []

        for t in team:
            if isinstance(t, dict):
                entry.append(t)
            else:
                entry.append(t.to_dict())

        b = self.copy()
        b.teams[team_id] = entry
        b.change = f"Team changed: team_id {team_id} swapped from \n{self.teams[team_id]} to \n{entry}"
        return b

    def set_required_input(self, input):
        b = self.copy()
        b.required_input = input
        b.change = f"Required input changed: {self.required_input} to {input}"
        return b

    def get_active_m(self, team_id):
        return self.teams[team_id][self.actives[team_id]]
