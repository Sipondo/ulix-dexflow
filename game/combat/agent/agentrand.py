from .baseagent import BaseAgent
import numpy as np


class AgentRand(BaseAgent):
    def get_action(self, scene):
        return (1, 1)

    def get_sendout(self, scene):
        return 1
    # def predict(self, obs):
    #     return np.random.randint(3)
