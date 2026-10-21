from .basegamestate import BaseGameState


class GameStateEnd(BaseGameState):
    def on_enter(self, succes=False):
        self.succes = succes

    def update(self, time, frame_time):
        self.time = time
        return False

    def on_exit(self):
        pass
