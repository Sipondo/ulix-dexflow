from .basegamestate import BaseGameState

import numpy as np


class GameStateMenuEvolve(BaseGameState):
    def on_enter(self):
        self.game.r_int.fade = False
        self.to_evolve = []  # list of members who evolve, evolution target
        self.evolving = False
        self.evolve = False
        for member in self.game.inventory.members:
            evolution_data = member.data["evolutions"]
            if evolution_data != evolution_data:
                continue
            evolve_target, cond, cond_req = evolution_data.split(",")
            if cond == "Level":
                if member.level > int(cond_req):
                    self.to_evolve.append((member, self.game.m_pbs.get_figher_by_name(evolve_target)))

        self.spr_statusbox = self.game.m_res.get_interface("statusbox")

        self.evo = None
        self.evo_target = None

        self.need_to_redraw = False

        # self.logo_engine = self.game.m_res.get_splash("ulix_logo_small")
        self.small_splash = None
        self.big_splash = None

    def on_tick(self, time, frame_time):
        if not self.evolving:
            if len(self.to_evolve) > 0:
                self.evo, self.evo_target = self.to_evolve.pop()
                self.get_evo_data()
                self.evolving = True
                self.evolve = False
                self.need_to_redraw = True
            else:
                self.game.m_gst.switch_state("overworld")
        self.time = time

        self.redraw(time, frame_time)
        return False

    def get_evo_data(self):
        self.small_splash = self.evo.sprite
        self.big_splash = self.game.m_res.get_sprite_from_anim(self.evo_target.name, size=2.0)

    def on_exit(self):
        self.game.r_int.fade = False

    def redraw(self, time, frame_time):
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.need_to_redraw = False

    def event_keypress(self, key, modifiers):
        if key == "interact":
            self.evolve = True
            self.evo.evolve(self.evo_target)
            self.need_to_redraw = True
        if key == "backspace":
            self.evolving = False
            self.need_to_redraw = True
            self.game.r_int.fade = True

    def draw_interface(self, time, frame_time):
        if len(self.to_evolve) > 0:
            self.game.r_int.draw_image(
                self.spr_statusbox, (0.0035, 0.9),
            )
            if not self.evolve:
                self.game.r_int.draw_image(
                    self.big_splash, (0.5, 0.5), centre=True
                )
                self.game.r_int.draw_text(
                    f"{self.evo.name} is evolving!", (0.01, 0.91), to=(0.99, 0.99), bcol=None
                )
            else:
                self.game.r_int.draw_image(
                    self.small_splash, (0.5, 0.5), centre=True
                )
                self.game.r_int.draw_text(
                    f"{self.evo.name} has evolved into {self.evo_target.name}!", (0.01, 0.91), to=(0.99, 0.99), bcol=None
                )


