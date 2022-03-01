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

    def event_keypress(self, key, modifiers):
        if "alt" in modifiers:
            self.game.m_ent.player.set_movement_type(0)
        elif "shift" in modifiers:
            self.game.m_ent.player.set_movement_type(1)
        elif "ctrl" in modifiers and self.game.m_map.allow_cycle:
            self.game.m_ent.player.set_movement_type(2)
        if not self.lock:
            if key == "interact":
                self.game.m_act.check_interact()
            if key == "menu":
                self.game.m_gst.switch_state("menuparty")
            if key == "zoom_in":
                self.game.pan_tool.zoom_in()
            if key == "zoom_out":
                self.game.pan_tool.zoom_out()
            if key == "debug":
                self.game.m_gst.switch_state("debug")
