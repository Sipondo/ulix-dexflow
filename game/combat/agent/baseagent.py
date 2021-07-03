import abc


class BaseAgent(abc.ABC):
    def __init__(self, game_state, team):
        self.game_state = game_state
        self.team = team
        self.action = None
        self.sendout = None

    @abc.abstractmethod
    def start(self, scene):
        pass

    @abc.abstractmethod
    def get_action(self, scene):
        return None

    @abc.abstractmethod
    def get_sendout(self, scene):
        return None
