from .basemoveeffect import BaseMoveEffect


class Antiminimize(BaseMoveEffect):
    def before_action(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if "Minimize" in [x.name for x in target_effects]:
            self.move.perfect_accuracy = True
            self.move.power *= 2
        return True, False, False

