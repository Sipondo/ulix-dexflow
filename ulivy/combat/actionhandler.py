from .action import Action, ActionType


class ActionHandler:
    def __init__(self, game, scene):
        self.game = game
        self.scene = scene
        self.legal_actions = []
        self.illegal_actions = []
        self.init_actions()

    def init_actions(self):
        self.legal_actions = []
        self.illegal_actions = []
        for i in range(4):
            self.legal_actions.append(Action(ActionType.ATTACK, a_index=i))
        self.legal_actions.append(Action(ActionType.SWITCH))
        self.legal_actions.append(Action(ActionType.ITEM))
        self.legal_actions.append(Action(ActionType.CATCH))
        self.legal_actions.append(Action(ActionType.RUN))
        self.illegal_actions.append(Action(ActionType.SENDOUT))

    def is_legal(self, action: Action) -> bool:
        if action.a_type == ActionType.ATTACK:
            return action.a_index in [
                _action.a_index
                for _action in self.legal_actions
                if _action.a_type == ActionType.ATTACK
            ]
        return action.a_type in [_action.a_type for _action in self.legal_actions]

    def describe_legal(self):
        return [str(a.a_type) for a in self.legal_actions]

    def only_legal(self, name):
        legals = self.describe_legal()
        for l in legals:
            if name not in l:
                return False
        return True

    def set_action_legal(self, action: Action):
        if action.a_type == ActionType.ATTACK:
            for a in self.legal_actions:
                if action.a_index == a.a_index:
                    self.illegal_actions.remove(a)
                    self.legal_actions.append(a)
            return
        for a in self.legal_actions:
            if action.a_type == a.a_type:
                self.illegal_actions.remove(a)
                self.legal_actions.append(a)

    def set_action_illegal(self, action: Action):
        if action.a_type == ActionType.ATTACK:
            for a in self.legal_actions:
                if action.a_index == a.a_index:
                    self.legal_actions.remove(a)
                    self.illegal_actions.append(a)
            return
        for a in self.legal_actions:
            if action.a_type == a.a_type:
                self.legal_actions.remove(a)
                self.illegal_actions.append(a)

    def force_action(self, action: Action):
        self.legal_actions = [action]

    def reset_legal(self):
        self.init_actions()
