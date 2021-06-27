from game.combat.effects.baseeffect import BaseEffect
from game.combat.effects.genericeffect import GenericEffect


class Safeguard(BaseEffect):
    name = "Safeguardstatus"
    particle = ""
    type = "Minorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "got protected from harm"
        self.target = target
        self.counter = 6

    def before_end(self):
        if self.counter == 0:
            self.scene.add_effect(
                GenericEffect(self.scene, f"{self.scene.board.get_actor(self.target).name}'s safeguard wore off"))
            return True, False, False
        self.counter -= 1
        return False, False, False

    def on_status(self, target):
        if target == self.target:
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.scene.board.get_actor(self.target).name} is protected from harm!",
                )
            )
            return True
        return False
