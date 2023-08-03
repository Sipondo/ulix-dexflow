from .basegamestate import BaseGameState

# from kivy.graphics.context import get_context


class GameStateOverworld(BaseGameState):
    def on_enter(self):
        # get_context().reload()
        self.game.r_fbo.enable_overworld()
        self.game.r_fbo.r_box.go_to(0.0)
        self.time = None
        self.movement_type = 0
        # self.game.r_aud.play_music("bgm/021-Field04.flac")
        self.game.r_aud.play_music(
            f"bgm/{self.game.m_map.environment}.ogg"
        )  # TODO: use map flag

        self.game.m_sav.write_to_file()

    def update(self, time, dt):
        self.time = time
        # TODO: potentially move this?
        self.lock = self.game.m_ani.on_tick(time, dt)
        return False

    def on_exit(self):
        pass
