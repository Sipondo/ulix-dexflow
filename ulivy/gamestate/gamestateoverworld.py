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
        direction = self.check_direction()
        self.lock = self.game.m_ani.on_tick(time, dt)
        if direction and not self.lock:
            self.game.m_ent.player.start_move(direction, self.time)
        self.game.m_pan.set_pan(self.game.m_ent.player.get_pos())
        return False

    def on_exit(self):
        pass

    def check_direction(self):
        # TODO: move to own function
        if (
            not self.game.m_map.allow_cycle
            and self.game.m_ent.player.movement_type == 2
        ):
            self.game.m_ent.player.set_movement_type(1)
        for v in self.game.m_key.pressed_keys:
            if v in ("up", "down", "left", "right"):
                return v
        return None
