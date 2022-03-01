import typing

from .action import ActionType, Action
from .agent.baseagent import BaseAgent
from .agent.agentuser import AgentUser


class AgentManager:
    def __init__(self, game, scene):
        self.game = game
        self.scene = scene
        self.agents: typing.List[BaseAgent] = []

    def add_agent(self, agent: BaseAgent):
        self.agents.append(agent)

    def register_action(self, i: int, action: Action):
        self.agents[i].set_action(action)

    def unregister_action(self, i: int):
        self.agents[i].reset_actions()

    def force_action(self, i: int, a_t: ActionType):
        self.agents[i].force_action(a_t)

    def set_legality(self, i: int, action: Action, legality: bool):
        self.agents[i].set_legality(action, legality)

    def start_agents(self):
        for agent in self.agents:
            agent.reset_actions()
            agent.start()

    def get_user_agents(self, has_action: typing.Optional[bool] = None) -> typing.List[int]:
        agents_indices = []
        for i, agent in enumerate(self.agents):
            if type(agent) == AgentUser:
                if has_action is not None:
                    if has_action:
                        if agent.action is not None:
                            agents_indices.append(i)
                    else:
                        if agent.action is None:
                            agents_indices.append(i)
                else:
                    agents_indices.append(i)
        return agents_indices

    def get_agents(self) -> typing.List[BaseAgent]:
        return self.agents

    def get_actions(self) -> typing.List[Action]:
        actions = []
        for i, agent in enumerate(self.agents):
            action = agent.get_action()
            if action is not None:
                actions.append(action)
            elif type(agent) == AgentUser:
                return []
        return actions
