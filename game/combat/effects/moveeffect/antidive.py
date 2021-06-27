from .basemoveeffect import BaseMoveEffect


class Antidive(BaseMoveEffect):
    def before_move(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if dive_effect := [x for x in target_effects if x.name == "Dive"]:
            dive_effect[0].skip = True
            self.move.power *= 2
            return True
