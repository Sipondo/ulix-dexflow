from .basemoveeffect import BaseMoveEffect


class Antidmgdealt(BaseMoveEffect):
    def __init__(self, scene, move):
        super().__init__(scene, move)
        self.doubles = False

    def on_damage(self, dmg):
        if self.scene.board.target == self.move.target:
            self.doubles = True

    def before_action(self):
        if self.doubles:
            self.move.power *= 2
        return True
