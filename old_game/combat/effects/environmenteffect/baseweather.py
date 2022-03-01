from ..baseeffect import BaseEffect


class BaseWeather(BaseEffect):
    type = "Weather"

    def __init__(self, scene, weather):
        super().__init__(scene)
        self.acc = self.scene.game.m_pbs.get_weather_acc_change(weather)
        self.active = True
        self.target = "Global"

    def acc_change(self, move_name):
        return self.acc[move_name]
