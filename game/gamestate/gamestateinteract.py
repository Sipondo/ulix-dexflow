from .basegamestate import BaseGameState
from copy import deepcopy
import numpy as np
import math
import re

from pathlib import Path

states = {"topmenu": 0, "movemenu": 1, "pokemenu": 2, "ballmenu": 3}
letterbox_to = 0.121

re_curly = re.compile(r"\{([^\{\}\[\]]*)\}")
re_bracket = re.compile(r"\[([^\{\}\[\]]*)\]")


class GameStateInteract(BaseGameState):
    def on_enter(self):
        self.selection = 0

        self.state = states["topmenu"]

        self.dialogue = self.game.m_evt.interact_entity.dialogue.split("\n\n")
        self.dialogue_id = -1
        self.goto = None
        self.options = []
        self.options_gotos = []
        self.letterbox = 0.0

        self.current_dialogue = self.interpret_dialogue()
        self.need_to_redraw = True

    def on_tick(self, time, frame_time):
        self.time = time
        self.lock = self.game.m_ani.on_tick(time, frame_time)
        self.redraw(time, frame_time)
        return False

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
        if self.letterbox < letterbox_to:
            self.letterbox = min(self.letterbox + frame_time * 0.25, letterbox_to)
            self.need_to_redraw = True

        self.game.m_ent.render()
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.need_to_redraw = False

    def interpret_dialogue(self):
        if self.dialogue_id + 1 >= len(self.dialogue):
            self.game.m_gst.switch_state("overworld")
            return

        self.dialogue_id += 1
        dialogue_line = self.dialogue[self.dialogue_id].strip()
        curlies = re_curly.findall(dialogue_line)
        brackets = re_bracket.findall(dialogue_line)

        if "end" in curlies and not self.goto:
            self.dialogue_id = len(self.dialogue) + 1
            return self.interpret_dialogue()

        if self.goto:
            if not self.goto in curlies:
                return self.interpret_dialogue()
            self.goto = None

        dialogue_line = re_bracket.sub(
            "", re_curly.sub("", dialogue_line).strip()
        ).strip()
        print(curlies, brackets, dialogue_line)
        if brackets:
            self.options = brackets[0].split("/")
            self.options_gotos = [x.split("::")[1] for x in self.options]
            self.options = [x.split("::")[0] for x in self.options]

            print("BRACKETSSSSSSSSSSSSS", self.options_gotos, self.options)
        return dialogue_line

    def set_locked(self, bool):
        self.lock = bool

    def event_keypress(self, key, modifiers):
        if self.lock == False:
            self.need_to_redraw = True
            if key == "down":
                self.selection = (self.selection + 1) % self.max_selection
                self.game.r_aud.effect("select")
            elif key == "up":
                self.selection = (self.selection - 1) % self.max_selection
                self.game.r_aud.effect("select")
            elif key == "interact":
                if self.options:
                    print("Selected: ", self.options[self.selection])
                    self.goto = self.options_gotos[self.selection]
                    self.game.r_aud.effect("confirm")
                else:
                    self.game.r_aud.effect("select")
                self.options = []
                self.current_dialogue = self.interpret_dialogue()
                self.selection = 0

    @property
    def max_selection(self):
        return len(self.options)

    def exit_battle(self):
        self.game.m_gst.switch_state("overworld")

    def draw_interface(self, time, frame_time):
        self.game.r_int.draw_rectangle((0, 0), to=(1, self.letterbox), col="black")
        self.game.r_int.draw_rectangle((0, 1 - self.letterbox), to=(1, 1), col="black")

        self.game.r_int.draw_rectangle((0.024, 0.83), to=(0.984, 0.99), col="gray")
        self.game.r_int.draw_text(self.current_dialogue, (0.02, 0.82), to=(0.98, 0.98))

        if self.options:
            self.game.r_int.draw_rectangle(
                (0.75, 0.3), size=(0.15, -0.04 + 0.1 * len(self.options)), col="black"
            )
            for i, name in enumerate(self.options):
                self.game.r_int.draw_text(
                    f"{self.selection == i and '' or ''}{name}",
                    (0.76, 0.31 + 0.08 * i),
                    size=(0.13, 0.06),
                    centre=False,
                    bcol=self.selection == i and "yellow" or "white",
                )
