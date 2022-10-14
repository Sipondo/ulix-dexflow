from ulivy.c2.combatboard import CombatBoard


class CombatManager:
    def __init__(self, game):
        self.game = game
        self.board_pointer = 0

    def init_new_stack(self):
        self.boards = [CombatBoard()]

    def advance(self):
        if self.board_pointer == len(self.boards) - 1:
            return False
        self.board_pointer += 1
        print(f"Advancing ({self.board_pointer}): {self.b.change}")

        if self.board_pointer == len(self.boards) - 1:
            return False
        return True

    def set_team(self, team_id, team):
        self.boards.append(self.board_head.set_team(team_id, team))

    def set_required_input(self, input):
        self.boards.append(self.board_head.set_required_input(input))

    @property
    def b(self):
        return self.board_current

    @property
    def board_current(self):
        return self.boards[self.board_pointer]

    @property
    def board_head(self):
        return self.boards[-1]
