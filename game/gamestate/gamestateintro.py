from .basegamestate import BaseGameState


class GameStateIntro(BaseGameState):
    def on_enter(self):
        self.need_to_redraw = True

        self.logo_engine = self.game.m_res.get_splash("ulix_logo")
        self.logo_framework = self.game.m_res.get_splash("dexflow_logo")

        self.stage = 0

    def on_tick(self, time, frame_time):
        self.time = time

        if self.stage == 0:
            self.stage = 1
            self.timer = 0
        else:
            self.timer += frame_time

        if self.stage == 1 and self.timer > 0.5:
            self.need_to_redraw = True
            self.stage = 2
        self.redraw(time, frame_time)
        if self.timer > 0.9:
            self.game.m_gst.switch_state("overworld")
        return False

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.need_to_redraw = False

    def event_keypress(self, key, modifiers):
        pass

    def draw_interface(self, time, frame_time):
        if self.stage == 1:
            self.game.r_int.draw_image(
                self.logo_engine, (0.5, 0.5), centre=True, size=0.5
            )
        elif self.stage == 2:
            self.game.r_int.draw_image(
                self.logo_framework, (0.5, 0.5), centre=True, size=0.5
            )
