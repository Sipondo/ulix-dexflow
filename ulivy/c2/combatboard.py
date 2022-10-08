from copy import deepcopy


class CombatBoard:
    def __init__(self):
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

    def set_team(self, team_id, team):
        entry = []

        for t in team:
            if isinstance(t, dict):
                entry.append(t)
            else:
                entry.append(t.to_dict())

        b = self.copy()
        b.teams[team_id] = entry
        print(b.teams)
        return b

    def copy(self):
        b = CombatBoard()
        b.teams = deepcopy(self.teams)
        return b
