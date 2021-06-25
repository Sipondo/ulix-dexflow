from .baseeffect import BaseEffect
from .returneffect import ReturnEffect
from .sendouteffect import SendOutEffect


class SwitchEffect(BaseEffect):
    def __init__(self, scene, action):
        super().__init__(scene)
        self.user = action.user
        self.target = action.target

    def on_action(self):
        self.scene.on_switch_effects(self.user)
        self.scene.add_effect(ReturnEffect(self.scene, self.user))
        self.scene.board.set_active(self.target)
        self.scene.add_effect(SendOutEffect(self.scene, self.target))
        self.scene.on_send_out_effects(self.target)
        return True, False, False
