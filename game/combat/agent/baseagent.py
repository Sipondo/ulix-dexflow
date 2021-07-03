import abc


class BaseAgent(abc.ABC):
    def __init__(self, game):
        self.game = game

    @abc.abstractmethod
    def get_action(self, scene):
        return None

    @abc.abstractmethod
    def get_sendout(self, scene):
        return None
