from game.combat.effects.baseeffect import BaseEffect
from game.combat.effects.genericeffect import GenericEffect


class Infatuation(BaseEffect):
    name = "Infatuation"
    particle = ""
    type = "Minorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.spd_on_action = 5
        self.user = user
        self.target = target
        self.apply_narration = "fell in love"

    def on_action(self):
        if self.scene.board.user == self.target:
            if self.scene.board.action.action_name == "attack":
                self.scene.board.no_skip(
                    f"{self.scene.board.get_actor(self.target).name} is in love with foe {self.scene.board.get_actor(self.user).name}!",
                    particle=self.name,
                )
                if self.scene.board.random_roll() < 0.5:
                    self.scene.add_effect(
                        GenericEffect(
                            self.scene,
                            f"{self.scene.board.get_actor(self.target).name} was immobilized by love!",
                        )
                    )
                    return False, True, False
        return False, False, False

    def on_switch(self, target_old, target_new):
        if target_old == self.user or target_old == self.target:
            return True, False, False

