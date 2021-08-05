from .basegamestate import BaseGameState
from copy import deepcopy
import numpy as np
import math
import re

from pathlib import Path

letterbox_to = 0.121


class GameStateMenuEvolve(BaseGameState):
    def on_enter(self):
        self.game.r_int.letterbox = False
        self.selection_team = 0
        self.selection_storage = 0
        self.selection_storage_window = 0
        self.selection_page = 0

        self.selection_page_type = [
            (k, v) for k, v in self.game.m_res.types.items() if k == "NORMAL"
        ][0]

        print("SELPAGE:", self.selection_page_type)

        self.goto = None
        self.shop_confirm = None
        self.letterbox = 0.0
        self.dialogue = None
        self.author = None
        self.prev_dialogue = None
        self.need_to_redraw = True

        self.spr_caught = (
            self.game.m_res.open_image_interface(
                self.game.m_res.p_graphics
                / "Pictures"
                / "Battle"
                / "icon_ball_empty.png",
                size=1.0,
            ),
            self.game.m_res.open_image_interface(
                self.game.m_res.p_graphics / "Pictures" / "Battle" / "icon_ball.png",
                size=1.0,
            ),
        )

        self.update_lists()

    def on_tick(self, time, frame_time):
        self.time = time
        # self.lock = self.game.m_ani.on_tick(time, frame_time)
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
        pass

    def update_lists(self):
        self.storage = self.game.m_pbs.fighters
        if self.selection_page > 0:
            self.storage_paged = self.storage[
                (self.storage.type1 == self.selection_page_type[0])
                | (self.storage.type2 == self.selection_page_type[0])
            ]
        else:
            self.storage_paged = self.storage

    @property
    def max_selection_storage(self):
        return len(self.storage_paged)

    @property
    def selected_storage(self):
        return self.storage_paged.iloc[self.selection_storage]

    def draw_interface(self, time, frame_time):
        self.game.r_int.draw_rectangle((0.04, 0.25), size=(0.27, 0.52), col="black")
        item = self.selected_storage
        self.game.r_int.draw_image(
            self.game.m_res.get_sprite_from_anim(item.name, size=2.0),
            (0.18, 0.505),
            centre=True,
            size=1.0,
        )
        self.game.r_int.draw_text(item["name"], (0.05, 0.26), size=(0.14, 0.05))
        self.game.r_int.draw_text(
            f"{item.type1}", (0.05, 0.7), size=(0.25, 0.05), fsize=10,
        )

        if self.selection_page > 0:
            self.game.r_int.draw_image(
                self.selection_page_type[1], (0.82, 0.21), centre=True, size=1.0
            )
        self.game.r_int.draw_rectangle(
            (0.69, 0.25),
            size=(0.25, 0.02 + 0.08 * min(7, len(self.storage_paged))),
            col="black",
        )
        for i, (_, name) in enumerate(self.storage_paged.iterrows()):
            if (
                i < self.selection_storage_window
                or i >= self.selection_storage_window + 7
            ):
                continue

            # if not isinstance(name, str):
            self.game.r_int.draw_image(
                self.spr_caught[1],
                (0.715, 0.29 + 0.08 * (i - self.selection_storage_window)),
                centre=True,
                size=0.5,
            )
            self.game.r_int.draw_image(
                self.game.m_res.get_party_icon(name["internalname"])[0],
                (0.755, 0.28 + 0.08 * (i - self.selection_storage_window)),
                centre=True,
                size=0.5,
            )
            self.game.r_int.draw_text(
                str(name["name"]),
                (0.79, 0.27 + 0.08 * (i - self.selection_storage_window)),
                size=(0.14, 0.05),
                centre=False,
                bcol=self.selection_storage == i and "yellow" or "white",
            )

