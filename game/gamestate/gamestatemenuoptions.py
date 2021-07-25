from .basegamestate import BaseGameState
from copy import deepcopy
import numpy as np
import math

from pathlib import Path


class GameStateMenuOptions(BaseGameState):
    def on_enter(self):
        self.selection = 0

        self.need_to_redraw = True

    def on_tick(self, time, frame_time):
        self.time = time
        # self.lock = self.game.m_ani.on_tick(time, frame_time)
        self.redraw(time, frame_time)
        return False

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
        self.game.m_ent.render()
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.need_to_redraw = False

    def set_locked(self, bool):
        self.lock = bool

    def event_keypress(self, key, modifiers):
        if self.lock == False:
            self.need_to_redraw = True
            if key == "menu" or key == "backspace":
                self.game.m_gst.switch_state("menuparty")

    def draw_interface(self, time, frame_time):
        """
        Party and Inspect view
        List pokemon and retrieve info via subview
        """
        self.game.r_int.draw_rectangle((0.07, 0.12), to=(0.93, 0.88), col="black")

