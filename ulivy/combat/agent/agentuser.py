from .baseagent import BaseAgent


class AgentUser(BaseAgent):
    def start(self):
        pass

    def get_action(self):
        return self.action

    def set_action(self, action):
        if self.action_handler.is_legal(action):  # action possible
            print("     Action possible :)", action)
            self.action = action
            return True
        # action impossible
        print("     Action IMPOSSIBLE!!!", action)
        print("Legal options:", self.action_handler.legal_actions)
        print("Illegal options:", self.action_handler.illegal_actions)
        return False

