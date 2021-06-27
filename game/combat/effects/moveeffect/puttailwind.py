from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Puttailwind(BaseMoveEffect):
    def after_move(self):
        ApplyStatus(self.scene, statuseffect.TAILWIND, self.move.user, self.move.user).apply()
