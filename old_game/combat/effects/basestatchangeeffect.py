from .baseeffect import BaseEffect


STATMAP = {
    "HP": 0,
    "Attack": 1,
    "Defense": 2,
    "Special Attack": 3,
    "Special Defense": 4,
    "Speed": 5,
}


class BaseStatChangeEffect(BaseEffect):
    name = "StatChange"

    def __init__(self, scene, target):
        super().__init__(scene)
        self.target = target
        self.stats = self.scene.board.get_actor(self.target).stats.copy()

    def update(self, stat, new_stat):
        self.stats[STATMAP[stat]] = new_stat

    def on_stat_request(self, target, stat):
        if target == self.target:
            return self.stats[STATMAP[stat]]
        return None

    def on_switch(self, target_old, target_new):
        return self.target == target_old, False, False

    def on_faint(self, target):
        return self.target == target, False, False
