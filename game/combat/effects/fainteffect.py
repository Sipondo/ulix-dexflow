from .baseeffect import BaseEffect
from .returneffect import ReturnEffect
from .endbattleeffect import EndBattleEffect


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
        self.scene.on_faint_effects(self.target)
        self.scene.add_effect(
            ReturnEffect(self.scene, self.target)
        )
        for i in range(len(self.scene.board.teams[self.target[0]])):
            mon_hp = self.scene.board.get_hp((self.target[0], i))
            if mon_hp > 0:
                end = False
        self.scene.add_effect(EndBattleEffect(self.scene))
        return True, False, end

    def on_end_turn(self):
        self.scene.board.need_sendout[self.target[0]] = True
