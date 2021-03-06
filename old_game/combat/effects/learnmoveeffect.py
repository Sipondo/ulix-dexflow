from .baseeffect import BaseEffect
from ..action import ActionType


class LearnMoveEffect(BaseEffect):
    def __init__(self, scene, target, move_name):
        super().__init__(scene)
        self.spd_on_action = 500
        self.target = target
        self.move = self.scene.game.m_pbs.get_move_by_name(move_name)

    def on_action(self):
        actor = self.scene.board.get_actor(self.target)
        actor.actions.append(self.move)
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.target).name} learned {self.move['name']}!", particle=""
        )
        if len(actor.actions) > 4:
            self.scene.board.new_move = True
            self.scene.force_action(self.target[0], ActionType.FORGET_MOVE)
            return True, True, True
        return True, False, False
