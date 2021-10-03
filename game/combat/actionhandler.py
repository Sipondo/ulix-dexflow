from .action import Action, ActionType


class ActionHandler:
    def __init__(self, game, scene):
        self.game = game
        self.scene = scene
        self.legal_actions = []
        self.all_actions = []
        self.init_actions()

    def init_actions(self):
        for i in range(4):
            self.all_actions.append(Action(ActionType.ATTACK, a_index=i))
        self.all_actions.append(Action(ActionType.SWITCH))
        self.all_actions.append(Action(ActionType.ITEM))
        self.all_actions.append(Action(ActionType.RUN))
        self.legal_actions = self.all_actions.copy()

    def is_legal(self, action: Action) -> bool:
        if action.a_type == ActionType.ATTACK:
            return action.a_index in [
                _action.a_index
                for _action in self.legal_actions
                if _action.a_type == ActionType.ATTACK
            ]
        return action.a_type in [_action.a_type for _action in self.legal_actions]

    def remove_legal_action(self, action: Action):
        if action.a_type == ActionType.ATTACK:
            for a in self.legal_actions:
                if action.a_index == a.a_index:
                    self.legal_actions.remove(a)
            return
        for a in self.legal_actions:
            if action.a_type == a.a_type:
                self.legal_actions.remove(a)

    def force_action(self, action: Action):
        self.legal_actions = [action]

    def reset_legal(self):
        self.legal_actions = self.all_actions
