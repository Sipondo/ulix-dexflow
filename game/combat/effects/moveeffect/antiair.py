from .basemoveeffect import BaseMoveEffect


class Antiair(BaseMoveEffect):
    def before_action(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if air_effect := [x for x in target_effects if x.name in ("Bounce", "Fly", "Skydrop")]:
            air_effect[0].skip = True
            self.move.power *= 2
        return True
