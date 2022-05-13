from .basegamestate import BaseGameState


class GameStateMenuMain(BaseGameState):
    def on_enter(self):
        pass

    def update(self, time, frame_time):
        self.time = time
        # self.lock = self.game.m_ani.on_tick(time, frame_time)
        # self.game.m_pan.set_pan(self.game.m_ent.player.get_pos())
        return False

    def on_exit(self):
        pass
