import abc


class BaseAgent(abc.ABC):
    def __init__(self, game, battle, team):
        self.game = game
        self.battle = battle
        self.team = team
