from .baseagent import BaseAgent
import numpy as np


class AgentUser(BaseAgent):
    def predict(self, obs):
        while True:
            obs_active_pmon = 0
            for move in self.team[obs_active_pmon].moves:
                move.describe()

            print("Choose action: 1-4")

            inp = input()

            try:
                inp = int(inp)
                inp %= 5
            except Exception as e:
                inp = 1
            return max(0, inp - 1)
