from ..baseeffect import BaseEffect


class BaseWeather(BaseEffect):
    def __init__(self, scene, weather):
        super().__init__(scene)
        self.acc = self.scene.game.m_pbs.get_weather_acc_change(weather)

    def acc_change(self, move_name):
        return self.acc[move_name]
