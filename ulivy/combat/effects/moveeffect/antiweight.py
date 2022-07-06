from .basemoveeffect import BaseMoveEffect


class Antiweight(BaseMoveEffect):
    def before_action(self):
        target_actor = self.scene.board.get_actor(self.move.target)
        target_weight = target_actor.data["weight"]
        if target_weight < 10:
            self.move.power = 20
            return True, False, False
        if target_weight < 25:
            self.move.power = 40
            return True, False, False
        if target_weight < 50:
            self.move.power = 60
            return True, False, False
        if target_weight < 100:
            self.move.power = 80
            return True, False, False
        if target_weight < 200:
            self.move.power = 100
            return True, False, False
        self.move.power = 120
        return True, False, False
