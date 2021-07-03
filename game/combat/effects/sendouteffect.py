from .baseeffect import BaseEffect


class SendOutEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.spd_on_action = 10
        self.target = target

    def on_action(self):
        self.scene.board.set_active(self.target)
        self.scene.board.switch[self.target[0]] = False
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name}, go!", particle=""
        )
        return True, False, False
