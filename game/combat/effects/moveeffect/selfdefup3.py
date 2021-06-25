from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.statchange import StatChange


class Selfdefup3(BaseMoveEffect):
    def after_move(self):
        StatChange(self.scene, self.move.user, "Defense", 3).apply()
