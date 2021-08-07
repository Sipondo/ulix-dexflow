from .baseeffect import BaseEffect


class ReturnEffect(BaseEffect):
    spd_on_action = 1000

    def __init__(self, scene, target):
        super().__init__(scene)
        self.target = target

    def on_action(self):
        self.scene.board.set_active((self.target[0], -1))
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name}, come back!", particle=""
        )
        return True, False, False
