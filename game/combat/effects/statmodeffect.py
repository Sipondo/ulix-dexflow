from .baseeffect import BaseEffect
from .genericeffect import GenericEffect


RAISE_TEXTS = {1: "",
               2: " sharply",
               3: " drastically",
               -1: "",
               -2: " harshly",
               -3: " drastically"}


class StatModEffect(BaseEffect):
    name = "Statmod"

    def __init__(self, scene, target):
        super().__init__(scene)
        self.target = target
        self.stats = {
            "Attack": 0,
            "Defense": 0,
            "Special Attack": 0,
            "Special Defense": 0,
            "Speed": 0,
            "Accuracy": 0,
            "Evasion": 0,
        }

    def update(self, stat, change, abs_change=None):
        if abs_change:
            self.stats[stat] = abs_change
            if abs_change == 6:
                self.scene.add_effect(
                    GenericEffect(
                        self.scene,
                        f"{self.scene.board.get_actor(self.target).name} maximized its {stat}",
                        particle="Raisestat",
                    )
                )
            return
        if change > 0:
            change = min(change, 6 - self.stats[stat])
        if change < 0:
            change = max(change, -6 + self.stats[stat])
        if change == 0:
            if change > 0:
                self.scene.add_effect(
                    GenericEffect(
                        self.scene,
                        f"{self.scene.board.get_actor(self.target).name}'s can't be raised any higher!",
                        particle="",
                    )
                )
                return
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.scene.board.get_actor(self.target).name}'s can't be dropped any lower!",
                    particle="",
                )
            )
        self.stats[stat] += change
        if change > 0:
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.scene.board.get_actor(self.target).name}{RAISE_TEXTS[change]} raised its {stat}",
                    particle="Raisestat",
                )
            )
            return

        self.scene.add_effect(
            GenericEffect(
                self.scene,
                f"{self.scene.board.get_actor(self.target).name}'s {stat} got lowered{RAISE_TEXTS[change]}",
                particle="Dropstat",
            )
        )

    @property
    def stat_mod(self):
        stats = [1, 1, 1, 1, 1, 1, 1]
        for index, (stat, mod) in enumerate(self.stats.items()):
            if mod < 0:
                mod = 1 / (-mod * 0.5 + 1)
                stats[index] = mod
            else:
                mod = mod * 0.5 + 1
                stats[index] = mod
        return stats
