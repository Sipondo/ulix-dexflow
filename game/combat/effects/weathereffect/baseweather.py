from ..baseeffect import BaseEffect


class BaseWeather(BaseEffect):
    def __init__(self, scene):
        super().__init__(scene)

    def acc_change(self, weather_name):
        return self.scene.board.get_weather_acc_change(weather_name)
