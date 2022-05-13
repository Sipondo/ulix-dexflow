from .basegamestate import BaseGameState


class GameStateCinematic(BaseGameState):
    def on_enter(self, letterbox=True):
        self.options = []
        self.dialogue = None
        self.author = None

        self.spr_talker = None

    def update(self, time, frame_time):
        self.time = time
        self.lock = self.game.m_ani.on_tick(time, frame_time)
        self.game.m_pan.set_pan(self.game.m_ent.player.get_pos())
        return False

    def on_exit(self):
        pass

    def set_locked(self, bool):
        self.lock = bool

    def exit_battle(self):
        print("DEPRECATED EXIT BATTLE GAMESTATEINTERACT")
        self.game.m_gst.switch_state("overworld")
