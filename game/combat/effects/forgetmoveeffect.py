from .baseeffect import BaseEffect


class ForgetMoveEffect(BaseEffect):
    def __init__(self, scene, action):
        super().__init__(scene)
        self.target = action.target
        self.move = action.action_data

    def on_action(self):
        print("Forgetting move!", self.target, self.move)
        actor = self.scene.board.get_actor(self.target)
        forgotten_move = actor.actions.remove(self.move)
        self.scene.board.new_move = False
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name} forgot {forgotten_move['name']}!", particle=""
        )
        return True, False, False
