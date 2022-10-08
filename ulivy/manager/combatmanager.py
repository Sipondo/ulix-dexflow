from ulivy.c2.combatboard import CombatBoard


class CombatManager:
    def __init__(self, game):
        self.game = game
        self.board_pointer = 0

    def init_new_combat(self):
        self.boards = [CombatBoard()]

    def advance(self):
        if self.board_pointer == len(self.boards) - 1:
            return False
        self.board_pointer += 1
        return True

    @property
    def current_board(self):
        return self.boards[self.board_pointer]
