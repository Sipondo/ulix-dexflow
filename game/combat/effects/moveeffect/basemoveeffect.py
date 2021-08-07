from game.combat.effects.baseeffect import BaseEffect

import abc


class BaseMoveEffect(BaseEffect, abc.ABC):
    type = "MoveEffect"

    def __init__(self, scene, move):
        super().__init__(scene)
        self.move = move

    def before_move(self):
        return True

    def after_move(self):
        return True
