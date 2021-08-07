from .baseeffect import BaseEffect


class LearnMoveEffect(BaseEffect):
    def __init__(self, scene, target, move_name):
        super().__init__(scene)
        self.target = target
        self.move = self.scene.game.m_pbs.get_move_by_name(move_name)

    def on_action(self):
        return True, False, False
        print("Learning move!", self.target, self.move)
        actor = self.scene.board.get_actor(self.target)
        actor.actions.append(self.move)
        self.scene.board.new_move = True
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name} learned {self.move['name']}!", particle=""
        )
        return True, True, True
