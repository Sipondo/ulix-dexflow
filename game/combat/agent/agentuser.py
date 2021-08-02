from .baseagent import BaseAgent


class AgentUser(BaseAgent):
    def start(self, scene):
        pass

    def get_action(self, scene):
        return self.action

    def set_action(self, action):
        if True:  # action possible
            self.action = action
            return True
        # action impossible
        return False

    def get_sendout(self, scene):
        return self.sendout

    def set_sendout(self, scene, sendout):
        if scene.board.get_can_fight(self.team, sendout):
            self.sendout = sendout
            return True
        return False
