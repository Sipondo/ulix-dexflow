from .basemoveeffect import BaseMoveEffect


class Terrainmod(BaseMoveEffect):
    def before_action(self):
        global_effects = self.scene.get_global_effects()
        for terrain in [x.name for x in global_effects if x.type == "Terrain"]:
            self.move.power *= terrain.mods(self.move.name)
        return True
