from .basegamestate import BaseGameState


class GameStateMenuSave(BaseGameState):
    def on_enter(self):
        self.game.r_int.letterbox = False
        self.selection = 0

        self.game.m_sav.write_to_file()

    def on_tick(self, time, frame_time):
        self.time = time
        self.game.m_ent.render()
        return False

    def on_exit(self):
        pass

    def on_render(self, time, frame_time):
        self.draw_interface(time, frame_time)

    def set_locked(self, bool):
        self.lock = bool

    def event_keypress(self, key, modifiers):
        if self.lock == False:
            if key == "menu" or key == "backspace":
                self.game.m_gst.switch_state("menuparty")

    def draw_interface(self, time, frame_time):
        """
        Party and Inspect view
        List pokemon and retrieve info via subview
        """
        self.game.r_int.draw_rectangle((0.07, 0.12), to=(0.93, 0.88), col="black")

