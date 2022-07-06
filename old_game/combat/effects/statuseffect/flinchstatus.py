from game.combat.effects.baseeffect import BaseEffect


class Flinch(BaseEffect):
    name = "Flinch"
    particle = ""
    type = "Minorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.spd_on_action = 5
        self.target = target
        self.apply_narration = ""

    def before_action(self):
        if self.scene.board.user == self.target:
            if self.scene.board.action.action_name == "attack":
                self.scene.board.no_skip(
                    f"{self.scene.board.get_actor(self.target).name} flinched!",
                    particle=self.name,
                )
                return True, True, False
        return False, False, False

    def before_end(self):
        return True, False, False
