from .baseeffect import BaseEffect
from .returneffect import ReturnEffect
from .sendouteffect import SendOutEffect
from ..action import ActionType


class SwitchEffect(BaseEffect):
    def __init__(self, scene, action):
        super().__init__(scene)
        self.user = action.user
        print("Switch!!!", action)
        self.target = action.target

    def on_action(self):
        self.scene.add_effect(ReturnEffect(self.scene, self.user))
        self.scene.on_switch_effects(self.user, self.target)
        self.scene.add_effect(SendOutEffect(self.scene, self.target))
        # self.scene.force_action(self.target[0], ActionType.SENDOUT)
        self.scene.on_send_out_effects(self.target)
        return True, False, False
