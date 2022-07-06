from .basemoveeffect import BaseMoveEffect


class Antiparalyze(BaseMoveEffect):
    def before_action(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if "Paralysis" in [x.name for x in target_effects]:
            self.move.power *= 2
        return True, False, False
