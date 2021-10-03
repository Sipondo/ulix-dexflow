import abc

from ..actionhandler import ActionHandler
from ..action import ActionType, Action


class BaseAgent(abc.ABC):
    def __init__(self, game, scene, team):
        self.game = game
        self.scene = scene
        self.team = team
        self.action_handler = ActionHandler(self.game, self.scene)
        self.action = None

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def get_action(self):
        return None

    def get_first_sendout(self):
        sendout_i = self.scene.board.get_first_sendout(self.team)
        return Action(ActionType.SENDOUT, user=(self.team, sendout_i), target=(self.team, sendout_i))

    def force_sendout(self):
        self.action_handler.force_action(Action(ActionType.SENDOUT))

    def reset_actions(self):
        self.action = None
        self.action_handler.reset_legal()
