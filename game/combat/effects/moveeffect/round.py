from .basemoveeffect import BaseMoveEffect


class Round(BaseMoveEffect):
    def __init__(self, scene, move):
        super().__init__(scene, move)
        self.doubles = False

    def on_action(self):
        if self.scene.board.action["name"] == self.move.name:
            self.doubles = True
        if self.scene.board.action.user == self.move.user:
            return True, False, False
        return False, False, False

    def after_action(self):
        if self.doubles:
            self.move.power *= 2
        return False, False, False
