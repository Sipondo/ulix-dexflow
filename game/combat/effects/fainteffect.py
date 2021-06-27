from .baseeffect import BaseEffect
from .returneffect import ReturnEffect


class FaintEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.spd_on_action = 10000
        self.target = target

    def on_action(self):
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name} fainted",
            particle="Faint",
        )
        end = True
        self.scene.add_effect(
            ReturnEffect(self.scene, self.target)
        )
        for i in range(len(self.scene.board.teams[self.target[0]])):
            mon_hp = self.scene.board.get_hp((self.target[0], i))
            if mon_hp > 0:
                end = False
        return True, False, end

    def on_end_turn(self):
        self.scene.board.need_sendout[self.target[0]] = True
