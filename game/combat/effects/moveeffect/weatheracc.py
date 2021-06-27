from .basemoveeffect import BaseMoveEffect


class Weatheraccuracy(BaseMoveEffect):
    def before_move(self):
        global_effects = self.scene.get_global_effects()
        for weather in [x.name for x in global_effects if x.type == "Weather"]:
            weather_acc_change = weather.acc_change(self.move.name)
            if weather_acc_change == "perf":
                self.move.perfect_accuracy = True
            else:
                self.move.acc += weather_acc_change
        return True
