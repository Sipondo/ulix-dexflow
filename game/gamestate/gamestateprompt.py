from .basegamestate import BaseGameState

import numpy as np


class GameStatePrompt(BaseGameState):
    def on_enter(self):
        pass

    def on_tick(self, time, frame_time):
        self.time = time
        self.redraw(time, frame_time)
        return False

    def get_evolutions(self):
        if not self.evolving:
            if len(self.to_evolve) > 0:
                self.evo, self.evo_target = self.to_evolve.pop()
                self.evo_name = self.evo.name
                self.get_evo_data()
                self.evolving = True
                self.evolve = False
                self.need_to_redraw = True
            else:
                self.game.m_gst.switch_state("overworld")

    def get_evo_data(self):
        self.small_splash = self.evo.sprite
        self.big_splash = self.game.m_res.get_sprite_from_anim(
            self.evo_target.name, size=2.0
        )

    def on_exit(self):
        self.game.r_int.fade = False

    def redraw(self, time, frame_time):
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.game.r_int.draw_rectangle(
                (0, 0), to=(1, 1), col="black",
            )
            self.draw_interface(time, frame_time)
            self.need_to_redraw = False

    def event_keypress(self, key, modifiers):
        if key == "interact":
            if self.evolving:
                self.evolve = True
                self.evo.evolve(self.evo_target)
                self.need_to_redraw = True
            else:
                self.get_evolutions()
        if key == "backspace":
            self.evolving = False
            self.need_to_redraw = True
            self.game.r_int.fade = True

    def draw_interface(self, time, frame_time):
        if self.evolving:
            self.game.r_int.draw_image(
                self.spr_statusbox, (0.0035, 0.9),
            )
            if not self.evolve:
                self.game.r_int.draw_image(self.small_splash, (0.5, 0.5), centre=True)
                self.game.r_int.draw_text(
                    f"{self.evo.name} is evolving!",
                    (0.01, 0.91),
                    to=(0.99, 0.99),
                    bcol=None,
                )
            else:
                self.game.r_int.draw_image(self.big_splash, (0.5, 0.5), centre=True)
                self.game.r_int.draw_text(
                    f"{self.evo_name} has evolved into {self.evo.name}!",
                    (0.01, 0.91),
                    to=(0.99, 0.99),
                    bcol=None,
                )
                self.evolving = False

