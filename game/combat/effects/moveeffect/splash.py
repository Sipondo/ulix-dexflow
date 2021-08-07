from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.genericeffect import GenericEffect


class Splash(BaseMoveEffect):
    def after_move(self):
        self.scene.add_effect(GenericEffect(self.scene, "But nothing happened!"))
        return
