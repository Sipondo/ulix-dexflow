from game.combat.effects.baseeffect import BaseEffect


class CurlEffect(BaseEffect):
    name = "Curl"

    def __init__(self, scene, target):
        super().__init__(scene)
        self.target = target

    def on_switch(self, target_old, target_new):
        return self.target == target_old, False, False

    def on_faint(self, target):
        return self.target == target, False, False
