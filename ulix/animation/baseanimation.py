import abc


class BaseAnimation(abc.ABC):
    def __init__(self, game, start, lock=False):
        self.game = game
        self.lock = lock
        self.start = start
        self.on_enter()

    @abc.abstractmethod
    def on_tick(self, time, frame_time):
        pass

    @abc.abstractmethod
    def on_enter(self):
        pass

    @abc.abstractmethod
    def on_end(self, time, frame_time):
        pass

    @abc.abstractmethod
    def conditions(self):
        return True
