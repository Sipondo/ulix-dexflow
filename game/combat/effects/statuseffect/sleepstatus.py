from game.combat.effects.baseeffect import BaseEffect


class Sleep(BaseEffect):
    name = "Sleep"
    particle = "sleep"
    type = "Majorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "fell asleep"
        self.spd_on_action = 10
        self.target = target
        self.counter = self.scene.board.random_int(1, 5)

    def on_action(self):
        if self.scene.board.user == self.target:
            if self.scene.board.action.action_name == "attack":
                if self.counter == 0:
                    self.scene.board.no_skip(
                        f"{self.scene.board.get_actor(self.target).name} woke up!",
                        particle=self.name,
                    )
                    return True, False, False
                else:
                    self.scene.board.no_skip(
                        f"{self.scene.board.get_actor(self.scene.board.user).name} is fast asleep!",  # for {self.counter} more turns!",
                        particle=self.name,
                    )
                    self.counter -= 1
                    return False, True, False
        return False, False, False
