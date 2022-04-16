from .basegamestate import BaseGameState


class GameStateDebug(BaseGameState):
    def on_enter(self):
        pass

    def update(self, time, frame_time):
        self.time = time
        return False

    def on_exit(self):
        pass

    def on_render(self, time, frame_time):
        self.game.m_ent.render()
