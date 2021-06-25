import abc


class BaseEvent(abc.ABC):
    # location is a list of coordinates that will trigger the event
    def __init__(self, game, location, lock = False, multitrigger = False):
        self.lock = lock
        self.triggered = False
        self.multitrigger = multitrigger
        self.location = location
        self.game = game

    @abc.abstractmethod
    def check_trigger(self):
        if self.game.m_ent.player.get_pos() in self.location:
            return True

    @abc.abstractmethod
    def on_trigger(self, time):
        pass
