from .baseagent import BaseAgent


class AgentUser(BaseAgent):
    def start(self, scene):
        pass

    def get_action(self, scene):
        return self.action

    def set_action(self, action):
        self.action = action

    def get_sendout(self, scene):
        return self.sendout

    def set_sendout(self, sendout):
        self.sendout = sendout
