import abc


class BaseGameState(abc.ABC):
    def __init__(self, game, config=None):
        self.game = game
        self.animations = None
        self.lock = False

    @abc.abstractmethod
    def on_enter(self, **kwargs):
        pass

    @abc.abstractmethod
    def on_tick(self, time, frame_time):
        return self.lock

    @abc.abstractmethod
    def on_exit(self):
        pass

    @abc.abstractmethod
    def event_keypress(self, key, modifiers):
        pass
