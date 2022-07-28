from .basegamestate import BaseGameState


class GameStatePrompt(BaseGameState):
    def on_enter(self, length=15, filter="all"):
        self.filter = filter  # TODO: move to ui
        self.length = length  # TODO: move to ui
        self.game.r_fbo.r_box.go_to(1.0)

    def update(self, time, frame_time):
        self.time = time
        return False

    def on_exit(self):
        pass
