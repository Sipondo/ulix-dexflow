from .baseeffect import BaseEffect
from .genericeffect import GenericEffect
from .endbattleeffect import EndBattleEffect


class RunEffect(BaseEffect):
    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.user = user
        self.target = target

    def on_action(self):
        # TODO speed check of both pokemon
        self.scene.add_effect(
            GenericEffect(
                self.scene,
                f"{self.scene.board.get_actor(self.user).name} ran away!",
            )
        )
        self.scene.add_effect(EndBattleEffect(self.scene))
        return False, False, True
