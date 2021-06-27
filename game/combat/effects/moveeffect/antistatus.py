from .basemoveeffect import BaseMoveEffect


class Antiselfstatus(BaseMoveEffect):
    def before_move(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if "Majorstatus" in [x.type for x in target_effects]:
            self.move.power *= 2
            return True
