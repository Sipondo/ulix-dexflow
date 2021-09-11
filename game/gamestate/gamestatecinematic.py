from .basegamestate import BaseGameState
from copy import deepcopy
import numpy as np
import math
import re

from pathlib import Path


class GameStateCinematic(BaseGameState):
    def on_enter(self):
        self.game.r_int.letterbox = True

        self.selection = 0
        self.goto = None
        self.options = []
        self.shop = False
        self.shop_confirm = None

        self.dialogue = None
        self.author = None
        self.prev_dialogue = None
        self.need_to_redraw = True

        self.spr_textbox = self.game.m_res.get_interface("textbox")
        self.spr_namebox = self.game.m_res.get_interface("namebox")

        self.spr_shop_header = self.game.m_res.get_interface("shop_headertile")
        self.spr_shop_descript = self.game.m_res.get_interface("shop_descript")
        self.spr_talker = None

        self.spr_shop_item_background = self.game.m_res.get_interface(
            "shop_item_background_window"
        )
        self.spr_shopwindow = self.game.m_res.get_interface("shopwindow")
        self.spr_itemcell = (
            self.game.m_res.get_interface("shop_itemcell"),
            self.game.m_res.get_interface("shop_itemcell_selected"),
        )
        self.spr_shop_itemtext_cell = self.game.m_res.get_interface(
            "shop_itemtext_cell"
        )
        self.spr_shoplistwindow = self.game.m_res.get_interface("shop_list_window")

    def on_tick(self, time, frame_time):
        self.time = time
        self.lock = self.game.m_ani.on_tick(time, frame_time)
        self.redraw(time, frame_time)
        return False

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
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
                if self.options:
                    self.selection = (self.selection + 1) % self.max_selection
                    self.game.r_aud.effect("select")
            elif key == "up":
                if self.shop_confirm is not None:
                    self.game.r_aud.effect("select")
                    self.shop_confirm += 1
                    if self.shop_confirm > 99:
                        self.shop_confirm = 1
                    return
                if self.options:
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
            elif key == "backspace" or key == "menu":
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
        # TODO: move this away from here
        if self.dialogue:
            self.dialogue = (
                self.dialogue.replace("{player.name}", self.game.m_ent.player.name)
                .replace("{player.he}", self.game.m_ent.player.he)
                .replace("{player.his}", self.game.m_ent.player.his)
                .replace("{player.che}", self.game.m_ent.player.che)
                .replace("{player.chis}", self.game.m_ent.player.chis)
            )

        if not self.shop and self.spr_talker:
            self.game.r_int.draw_image(
                self.spr_talker, (0.8, 0.7), centre=True, size=3.0
            )

        # self.game.r_int.draw_rectangle((0.024, 0.83), to=(0.984, 0.99), col="gray")

        if self.author is not None and self.author:
            self.game.r_int.draw_image(
                self.spr_namebox, (0.02, 0.75),
            )
            self.game.r_int.draw_text(
                self.author, (0.025, 0.755), to=(0.30, 0.80), bcol=None,
            )

        if self.shop:
            item = self.options[self.selection]
            self.game.r_int.draw_image(self.spr_shopwindow, (0.5, 0.45), centre=True)
            self.game.r_int.draw_image(
                self.spr_shop_item_background, (0.3, 0.465), centre=True
            )
            self.game.r_int.draw_image(item.icon, (0.3, 0.41), centre=True, size=3.0)
            self.game.r_int.draw_image(self.spr_shop_header, (0.3, 0.275), centre=True)
            self.game.r_int.draw_image(self.spr_shop_descript, (0.3, 0.6), centre=True)
            self.game.r_int.draw_image(
                self.spr_shoplistwindow, (0.55, 0.23), centre=False
            )
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

            # self.game.r_int.draw_rectangle((0.19, 0.25), size=(0.37, 0.42), col="black")
            self.game.r_int.draw_text(
                f"{item.itemname}",
                (0.31, 0.285),
                size=(0.14, 0.08),
                bcol=None,
                centre=True,
            )
            self.game.r_int.draw_text(
                f"{item.description}",
                (0.3, 0.622),
                size=(0.35, 0.15),
                fsize=10,
                bcol=None,
                centre=True,
            )

            if self.shop_confirm is not None:
                self.game.r_int.draw_image(
                    self.spr_itemcell[1], (0.56, 0.24),
                )
                self.game.r_int.draw_text(
                    f"Quantity: {self.shop_confirm}",
                    (0.65, 0.26),
                    size=(0.22, 0.06),
                    centre=False,
                    bcol=None,
                )
            else:
                # self.game.r_int.draw_rectangle(
                #     (0.59, 0.3),
                #     size=(0.37, 0.02 + 0.08 * len(self.options)),
                #     col="black",
                # )
                for i, name in enumerate(self.options):
                    self.game.r_int.draw_image(
                        self.spr_itemcell[1 if self.selection == i else 0],
                        (0.56, 0.24 + 0.08 * i),
                    )
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{name.price}",
                        (0.57, 0.26 + 0.08 * i),
                        size=(0.10, 0.06),
                        centre=False,
                        bcol=None,
                    )
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{name.itemname}",
                        (0.65, 0.26 + 0.08 * i),
                        size=(0.22, 0.06),
                        centre=False,
                        bcol=None,
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
