from game.combat.effects.baseeffect import BaseEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Drowsy(BaseEffect):
    name = "Drowsy"
    particle = ""
    type = "Minorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "got drowsy"
        self.user = user
        self.target = target
        self.counter = 5

    def before_end(self):
        if self.counter == 0:
            ApplyStatus(self.scene.board, statuseffect.SLEEP, self.user, self.target).apply()
            return True, False, False
        self.counter -= 1
        return False, False, False

    def on_switch(self, target_old, target_new):
        return target_old == self.target, False, False

    def on_faint(self, target):
        return self.target == target, False, False
