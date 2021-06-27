from game.combat.effects.baseeffect import BaseEffect


class CurlEffect(BaseEffect):
    name = "Curl"

    def __init__(self, scene, target):
        super().__init__(scene)
        self.target = target

    def on_switch(self, target_old, target_new):
        if self.target == target_old:
            return True
        return False
