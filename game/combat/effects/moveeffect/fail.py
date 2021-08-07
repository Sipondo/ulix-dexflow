from .basemoveeffect import BaseMoveEffect
from ..genericeffect import GenericEffect


class Fail(BaseMoveEffect):
    def after_move(self):
        self.scene.add_effect(GenericEffect(self.scene, "But it failed"))
        return True
