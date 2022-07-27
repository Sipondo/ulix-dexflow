from .baseeffect import BaseEffect
from .returneffect import ReturnEffect
from .endbattleeffect import EndBattleEffect
from .experienceeffect import ExperienceEffect
from ..action import ActionType
from .sendouteffect import SendOutEffect


class FaintEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.spd_on_action = 1000
        self.target = target

    def on_action(self):
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name} fainted", particle="",
        )
        end = False
        self.scene.on_faint_effects(self.target)
        self.scene.add_effect(ReturnEffect(self.scene, self.target))
        self.scene.remove_action_effects(self.target)
        self.scene.board.set_can_fight(self.target, False)
        if not self.scene.board.has_fighter(self.target[0]):
            end = True
        if self.target[0] == 1:
            pass
            # experience if enemy fainted
            # self.scene.add_effect(
            #     ExperienceEffect(
            #         self.scene,
            #         (0, self.scene.board.get_active(0)),
            #         self.scene.board.get_actor(self.target),
            #     )
            # ) TODO: re-enable
        if end:
            self.scene.add_effect(EndBattleEffect(self.scene))
        self.scene.board.fainted = True
        # if self.target[0]

        if self.target[0] == 0:
            self.scene.force_action(self.target[0], ActionType.SENDOUT)
        else:
            if not end:
                self.scene.add_effect(
                    SendOutEffect(self.scene, (self.target[0], self.target[1] + 1))
                )
                self.scene.force_action(0, ActionType.SWITCH)
        return True, False, False

    def on_faint(self, target):
        return False, False, False
