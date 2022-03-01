from game.combat.effects.baseeffect import BaseEffect


class AutotomizeEffect(BaseEffect):
    name = "Autotomize"

    def __init__(self, scene, target):
        super().__init__(scene)
        self.target = target

    # TODO weight halved
