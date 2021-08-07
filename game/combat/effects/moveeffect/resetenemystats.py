from .basemoveeffect import BaseMoveEffect


class Resetenemystats(BaseMoveEffect):
    def after_move(self):
        if statmod_effect := [x for x in self.scene.get_effects_on_target(self.move.target) if x.name == "Statmod"]:
            self.scene.delete_effect(statmod_effect)
        return True