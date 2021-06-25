from .baseeffect import BaseEffect
from .genericeffect import GenericEffect


class SendOutEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.spd_on_action = 1
        self.target = target

    def on_action(self):
        self.scene.add_effect(
            GenericEffect(
                self.scene,
                f"{self.scene.board.get_actor(self.target).name}, go!",
                particle="Sendout",
            )
        )
        return False, False, False
