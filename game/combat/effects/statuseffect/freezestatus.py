from game.combat.effects.baseeffect import BaseEffect


class Freeze(BaseEffect):
    name = "Freeze"
    particle = "freeze"
    type = "Majorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "is frozen solid"
        self.spd_on_action = 11
        self.target = target

    def on_action(self):
        if self.scene.board.user == self.target:
            if self.scene.board.action.action_name == "attack":
                if self.scene.board.action.type == "Fire" and self.scene.board.action.power > 0:
                    self.scene.board.no_skip(
                        f"{self.scene.board.get_actor(self.target).name} thawed out!",
                        particle=self.name,
                    )
                    return True, False, False
                else:
                    self.scene.board.no_skip(
                        f"{self.scene.board.get_actor(self.target).name} is frozen solid!",
                        particle=self.name,
                    )
                    return False, True, False
        return False, False, False
