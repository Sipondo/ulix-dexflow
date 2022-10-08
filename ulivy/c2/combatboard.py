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

    def copy(self):
        b = CombatBoard()
