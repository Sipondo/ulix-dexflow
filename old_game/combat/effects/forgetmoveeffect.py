from .baseeffect import BaseEffect


class ForgetMoveEffect(BaseEffect):
    def __init__(self, scene, action):
        super().__init__(scene)
        self.spd_on_action = 250
        self.target = action.target
        self.move = action.a_index

    def on_action(self):
        actor = self.scene.board.get_actor(self.target)
        forgotten_move = actor.actions.pop(self.move)
        self.scene.board.new_move = False
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name} forgot {forgotten_move['name']}!", particle=""
        )
        return True, False, False
