from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Sleep(BaseMoveEffect):
    def after_move(self):
        ApplyStatus(self.scene, statuseffect.SLEEP, self.move.user, self.move.target).apply()
