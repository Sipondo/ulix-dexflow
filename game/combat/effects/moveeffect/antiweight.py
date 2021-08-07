from .basemoveeffect import BaseMoveEffect


class Antiweight(BaseMoveEffect):
    def before_move(self):
        target_actor = self.scene.get_actor(self.move.target)
        target_weight = target_actor.data["weight"]
        if target_weight < 10:
            self.move.power = 20
            return True
        if target_weight < 25:
            self.move.power = 40
            return True
        if target_weight < 50:
            self.move.power = 60
            return True
        if target_weight < 100:
            self.move.power = 80
            return True
        if target_weight < 200:
            self.move.power = 100
            return True
        self.move.power = 120
        return True
