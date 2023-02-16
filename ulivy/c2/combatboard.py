import enum

from dataclasses import replace, dataclass, fields
from .combatteam import CombatTeam
from .combatfighter import CombatFighter

from ulivy.c2.action import ActionType, Action


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
        changes = {**self.__dict__, **changes}
        return replace(self, **changes)

    def set_team(self, team_id, team):
        entry = []

        for t in team:
            if isinstance(t, dict):
                entry.append(t)
            else:
                entry.append(t.to_dict())

        teams = list(self.teams)

        new_team = CombatTeam(members=tuple(CombatFighter(**x) for x in entry))
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
        if self.actives[team_id] < len(self.teams[team_id].members):
            return self.teams[team_id].members[self.actives[team_id]]
        return None

    def set_action(self, action: Action):
        if self.required_input == Input.TURN:
            return self.copy(
                required_input=Input.NONE,
                change=f"Required input changed: {self.required_input} to {input}",
            )
        else:
            raise Exception(
                f"Combatboard received unexpected input even though {self.required_input} was expected!"
            )
