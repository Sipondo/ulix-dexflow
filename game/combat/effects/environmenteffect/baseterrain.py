from ..baseeffect import BaseEffect


class BaseTerrain(BaseEffect):
    def __init__(self, scene, terrain):
        super().__init__(scene)
        self.mods = self.scene.game.m_pbs.get_terrain_mods(terrain)
        self.target = "Global"

    def terrain_mods(self, move_name):
        return self.mods[move_name]
