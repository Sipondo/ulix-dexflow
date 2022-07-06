from .basegamestate import BaseGameState


class GameStateOverworld(BaseGameState):
    def on_enter(self):
        # self.game.r_int.letterbox = False

        self.time = None
        self.movement_type = 0
        # self.game.r_aud.play_music("BGM/021-Field04.flac")

    def update(self, time, dt):
        self.time = time
        direction = self.check_direction()
        self.lock = self.game.m_ani.on_tick(time, dt)
        if direction and not self.lock:
            self.game.m_ent.player.start_move(direction, self.time)
        self.game.m_pan.set_pan(self.game.m_ent.player.get_pos())
        # self.game.m_ent.render()

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
