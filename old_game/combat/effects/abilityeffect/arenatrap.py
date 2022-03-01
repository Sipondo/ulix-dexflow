from .baseabilityeffect import BaseAbilityEffect
from ...action import ActionType, Action


class Arenatrap(BaseAbilityEffect):
    name = "Arena Trap"

    def on_activate(self):
        for i in range(len(self.scene.board.teams)):
            if i != self.holder[0]:
                self.scene.set_action_legality(i, Action(ActionType.SWITCH), False)

    def on_deactivate(self):
        for i in range(len(self.scene.board.teams)):
            if i != self.holder[0]:
                self.scene.set_action_legality(i, Action(ActionType.SWITCH), True)
