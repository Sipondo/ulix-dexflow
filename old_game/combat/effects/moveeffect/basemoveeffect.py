from typing import Tuple
from game.combat.effects.baseeffect import BaseEffect

import abc


class BaseMoveEffect(BaseEffect, abc.ABC):
    type = "MoveEffect"

    def __init__(self, scene, move):
        super().__init__(scene)
        self.move = move

    def before_action(self) -> Tuple[bool, bool, bool]:
        """Anything that needs to happen before an action. Returns a tuple containing information about the current
        action. In order: Delete this effect, skip everything related to this action, end the battle"""
        return False, False, False

    def after_action(self) -> Tuple[bool, bool, bool]:
        """Anything that needs to happen after an action. Returns a tuple containing information about the current
        action. In order: Delete this effect, skip everything related to this action, end the battle."""
        return False, False, False

    def before_end(self) -> Tuple[bool, bool, bool]:
        """Method to delete the move-effect in case it did not happen yet."""
        # always remove these effects at the end of a turn unless otherwise specified.
        return True, False, False
