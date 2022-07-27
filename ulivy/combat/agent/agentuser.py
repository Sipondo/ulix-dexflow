from .baseagent import BaseAgent


class AgentUser(BaseAgent):
    def start(self):
        pass

    def get_action(self):
        return self.action

    def set_action(self, action):
        if self.action_handler.is_legal(action):  # action possible
            self.action = action
            return True
        # action impossible
        print("Action IMPOSSIBLE!!!", action)
        return False

