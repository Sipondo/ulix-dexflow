import numpy as np

from .baseagent import BaseAgent
from ..action import Action, ActionType


class AgentRand(BaseAgent):
    def start(self):
        pass

    def get_action(self):
        action_i = np.random.randint(
            len(
                self.scene.board.get_actor(
                    (self.team, self.scene.board.get_active(self.team))
                ).actions
            )
        )
        user = (self.team, self.scene.board.get_active(self.team))
        target_team = np.random.randint(len(self.scene.board.teams))
        while target_team == self.team:
            target_team = np.random.randint(len(self.scene.board.teams))
        target = (target_team, self.scene.board.get_active(target_team))
        action = Action(
            ActionType.ATTACK,
            a_index=action_i,
            a_data=self.scene.board.get_actor(user).actions[action_i],
            user=user,
            target=target
        )
        return action

