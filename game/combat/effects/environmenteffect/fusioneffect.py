from game.combat.effects.baseeffect import BaseEffect


class FusionEffect(BaseEffect):
    name = "Fusioneffect"

    def __init__(self, scene, move):
        super().__init__(scene)
        self.move = move
        self.target = "Global"
        self.action = 1

    def after_action(self):
        if self.action == 0:
            return True, False, False
        self.action -= 1
        return False, False, False
