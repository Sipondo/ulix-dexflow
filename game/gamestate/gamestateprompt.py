from .basegamestate import BaseGameState

import numpy as np


class GameStatePrompt(BaseGameState):
    def on_enter(self, length=15, filter="all"):
        self.need_to_redraw = True
        self.input = ""
        self.filter = filter
        self.block_input = True
        self.length = length

        self.initialised = False

    def on_tick(self, time, frame_time):
        self.time = time

        if not self.initialised:
            self.initialised = True
            self.input = ""

        self.redraw(time, frame_time)
        return False

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.game.r_int.draw_rectangle(
                (0.28, 0.34), to=(0.72, 0.46), col="black",
            )
            self.game.r_int.draw_text(
                self.input, (0.3, 0.36), to=(0.7, 0.44), col="black",
            )
            self.need_to_redraw = False
        self.game.m_ent.render()

    def event_unicode(self, char):
        if len(self.input) >= self.length:
            return
        if self.filter == "letters":
            if not char.isalpha():
                return
        self.need_to_redraw = True
        self.input += char

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            if len(self.input):
                self.need_to_redraw = True
                self.input = self.input[:-1]
        if key == "enter":
            print("Input:", self.input)
            self.game.text_input = self.input
            self.game.m_gst.switch_to_previous_state()

