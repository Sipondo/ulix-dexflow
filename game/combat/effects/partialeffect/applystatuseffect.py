from .basepartialeffect import BasePartialEffect
from game.combat.effects.genericeffect import GenericEffect


class ApplyStatus(BasePartialEffect):
    def __init__(self, scene, status, user, target):
        super().__init__(scene)
        self.status = status
        self.user = user
        self.target = target
        print(self.user, self.target)

    def apply(self):
        target_effects = self.scene.get_effects_on_target(self.target)
        if self.status.type == "Majorstatus":
            if "Majorstatus" not in [x.type for x in target_effects]:
                self.scene.board.inflict_status(self.status, self.user, self.target)
        elif self.status.name not in [x.name for x in target_effects]:
            self.scene.board.inflict_status(self.status, self.user, self.target)
        self.scene.board.no_skip("But it failed", particle="")

    def on_faint(self, target):
        return self.target == target, False, False
