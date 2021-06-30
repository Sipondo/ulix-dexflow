from .baseeffect import BaseEffect


class BallEffect(BaseEffect):
    def __init__(self, scene, move):
        super().__init__(scene)
        self.spd_on_action = 100
        self.move = move
        self.user = move.user
        self.target = move.target
        self.ball = move.action_data

    def on_action(self):
        print("BALL:", self.ball)
        return True, False, False
