from ulivy.combat.effects.baseeffect import BaseEffect


class Paralysis(BaseEffect):
    name = "Paralysis"
    particle = "paralysis"
    type = "Majorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "was paralyzed"
        self.target = target
        self.spd_on_action = 1

    def on_action(self):
        if self.target == self.scene.board.user:
            if self.scene.board.random_roll(0.25):
                self.scene.board.no_skip(
                    f"{self.scene.board.get_actor(self.target).name} was fully paralyzed",
                    particle="Paralysis",
                )
                return False, True, False
        return False, False, False

    @property
    def stat_mod(self):
        return [1, 1, 1, 1, 0.5, 1, 1]
