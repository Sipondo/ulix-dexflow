from .basegamestate import BaseGameState
from copy import deepcopy
import numpy as np
import math

from pathlib import Path

states = {"top": 0, "party": 1, "inspect": 2}
pstates = {"overview": 0, "moves": 1, "stats": 2, "values": 3}


class GameStateMenuParty(BaseGameState):
    def on_enter(self):
        self.selection = 0
        self.selectedmember = 0
        self.icon_frame = 0
        self.frame_counter = 0

        self.state = states["top"]
        self.pstate = pstates["moves"]

        top_menu_options = ["Team", "Bag", "Dex", "Career", "Save", "Options"]

        self.top_menu_options = [
            self.game.m_res.get_interface(x) for x in top_menu_options
        ]
        self.spr_mainmenucell = (
            self.game.m_res.get_interface("Cell"),
            self.game.m_res.get_interface("Cell_Selected"),
        )
        self.spr_partyback = self.game.m_res.get_interface("partyback")
        self.spr_partymemberback = (
            self.game.m_res.get_interface("partymemberback"),
            self.game.m_res.get_interface("partymemberbackmirror"),
        )
        self.spr_iconback = self.game.m_res.get_interface("iconback")

        self.need_to_redraw = True

    def on_tick(self, time, frame_time):
        self.time = time
        # self.lock = self.game.m_ani.on_tick(time, frame_time)
        self.redraw(time, frame_time)
        return False

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
        self.frame_counter += frame_time
        if self.state == states["party"]:
            if self.icon_frame == 0 and self.frame_counter > 0.15:
                self.icon_frame = 1
                self.need_to_redraw = True
            elif self.frame_counter > 0.3:
                self.icon_frame = 0
                self.need_to_redraw = True
                self.frame_counter = 0

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

            if key == "down":
                self.selection = (self.selection + 1) % self.max_selection
                self.game.r_aud.effect("select")
            elif key == "up":
                self.selection = (self.selection - 1) % self.max_selection
                self.game.r_aud.effect("select")

            if self.state == states["top"]:
                if key == "interact":
                    if self.selection == 0:
                        self.state = states["party"]
                        self.selection = 0
                    elif self.selection == 1:
                        self.game.m_gst.switch_state("menubag")
                    elif self.selection == 2:
                        self.game.m_gst.switch_state("menudex")
                    elif self.selection == 3:
                        self.game.m_gst.switch_state("menucareer")
                    elif self.selection == 4:
                        self.game.m_gst.switch_state("menusave")
                    elif self.selection == 5:
                        self.game.m_gst.switch_state("menuoptions")
                    else:
                        self.game.m_gst.switch_state("overworld")
                    self.game.r_aud.effect("confirm")
                elif key == "menu" or key == "backspace":
                    self.game.m_gst.switch_state("overworld")
                    self.game.r_aud.effect("menuclose")
            elif self.state == states["party"]:
                if key == "backspace":
                    self.state = states["top"]
                    self.selection = 0
                    self.game.r_aud.effect("cancel")
                if key == "interact":
                    self.state = states["inspect"]
                    self.selectedmember = self.selection
                    self.selection = 0
                    self.game.r_aud.effect("confirm")
            elif self.state == states["inspect"]:
                if key == "backspace":
                    self.state = states["party"]
                    self.selection = self.selectedmember
                    self.game.r_aud.effect("cancel")
                elif key == "left":
                    if self.pstate <= 0:
                        self.pstate = len(pstates)
                    self.pstate -= 1
                    self.game.r_aud.effect("select")
                elif key == "right":
                    self.pstate += 1
                    if self.pstate >= len(pstates):
                        self.pstate = 0
                    self.game.r_aud.effect("select")

    @property
    def max_selection(self):
        if self.state == states["top"]:
            return len(self.top_menu_options)
        elif self.state == states["party"]:
            return len(self.game.inventory.member_names)
        elif self.state == states["inspect"]:
            return len(self.game.inventory.members[self.selectedmember].moves)

    def draw_interface(self, time, frame_time):
        """
        Top menu view
        Choose from 6 categories
        """
        if self.state == states["top"]:
            # self.game.r_int.draw_rectangle((0.75, 0.3), size=(0.15, 0.4), col="black")
            for i, img in enumerate(self.top_menu_options):
                # self.game.r_int.draw_text(
                #     f"{self.selection == i and '' or ''}{name}",
                #     (0.76, 0.31 + 0.08 * i),
                #     size=(0.13, 0.06),
                #     bcol=self.selection == i and "yellow" or "white",
                # )
                self.game.r_int.draw_image(
                    self.selection == i
                    and self.spr_mainmenucell[1]
                    or self.spr_mainmenucell[0],
                    (0.76 + (self.selection == i and -0.01 or 0), 0.10 + 0.14 * i),
                )
                self.game.r_int.draw_image(
                    img, (0.76 + (self.selection == i and -0.01 or 0), 0.10 + 0.14 * i)
                )
            """
            Party and Inspect view
            List pokemon and retrieve info via subview
            """
        elif self.state == states["party"] or self.state == states["inspect"]:
            # self.game.r_int.draw_rectangle((0.07, 0.12), to=(0.93, 0.88), col="black")
            self.game.r_int.draw_image(self.spr_partyback, (0.5, 0.5), centre=True)
            # Draw left full party view if in party
            if self.state == states["party"]:
                for i, member in enumerate(self.game.inventory.members):
                    i_v = 0.25 + 0.10 * i
                    self.game.r_int.draw_rectangle(
                        (0.155 + (i % 2) * 0.18, i_v + 0.07),
                        size=(0.14, 0.01),
                        col="gray",
                    )
                    current_hp = member.current_hp / member.stats[0]
                    self.game.r_int.draw_rectangle(
                        (0.155 + (i % 2) * 0.18, i_v + 0.07),
                        size=(0.14 * current_hp, 0.01),
                        col="green",
                    )
                    self.game.r_int.draw_image(
                        self.spr_partymemberback[(i + 1) % 2],
                        (0.21 + (i % 2) * 0.22, i_v),
                        centre=True,
                    )
                    self.game.r_int.draw_image(
                        member.icon[self.icon_frame]
                        if self.selection == i
                        else member.icon[0],
                        (0.12 + (i % 2) * 0.4, i_v),
                        centre=True,
                        size=3 / 4,
                    )
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{member.name}",
                        (0.15 + (i % 2) * 0.18, i_v),
                        size=(0.15, 0.07),
                        bcol=None,
                    )
                # Draw left inspect view if in inspect
            elif self.state == states["inspect"]:
                member = self.game.inventory.members[self.selectedmember]
                self.game.r_int.draw_image(
                    member.sprite, (0.25, 0.48), centre=True,
                )
                self.game.r_int.draw_text(
                    f"{member.name}", (0.25, 0.74), size=(0.14, 0.08), centre=True
                )

            # Selected party member
            member = (
                self.game.inventory.members[self.selection]
                if self.state == states["party"]
                else self.game.inventory.members[self.selectedmember]
            )

            # Substates
            if self.pstate == pstates["overview"]:
                for i, stat in enumerate(
                    (
                        ("Dex No.", member.name),
                        ("Species", member.kind),
                        ("Nature", member.nature_name),
                        ("Char", member.characteristic),
                        ("Exp Total", member.exp_total),
                        ("To Next", member.level_xp - member.current_xp),
                    )
                ):
                    self.game.r_int.draw_text(
                        f"{stat[0]}:",
                        (0.7, 0.25 + 0.09 * i,),
                        size=(0.064, 0.07),
                        bcol="white",
                        fsize=8,
                    )
                    self.game.r_int.draw_text(
                        f"{stat[1]}",
                        (0.77, 0.25 + 0.09 * i,),
                        size=(0.11, 0.07),
                        bcol="white",
                        fsize=8,
                        align="right",
                    )

                if self.state == states["inspect"]:
                    self.game.r_int.draw_text(
                        f"{member.pokedex}", (0.4, 0.25), size=(0.28, 0.6), fsize=10,
                    )

            elif self.pstate == pstates["moves"]:
                for i, move in enumerate(member.actions):
                    move = self.game.m_pbs.get_move(move)
                    self.game.r_int.draw_text(
                        f"{move['name']}",
                        (0.7, 0.25 + 0.12 * i,),
                        size=(0.18, 0.1),
                        bcol="white"
                        if self.state == states["party"]
                        else self.selection == i and "yellow" or "white",
                    )
                    self.game.r_int.draw_text(
                        f"{move.pp}/{move.pp}",
                        (0.8, 0.31 + 0.12 * i,),
                        size=(0.08, 0.05),
                        bcol=None,
                        align="right",
                        bold=False,
                    )

                if self.state == states["inspect"]:
                    self.game.r_int.draw_text(
                        f"{self.game.m_pbs.get_move(member.actions[self.selection]).description}",
                        (0.4, 0.25),
                        size=(0.28, 0.6),
                        fsize=10,
                    )
            elif self.pstate == pstates["stats"]:
                for i, stat in enumerate(
                    zip(("HP", "ATK", "DEF", "S.ATK", "S.DEF", "SPD"), member.stats)
                ):
                    self.game.r_int.draw_text(
                        f"{stat[0]}:",
                        (0.7, 0.25 + 0.09 * i,),
                        size=(0.064, 0.07),
                        bcol="white",
                        fsize=8,
                    )
                    self.game.r_int.draw_text(
                        f"{stat[1]}",
                        (0.77, 0.25 + 0.09 * i,),
                        size=(0.11, 0.07),
                        bcol="white",
                        fsize=8,
                        align="right",
                    )

                # if self.state == states["inspect"]:
                #     self.game.r_int.draw_text(
                #         f"{member.flavor}", (0.6, 0.25), size=(0.28, 0.6), fsize=10,
                #     )
            elif self.pstate == pstates["values"]:
                for i, stat in enumerate(
                    zip(
                        ("HP", "ATK", "DEF", "S.ATK", "S.DEF", "SPD"),
                        member.stats_IV,
                        member.stats_EV,
                    )
                ):
                    self.game.r_int.draw_text(
                        f"{stat[0]}:",
                        (0.7, 0.25 + 0.09 * i,),
                        size=(0.064, 0.07),
                        bcol="white",
                        fsize=8,
                    )
                    self.game.r_int.draw_text(
                        f"{stat[1]}",
                        (0.77, 0.25 + 0.09 * i,),
                        size=(0.043, 0.07),
                        bcol="blue",
                        fsize=8,
                        align="right",
                    )
                    self.game.r_int.draw_text(
                        f"{stat[2]}",
                        (0.82, 0.25 + 0.09 * i,),
                        size=(0.06, 0.07),
                        bcol="red",
                        fsize=8,
                        align="right",
                    )

                # if self.state == states["inspect"]:
                #     self.game.r_int.draw_text(
                #         f"{member.flavor}", (0.6, 0.25), size=(0.28, 0.6), fsize=10,
                #     )

