import enum

from dataclasses import replace, dataclass
from .combatteam import CombatTeam
from .combatfighter import CombatFighter


class Input(enum.Enum):
    NONE = enum.auto()
    TURN = enum.auto()


@dataclass(frozen=True)
class CombatBoard:
    change = "No change description available."
    parent = None
    required_input = Input.NONE
    teams = (CombatTeam(), CombatTeam())
    actives = (0, 0)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def copy(self, **changes):
        return replace(self, **changes)

    def set_team(self, team_id, team):
        entry = []

        for t in team:
            if isinstance(t, dict):
                entry.append(t)
            else:
                entry.append(t.to_dict())

        new_team = CombatTeam(members=tuple(CombatFighter(**x) for x in entry))

        teams = list(self.teams)
        teams[team_id] = new_team  # teams[team_id].copy(**changes)

        b = self.copy(
            teams=tuple(teams),
            change=f"Team changed: team_id {team_id} changed to {new_team}",
            # change=f"Team changed: team_id {team_id} swapped from \n{self.teams[team_id]} to \n{entry}",
        )
        # b.teams[team_id] = entry  # TODO: fix
        return b

    def set_required_input(self, input):
        return self.copy(
            required_input=input,
            change=f"Required input changed: {self.required_input} to {input}",
        )

    def get_active_m(self, team_id):
        print(self.teams)
        print(self.teams[0])
        print(self.teams[1])
        return self.teams[team_id].members[self.actives[team_id]]
