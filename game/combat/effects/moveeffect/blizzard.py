from .basemoveeffect import BaseMoveEffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus
from game.combat.effects import statuseffect


class Blizzard(BaseMoveEffect):
    def before_move(self):
        global_effects = self.scene.get_global_effects()
        for weather in [x.name for x in global_effects if x.type == "Weather"]:
            weather_acc_change = weather.acc_change(self.move.name)
            if weather_acc_change == "perf":
                self.move.perfect_accuracy = True
            else:
                self.move.acc += weather.acc_change(self.move.name)
        return True

    def after_move(self):
        if self.scene.board.random_roll() < self.move.chance:
            ApplyStatus(self.scene, statuseffect.FREEZE, self.move.user, self.move.target).apply()
