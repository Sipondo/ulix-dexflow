from .baseagent import BaseAgent
import numpy as np


class AgentUser(BaseAgent):
    def __init__(self, game):
        super().__init__(game)
        self.sendout = None
        self.action = None

    def get_action(self, scene):
        return (1, 1)

    def set_action(self, action):
        self.action = action

    def get_sendout(self, scene):
        return 1

    def set_sendout(self, sendout):
        self.sendout = sendout
