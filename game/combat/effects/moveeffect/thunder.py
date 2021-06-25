from .basemoveeffect import BaseMoveEffect
from game.combat.effects import statuseffect
from game.combat.effects.partialeffect.applystatuseffect import ApplyStatus


class Thunder(BaseMoveEffect):
    def before_move(self):
        global_effects = self.scene.get_global_effects()
        for weather in [x.name for x in global_effects if x.type == "Weather"]:
            weather_acc_change = weather.acc_change(self.move.name)
            if weather_acc_change == "perf":
                self.move.perfect_accuracy = True
            else:
                self.move.acc += weather.acc_change(self.move.name)
        target_effects = self.scene.get_effects_on_target(self.move.target)
        if effects := [x for x in target_effects if x.name in ("Fly", "Bounce", "Sky drop")]:
            for effect in effects:
                effect.done = True
        return True

    def after_move(self):
        if self.scene.board.random_roll() < self.move.chance:
            ApplyStatus(self.scene, statuseffect.PARALYSIS, self.move.user, self.move.target).apply()
