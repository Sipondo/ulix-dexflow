from .basegamestate import BaseGameState


class GameStateMenuBag(BaseGameState):
    def on_enter(self):
        pass

    def update(self, time, frame_time):
        self.time = time
        return False

    def on_exit(self):
        pass
