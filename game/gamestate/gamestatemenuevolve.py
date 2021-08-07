from .basegamestate import BaseGameState


class GameStateIntro(BaseGameState):
    def on_enter(self):
        self.to_evolve = []  # list of members who evolve, evolution target
        for member in self.game.inventory.members:
            evolution_data = member.data["evolutions"]
            evolve_target, cond, cond_req = evolution_data.split(",")
            if cond == "Level":
                if member.level > int(cond_req):
                    self.to_evolve.append((member, evolve_target))
        self.game.r_int.fade = True

        self.evo = None
        self.evo_target = None

        self.need_to_redraw = True

        # self.logo_engine = self.game.m_res.get_splash("ulix_logo_small")
        self.logo_framework = self.game.m_res.get_splash("dexflow_logo_small")

        self.stage = 0

    def on_tick(self, time, frame_time):
        if not self.lock:
            if self.to_evolve:
                self.evo, self.evo_target = self.to_evolve.pop()
            else:
                self.game.m_gst.switch_state("overworld")
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
        return False

    def on_exit(self):
        self.game.r_int.fade = False
        pass

    def redraw(self, time, frame_time):
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.need_to_redraw = False

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
