from .basegamestate import BaseGameState


class GameStateIntro(BaseGameState):
    def on_enter(self):
        self.game.r_int.fade = True

        # self.logo_engine = self.game.m_res.get_splash("ulix_logo_small")
        self.logo_framework = "splash/dexflow_logo_small"
        self.game.r_int.load_sprite(self.logo_framework)
        self.game.r_int.init_sprite_drawer()

        self.stage = 0

    def on_tick(self, time, frame_time):
        self.time = time

        if self.stage == 0:
            self.stage = 1
            self.timer = 0
        else:
            self.timer += frame_time

        if self.stage == 1 and self.timer > 0.5:
            self.stage = 2

        if self.timer > 0.7:
            self.game.m_gst.switch_state("overworld")
        return False

    def on_exit(self):
        self.game.r_int.fade = False
        pass

    def on_render(self, time, frame_time):
        self.draw_interface(time, frame_time)

    def event_keypress(self, key, modifiers):
        pass

    def draw_interface(self, time, frame_time):
        if self.stage < 3:
            #     self.game.r_int.draw_image(
            #         self.logo_engine, (0.5, 0.5), centre=True, size=0.5
            #     )
            # elif self.stage == 2:
            self.game.r_int.draw_image(
                self.logo_framework, (0.5, 0.5), centre=True, size=0.5
            )
