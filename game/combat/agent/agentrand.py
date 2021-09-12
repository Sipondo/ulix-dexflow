from .baseagent import BaseAgent
import numpy as np


class AgentRand(BaseAgent):
    def start(self, scene):
        pass

    def get_action(self, scene):
        action_i = np.random.randint(
            len(
                scene.board.get_actor(
                    (self.team, scene.board.get_active(self.team))
                ).actions
            )
        )
        action = (
            "attack",
            scene.board.get_actor(
                (self.team, scene.board.get_active(self.team))
            ).actions[action_i],
        )
        user = (self.team, scene.board.get_active(self.team))
        target_team = np.random.randint(len(scene.board.teams))
        while target_team == self.team:
            target_team = np.random.randint(len(scene.board.teams))
        target = (target_team, scene.board.get_active(target_team))
        return action, user, target

    def get_sendout(self, scene):
        random_fighter = np.random.randint(len(scene.board.teams[self.team]))
        while not scene.board.get_data((self.team, random_fighter)).can_fight:
            random_fighter = np.random.randint(len(scene.board.teams[self.team]))
        return random_fighter
