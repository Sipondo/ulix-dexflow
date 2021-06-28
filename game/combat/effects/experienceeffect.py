from .baseeffect import BaseEffect


class ExperienceEffect(BaseEffect):
    def __init__(self, scene, target, amount):
        super().__init__(scene)
        self.spd_on_action = 100
        self.target = target
        self.amount = amount

    def on_action(self):
        # TODO gain experience from battle
        self.scene.board.no_skip(f"{self.scene.board.get_actor(self.target).name} gained {self.amount} experience", particle="")
        return True, False, False
