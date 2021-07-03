from .baseagent import BaseAgent
import numpy as np


class AgentRand(BaseAgent):
    def start(self, scene):
        pass

    def get_action(self, scene):
        action_i = np.random.randint(4)
        action = ("attack", scene.board.get_actor((self.team, scene.board.get_active(self.team))).actions[action_i])
        user = (self.team, scene.board.get_active(self.team))
        target_team = np.random.randint(len(scene.teams))
        while target_team == self.team:
            target_team = np.random.randint(len(scene.teams))
        target = (target_team, scene.board.get_active(target_team))
        return action, user, target

    def get_sendout(self, scene):
        return 1
