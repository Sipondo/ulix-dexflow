from .baseeffect import BaseEffect


class SendOutEffect(BaseEffect):
    def __init__(self, scene, action):
        super().__init__(scene)
        self.spd_on_action = 10
        # TODO: get rid of this patch
        try:
            self.target = action.target  # .user
        except AttributeError:
            self.target = action

    def on_action(self):
        self.scene.board.set_active(self.target)
        self.scene.board.fainted = False
        self.scene.on_send_out_effects(self.target)
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name}, go!", particle="summon"
        )
        return True, False, False

    def switch_phase(self):
        self.scene.board.set_active(self.target)
        self.scene.board.fainted = False
        self.scene.on_send_out_effects(self.target)
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name}, go!", particle="summon"
        )
        return True, False, False
