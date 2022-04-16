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
    def update(self, time, frame_time):
        return self.lock

    # @abc.abstractmethod
    def on_render(self, time, frame_time):
        return self.lock

    @abc.abstractmethod
    def on_exit(self):
        pass

    def event_keypress(self, key, modifiers):
        pass

    def event_unicode(self, char):
        pass
