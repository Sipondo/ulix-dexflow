from .baseeffect import BaseEffect


class SendOutEffect(BaseEffect):
    def __init__(self, scene, action):
        super().__init__(scene)
        self.spd_on_action = 10
        self.target = action.user

    def on_action(self):
        self.scene.board.set_active(self.target)
        self.scene.board.switch[self.target[0]] = False
        for ability in self.scene.get_target_abilities(self.target):
            ability.activate()
        self.scene.on_send_out_effects(self.target)
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name}, go!", particle=""
        )
        return True, False, False

    def switch_phase(self):
        self.scene.board.set_active(self.target)
        self.scene.board.switch[self.target[0]] = False
        for ability in self.scene.get_target_abilities(self.target):
            ability.activate()
        self.scene.on_send_out_effects(self.target)
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name}, go!", particle=""
        )
        return True, False, False
