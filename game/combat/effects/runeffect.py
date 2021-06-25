from .baseeffect import BaseEffect
from .genericeffect import GenericEffect
from .endbattleeffect import EndBattleEffect


class RunEffect(BaseEffect):
    def __init__(self, scene):
        super().__init__(scene)

    def on_action(self):
        # TODO speed check of both pokemon
        self.scene.add_effect(GenericEffect(self.scene, "BLA ran away!"))
        self.scene.add_effect(EndBattleEffect(self.scene))

        return False, False, True
