from .baseeffect import BaseEffect


class RunCounterEffect(BaseEffect):
    def __init__(self, scene, c):
        super().__init__(scene)
        self.counter = c

    def on_action(self):
        return False, False, False
