from game.combat.effects.baseeffect import BaseEffect
from game.combat.effects.genericeffect import GenericEffect


class Mist(BaseEffect):
    name = "Miststatus"
    particle = ""
    type = "Minorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "got protected from stat changes"
        self.target = target
        self.counter = 6

    def before_end(self):
        if self.counter == 0:
            self.scene.add_effect(GenericEffect(self.scene, f"{self.scene.board.get_actor(self.target).name}'s mist wore off"))
            return True, False, False
        self.counter -= 1
        return False, False, False

    def on_stat_change(self, target):
        if target == self.target:
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.scene.board.get_actor(self.target).name} is protected from stat changes!",
                )
            )
            return True
        return False
