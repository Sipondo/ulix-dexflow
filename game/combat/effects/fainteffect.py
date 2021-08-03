from .baseeffect import BaseEffect
from .returneffect import ReturnEffect
from .endbattleeffect import EndBattleEffect
from .experienceeffect import ExperienceEffect


class FaintEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.spd_on_action = 10000
        self.target = target

    def on_action(self):
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name} fainted",
            particle="",
        )
        end = True
        self.scene.on_faint_effects(self.target)
        self.scene.add_effect(ReturnEffect(self.scene, self.target))
        self.scene.remove_action_effects(self.target)
        self.scene.board.set_can_fight(self.target, False)
        if self.scene.board.has_fighter(self.target[0]):
            end = False
        if self.target[0] == 1:
            # experience if enemy fainted
            # TODO make the experience dependent on fainted mon
            self.scene.add_effect(
                ExperienceEffect(
                    self.scene,
                    (0, self.scene.board.get_active(0)),
                    self.scene.board.get_actor(self.target),
                )
            )
        if end:
            self.scene.add_effect(EndBattleEffect(self.scene))
        self.scene.board.switch[self.target[0]] = True
        return True, False, False
