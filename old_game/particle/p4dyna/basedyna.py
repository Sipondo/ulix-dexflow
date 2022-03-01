import abc


class BaseDyna(abc.ABC):
    def __init__(self, game):
        self.game = game
