from .basemoveeffect import BaseMoveEffect


class Resetallstats(BaseMoveEffect):
    def after_action(self):
        for statmod_effect in [x for x in self.scene.get_effects() if x.name == "Statmod"]:
            self.scene.delete_effect(statmod_effect)
        return True
