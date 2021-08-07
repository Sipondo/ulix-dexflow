from .basegamestate import BaseGameState


class GameStateOverworld(BaseGameState):
    def on_enter(self):
        self.game.r_int.letterbox = False

        self.time = None
        self.movement_type = 0
        self.need_to_redraw = True
        self.game.r_aud.play_music("BGM/021-Field04.flac")

    def on_tick(self, time, frame_time):
        self.time = time
        direction = self.check_direction()
        self.lock = self.game.m_ani.on_tick(time, frame_time)
        if direction and not self.lock:
            self.game.m_ent.player.start_move(direction, self.time)
        self.redraw()
        return False

    def on_exit(self):
        pass

    def redraw(self):
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.need_to_redraw = False
        self.game.m_ent.render()

    def check_direction(self):
        for v in self.game.m_key.pressed_keys:
            if v in ("up", "down", "left", "right"):
                return v
        return None

    def event_keypress(self, key, modifiers):
        if modifiers.alt:
            self.game.m_ent.player.set_movement_type(0)
        elif modifiers.shift:
            self.game.m_ent.player.set_movement_type(1)
        # elif modifiers.ctrl:
        #     self.game.m_ent.player.set_movement_type(2)
        if not self.lock:
            if key == "interact":
                self.game.m_act.check_interact()
            # if key == "battle":
            #     self.game.m_gst.switch_state("battle")
            if key == "menu":
                self.game.m_gst.switch_state("menuparty")
            # if key == "zoom_in":
            #     self.game.pan_tool.zoom_in()
            # if key == "zoom_out":
            #     self.game.pan_tool.zoom_out()
