from game.combat.effects.baseeffect import BaseEffect
from game.combat.effects.damageeffect import DamageEffect


class Confusion(BaseEffect):
    name = "Confusion"
    particle = "confusion"
    type = "Minorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "got confused"
        self.target = target
        self.counter = self.scene.board.random_int(1, 5)

    def on_action(self):
        if self.scene.board.user == self.target:
            if self.scene.board.action.action_name == "attack":
                if self.counter == 0:
                    self.scene.board.no_skip(
                        f"{self.scene.board.get_actor(self.target).name} snapped out of confusion!",
                        particle=self.name,
                    )
                    return True, False, False
                else:
                    self.scene.board.no_skip(
                        f"{self.scene.board.get_actor(self.target).name} is confused!",
                        # for {self.counter} more turns!",
                        particle=self.name,
                    )
                    if self.scene.board.random_roll(0.5):
                        self.scene.add_effect(DamageEffect(self.scene, self.target, ))
                    self.counter -= 1
                    return False, True, False
        return False, False, False

    def on_switch(self, old_target, new_target):
        return self.target == old_target, False, False

    def on_faint(self, target):
        return self.target == target, False, False
