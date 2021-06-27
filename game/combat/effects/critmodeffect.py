from game.combat.effects.baseeffect import BaseEffect


class CritModEffect(BaseEffect):
    name = "Critmod"

    def __init__(self, scene, target, level):
        super().__init__(scene)
        self.target = target
        self.level = level

    def update(self, level):
        self.level += level

    def get_crit_mod(self):
        return self.level
