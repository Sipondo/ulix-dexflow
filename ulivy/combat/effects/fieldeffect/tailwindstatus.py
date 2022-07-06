from ulivy.combat.effects.baseeffect import BaseEffect
from ulivy.combat.effects.genericeffect import GenericEffect


class Tailwind(BaseEffect):
    name = "Tailwindstatus"
    particle = ""
    type = "Minorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "set up a wind blowing from behind"
        self.target = target[0]
        self.counter = 4

    def before_end(self):
        if self.counter == 0:
            self.scene.add_effect(GenericEffect(self.scene, f"The tailwind ended"))
            return True, False, False
        self.counter -= 1
        return False, False, False

    @property
    def stat_mod(self):
        return [1, 1, 1, 1, 2, 1, 1]
