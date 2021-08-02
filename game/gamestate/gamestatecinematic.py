from .basegamestate import BaseGameState
from copy import deepcopy
import numpy as np
import math
import re

from pathlib import Path

letterbox_to = 0.121


class GameStateCinematic(BaseGameState):
    def on_enter(self):
        self.selection = 0
        self.goto = None
        self.options = []
        self.letterbox = 0.0
        self.shop = False
        self.shop_confirm = None

        self.dialogue = None
        self.author = None
        self.prev_dialogue = None
        self.need_to_redraw = True

        self.spr_textbox = self.game.m_res.get_interface("textbox")
        self.spr_namebox = self.game.m_res.get_interface("namebox")
        self.spr_talker = None

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
        if self.need_to_redraw or (self.dialogue != self.prev_dialogue):
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.prev_dialogue = self.dialogue
            self.need_to_redraw = False

    def set_locked(self, bool):
        self.lock = bool

    def event_keypress(self, key, modifiers):
        if self.lock == False:
            self.need_to_redraw = True
            if key == "down":
                if self.shop_confirm is not None:
                    self.game.r_aud.effect("select")
                    self.shop_confirm -= 1
                    if self.shop_confirm < 1:
                        self.shop_confirm = 99
                    return
                self.selection = (self.selection + 1) % self.max_selection
                self.game.r_aud.effect("select")
            elif key == "up":
                if self.shop_confirm is not None:
                    self.game.r_aud.effect("select")
                    self.shop_confirm += 1
                    if self.shop_confirm > 99:
                        self.shop_confirm = 1
                    return
                self.selection = (self.selection - 1) % self.max_selection
                self.game.r_aud.effect("select")
            elif key == "interact":
                if self.shop:
                    if self.shop_confirm is not None:
                        if self.shop_confirm < 1:
                            self.game.r_aud.effect("cancel")
                            self.shop_confirm = None
                        else:
                            self.game.r_aud.effect("buy")
                            self.game.inventory.add_item(
                                self.options[self.selection].identifier,
                                self.shop_confirm,
                            )
                            self.shop_confirm = None
                            self.dialogue = (
                                "Thank you for your purchase! Anything else?"
                            )
                    else:
                        self.game.r_aud.effect("select")
                        self.shop_confirm = 1
                    return
                if self.options:
                    print("Selected: ", self.options[self.selection])
                    self.game.selection = self.selection
                    self.game.selection_text = self.options[self.selection]
                    self.game.r_aud.effect("confirm")
                else:
                    self.game.r_aud.effect("select")
                self.options = []
                self.selection = 0
                self.dialogue = None
                self.author = None
                self.spr_talker = None
            elif key == "backspace":
                if self.shop:
                    self.game.r_aud.effect("cancel")
                    if self.shop_confirm is not None:
                        self.shop_confirm = None
                    else:
                        self.options = []
                        self.shop = False
                        self.selection = 0
                        self.dialogue = None
                        self.author = None
                        self.spr_talker = None
                # self.game.m_gst.switch_state("overworld")

    @property
    def max_selection(self):
        return len(self.options)

    def exit_battle(self):
        print("DEPRECATED EXIT BATTLE GAMESTATEINTERACT")
        self.game.m_gst.switch_state("overworld")

    def draw_interface(self, time, frame_time):
        self.game.r_int.draw_rectangle((0, 0), to=(1, self.letterbox), col="black")
        self.game.r_int.draw_rectangle((0, 1 - self.letterbox), to=(1, 1), col="black")

        if not self.shop and self.spr_talker:
            self.game.r_int.draw_image(
                self.spr_talker, (0.8, 0.7), centre=True, size=3.0
            )

        # self.game.r_int.draw_rectangle((0.024, 0.83), to=(0.984, 0.99), col="gray")

        if self.author is not None:
            self.game.r_int.draw_image(
                self.spr_namebox, (0.02, 0.75),
            )
            self.game.r_int.draw_text(
                self.author, (0.025, 0.755), to=(0.30, 0.80), bcol=None,
            )

        if self.shop:
            if self.dialogue:
                self.game.r_int.draw_image(
                    self.spr_textbox, (0.02, 0.82),
                )
                self.game.r_int.draw_text(
                    "How many of this article would you like?"
                    if self.shop_confirm is not None
                    else (self.dialogue if self.dialogue is not None else ""),
                    (0.025, 0.825),
                    to=(0.98, 0.98),
                    bcol=None,
                )

            self.game.r_int.draw_rectangle((0.19, 0.25), size=(0.37, 0.42), col="black")

            item = self.options[self.selection]
            self.game.r_int.draw_text(
                f"{item.itemname}", (0.20, 0.26), size=(0.14, 0.08)
            )
            self.game.r_int.draw_text(
                f"{item.description}", (0.20, 0.5), size=(0.35, 0.15), fsize=10,
            )
            self.game.r_int.draw_image(item.icon, (0.45, 0.375), centre=True, size=3.0)

            if self.shop_confirm is not None:
                self.game.r_int.draw_rectangle(
                    (0.59, 0.3), size=(0.37, 0.08), col="black"
                )
                self.game.r_int.draw_text(
                    f"Quantity: {self.shop_confirm}",
                    (0.60, 0.31),
                    size=(0.35, 0.06),
                    centre=False,
                    bcol="yellow",
                )
            else:
                self.game.r_int.draw_rectangle(
                    (0.59, 0.3),
                    size=(0.37, 0.02 + 0.08 * len(self.options)),
                    col="black",
                )
                for i, name in enumerate(self.options):
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{name.price}",
                        (0.60, 0.31 + 0.08 * i),
                        size=(0.10, 0.06),
                        centre=False,
                        bcol=self.selection == i and "yellow" or "white",
                    )
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{name.itemname}",
                        (0.72, 0.31 + 0.08 * i),
                        size=(0.22, 0.06),
                        centre=False,
                        bcol=self.selection == i and "yellow" or "white",
                    )
            return

        if self.dialogue:
            self.game.r_int.draw_image(
                self.spr_textbox, (0.02, 0.82),
            )
            self.game.r_int.draw_text(
                self.dialogue if self.dialogue is not None else "",
                (0.025, 0.825),
                to=(0.98, 0.98),
                bcol=None,
            )

        if self.options:
            self.game.r_int.draw_rectangle(
                (0.75, 0.3), size=(0.15, 0.04 + 0.1 * len(self.options)), col="black"
            )
            for i, name in enumerate(self.options):
                self.game.r_int.draw_text(
                    f"{self.selection == i and '' or ''}{name}",
                    (0.76, 0.31 + 0.08 * i),
                    size=(0.13, 0.06),
                    centre=False,
                    bcol=self.selection == i and "yellow" or "white",
                )
