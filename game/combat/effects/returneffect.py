from .baseeffect import BaseEffect


class ReturnEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.spd_on_action = 11
        self.target = target

    def on_action(self):
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name}, come back!", particle=""
        )
        return True, False, False
