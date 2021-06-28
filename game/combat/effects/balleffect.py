from .baseeffect import BaseEffect


class BallEffect(BaseEffect):
    def __init__(self, scene, move):
        super().__init__(scene)
        self.spd_on_action = 100
        self.move = move

    def on_action(self):
        return True, False, False
