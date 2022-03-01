from .baseanimation import BaseAnimation


class EncounterAnimation(BaseAnimation):
    def __init__(self, game, start):
        print("Encounter!")
        super().__init__(game, start, lock=True)

    def on_tick(self, time, frame_time):
        if time - self.start > 0.5:
            self.on_end(time, frame_time)
            return False
        return self.lock

    def on_enter(self):
        self.game.pan_tool.zoom_encounter()

    def on_end(self, time, frame_time):
        self.game.m_gst.switch_state("battle")
        self.game.m_ani.remove_anim(self)

    def conditions(self):
        return True
