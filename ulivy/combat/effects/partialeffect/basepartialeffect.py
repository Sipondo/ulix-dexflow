import abc


class BasePartialEffect(abc.ABC):
    def __init__(self, scene):
        self.scene = scene

    @abc.abstractmethod
    def apply(self):
        pass
