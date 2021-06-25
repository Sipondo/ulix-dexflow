from .baseagent import BaseAgent
import numpy as np


class AgentRand(BaseAgent):
    def predict(self, obs):
        return np.random.randint(3)
