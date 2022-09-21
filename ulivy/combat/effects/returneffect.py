from .baseeffect import BaseEffect


class ReturnEffect(BaseEffect):
    name = "Return"

    def __init__(self, scene, target, faint=False):
        super().__init__(scene)
        self.spd_on_action = 1000
        self.target = target

        self.is_fainted = faint

    def on_action(self):
        self.scene.board.set_active((self.target[0], -1))

        if not self.is_fainted:
            print("COME BACK HP", self.scene.board.get_actor(self.target).current_hp)
            self.scene.board.no_skip(
                f"{self.scene.board.get_actor(self.target).name}, come back!",
                particle="summon",
            )
        else:
            self.scene.board.no_skip(
                f"{self.scene.board.get_actor(self.target).name} has fallen!",
                particle="summon",
            )
        return True, False, False
