from .basegamestate import BaseGameState

from game.particle.battlerender import BattleRender
from game.combat.combatscene import CombatScene
from game.combat.agent.agentrand import AgentRand
from game.combat.agent.agentuser import AgentUser
import traceback

import time as ti

states = {"action": 0, "topmenu": 1, "actionmenu": 2, "swapmenu": 3, "ballmenu": 4}


class GameStateBattle(BaseGameState):
    def on_enter(self, enemy_team=None, agents=None):
        self.render = BattleRender(self.game)
        self.combat = CombatScene(
            self.game,
            [x.series for x in self.game.inventory.members],
            enemy_team or [1, 2],
        )
        self.render.camera.reset()
        self.board = self.combat.board
        self.pending_boards = []

        self.actor_1 = self.board.actor_1
        self.actor_2 = self.board.actor_2

        # TODO move away as it should be initiated as a move
        self.render.set_pokemon(self.actor_1[0].sprite, 0)
        self.render.set_pokemon(self.actor_2[0].sprite, 1)

        self.spr_battlecell = (
            self.game.m_res.get_interface("battlecell"),
            self.game.m_res.get_interface("battlecell_selected"),
        )

        self.spr_battlestatus = (
            self.game.m_res.get_interface("battlestatus_ours"),
            self.game.m_res.get_interface("battlestatus_theirs"),
        )

        self.spr_teamstatus = (
            self.game.m_res.get_picture("Battle/icon_ball"),
            self.game.m_res.get_picture("Battle/icon_ball_empty"),
            self.game.m_res.get_picture("Battle/icon_ball_faint"),
            self.game.m_res.get_picture("Battle/icon_ball_status"),
        )

        self.spr_own = self.game.m_res.get_picture("Battle/icon_own")

        self.spr_statusbox = self.game.m_res.get_interface("statusbox")

        self.spr_attackcell = (
            self.game.m_res.get_interface("attackcell"),
            self.game.m_res.get_interface("attackcell_selected"),
        )

        self.spr_ballcell = (
            self.game.m_res.get_interface("ballcell"),
            self.game.m_res.get_interface("ballcell_selected"),
        )

        self.spr_attacktypes = self.game.m_res.attack_types

        self.agents = []
        if agents:
            self.agents = agents
        else:
            self.agents.append(self.init_agent("user", 0))
            self.agents.append(self.init_agent("random", 1))
        for agent in self.agents:
            agent.start(self.combat)

        self.lock_state = False
        self.need_to_redraw = True
        self.selection = 0
        self.state = states["topmenu"]
        self.game.r_aud.play_music("BGM/Battle wild.flac")
        self.particle_test = False
        self.particle_test_cooldown = 0.0
        self.end_time = ti.time()
        self.max_time = 1

    def init_agent(self, agent, team):
        if agent == "random":
            return AgentRand(self, team)
        if agent == "user":
            return AgentUser(self, team)

    def on_tick(self, time, frame_time):
        actions = []
        if self.state != states["action"] or self.particle_test:
            skip = False
            if self.particle_test and not self.lock:
                if self.particle_test_cooldown:
                    self.particle_test_cooldown = max(
                        0, self.particle_test_cooldown - frame_time
                    )
                else:
                    tackle = self.game.m_pbs.get_move(399).copy()
                    tackle.power = 0
                    actions.append(
                        (
                            ("attack", tackle),
                            (1, self.board.get_active(1)),
                            (0, self.board.get_active(0)),
                        )
                    )
                    actions.append(
                        (
                            ("attack", tackle),
                            (1, self.board.get_active(1)),
                            (0, self.board.get_active(0)),
                        )
                    )
            else:
                for i, agent in enumerate(self.agents):
                    if self.lock_state:
                        if self.board.switch[i]:
                            sendout = agent.get_sendout(self.combat)
                            if sendout is not None:
                                actions.append((("sendout", (i, sendout)), None, None))
                            else:
                                skip = True
                    else:
                        action = agent.get_action(self.combat)
                        if action is not None:
                            actions.append(action)
                        else:
                            skip = True
            if not skip:
                self.lock_state = False
                self.state = states["action"]
                self.pending_boards = self.combat.run_scene(actions)
                self.advance_board()

        self.redraw(time, frame_time)
        self.lock = self.render.render(time, frame_time)
        return True

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
        if self.need_to_redraw:
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.need_to_redraw = False

    def event_keypress(self, key, modifiers):
        if self.particle_test:
            return
        if self.lock == False:
            self.need_to_redraw = True
            if self.state == states["action"]:
                if key == "interact":
                    self.advance_board()
            else:
                if key == "down":
                    self.selection = (self.selection + 1) % self.max_selection
                    self.game.r_aud.effect("select")
                elif key == "up":
                    self.selection = (self.selection - 1) % self.max_selection
                    self.game.r_aud.effect("select")
                elif key == "left":
                    if self.state == states["topmenu"]:
                        self.selection = (self.selection - 2) % self.max_selection
                        self.game.r_aud.effect("select")
                elif key == "right":
                    if self.state == states["topmenu"]:
                        self.selection = (self.selection + 2) % self.max_selection
                        self.game.r_aud.effect("select")
                elif key == "interact":
                    self.game.r_aud.effect("confirm")
                    if self.state == states["topmenu"]:
                        if self.selection == 0:
                            self.state = states["actionmenu"]
                        elif self.selection == 1:
                            self.state = states["swapmenu"]
                        elif self.selection == 2:
                            self.state = states["ballmenu"]
                        elif self.selection == 3:
                            self.reg_action(("flee", None))
                    elif self.state == states["actionmenu"]:
                        self.reg_action(
                            ("attack", self.actor_1[0].actions[self.selection],)
                        )
                    elif self.state == states["swapmenu"]:
                        if self.board.teams[0][self.selection][1]["can_fight"]:
                            if self.lock_state:
                                for agent in self.agents:
                                    if type(agent) == AgentUser:
                                        agent.set_sendout(self.combat, self.selection)
                            else:
                                self.reg_action(("swap", self.selection,),)
                    elif self.state == states["ballmenu"]:
                        self.reg_action(("catch", self.selection))
                    self.selection = 0
                elif key == "backspace":
                    self.game.r_aud.effect("cancel")
                    if not self.lock_state:
                        self.game.r_aud.effect("cancel")
                        if self.state == states["actionmenu"]:
                            self.selection = 0
                        elif self.state == states["swapmenu"]:
                            self.selection = 1
                        elif self.state == states["ballmenu"]:
                            self.selection = 2
                        self.state = states["topmenu"]

        else:
            self.game.m_par.fast_forward = True

    @property
    def max_selection(self):
        if self.state == states["swapmenu"]:
            return len(self.game.inventory.members)
        return 4

    def reg_action(self, action):
        self.selection = 0

        user = (0, self.board.get_active(0))
        target = (1, self.board.get_active(1))
        if action[0] == "swap":
            user = (0, self.board.get_active(0))
            target = (0, action[1])
        if action[0] == "attack":
            user = (0, self.board.get_active(0))
            target = (1, self.board.get_active(1))
        if action[0] == "catch":
            user = (0, self.board.get_active(0))
            target = (1, self.board.get_active(1))
        action_desc = (action, user, target)
        for agent in self.agents:
            if type(agent) == AgentUser:
                self.agents[0].set_action(action_desc)

    def advance_board(self):
        self.lock_state = False
        if self.board.battle_end:
            self.end_battle()
            return
        if not self.pending_boards:
            self.need_to_redraw = True
            if any(self.board.switch):
                self.lock_state = True
                self.state = states["topmenu"]
                for i, boo in enumerate(self.board.switch):
                    if boo:
                        if type(self.agents[i]) == AgentUser:
                            self.state = states["swapmenu"]
                            self.lock_state = "user_switch"
                            self.agents[i].set_sendout(self.combat, None)
                return
            else:
                self.state = states["topmenu"]
                for agent in self.agents:
                    if type(agent) == AgentUser:
                        agent.set_action(None)
                    agent.start(self.combat)
                self.render.camera.reset()
                print("--- RESET STATES")
                return

        self.board = self.pending_boards.pop(0)

        if self.board.actor_1 != self.actor_1:
            if self.board.actor_1 == -1:
                self.render.set_pokemon(
                    None, 0
                )  # empty spriteset for if poke is fainted
            else:
                self.render.set_pokemon(self.board.actor_1[0].sprite, 0)
            self.actor_1 = self.board.actor_1
        if self.board.actor_2 != self.actor_2:
            if self.board.actor_2 == -1:
                self.render.set_pokemon(
                    None, 1
                )  # empty spriteset for if poke is fainted
            else:
                self.render.set_pokemon(self.board.actor_2[0].sprite, 1)
            self.actor_2 = self.board.actor_2

        self.need_to_redraw = True

        if self.board.skip:
            self.advance_board()
            return
        self.game.m_par.fast_forward = False

        if self.particle_test:
            try:
                self.render.do_particle(
                    self.particle_test,
                    self.board.user,
                    self.board.target,
                    miss=self.board.particle_miss,
                )
            except Exception as e:
                traceback.print_exc()
                self.particle_test_cooldown = 5.0
        else:
            self.render.do_particle(
                self.board.particle,
                self.board.user,
                self.board.target,
                miss=self.board.particle_miss,
            )
        self.end_time = ti.time()

    def synchronize(self):
        for i, member in enumerate(self.game.inventory.members):
            self.combat.board.sync_actor((0, i))
            member.from_series(self.board.get_actor((0, i)).series)
        # TODO transfer status effects.

    def end_battle(self):
        self.synchronize()
        self.game.m_gst.switch_state("overworld")

    @property
    def narrate(self):
        if self.state == states["action"]:
            return self.board.narration

        if self.state == states["actionmenu"]:
            action = self.actor_1[0].actions[self.selection]
            return action.description

        if self.state == states["swapmenu"]:
            name = self.game.inventory.fighter_names[self.selection]
            return f"Send out {name}."

        if self.state == states["ballmenu"]:
            # ball = self.game.inventory.get_pocket_items(3)[self.selection]
            return "blabla ik ben een bal"  # ball.description

        if self.state == states["topmenu"]:
            strings = [
                "Attack the enemy!",
                "Choose a Pokemon!",
                "Throw a Poke Ball!",
                "Run away!",
            ]
            return strings[self.selection]
        return "ERROR: Missing String"

    def exit_battle(self):
        self.game.m_gst.switch_state("overworld")

    def draw_interface(self, time, frame_time):
        if not len(self.pending_boards):
            if self.state == states["topmenu"]:
                # self.game.r_int.draw_rectangle(
                #     (0.80, 0.53), size=(0.15, 0.32), col="black"
                # )

                for i, name in enumerate(["Fight", "Pokemon", "Ball", "Run"]):
                    #     self.game.r_int.draw_text(
                    #         f"{self.selection == i and '' or ''}{name}",
                    #         (0.81, 0.54 + 0.08 * i),
                    #         size=(0.13, 0.06),
                    #         bcol=self.selection == i and "yellow" or "white",
                    #     )

                    self.game.r_int.draw_image(
                        self.spr_battlecell[self.selection == i and 1 or 0],
                        (0.85 + 0.9 * 0.09 * (i // 2), 0.63 + 0.89 * 0.16 * (i % 2)),
                        centre=True,
                    )

            elif self.state == states["actionmenu"]:
                # self.game.r_int.draw_rectangle(
                #     (0.685, 0.59), size=(0.29, 0.27), col="white"
                # )

                actionlist = self.actor_1[0].actions
                for i in range(min(len(actionlist), 4)):
                    self.game.r_int.draw_image(
                        self.spr_attacktypes[actionlist[i].type],
                        (0.6938, 0.607 + 0.065 * i),
                    )
                    self.game.r_int.draw_image(
                        self.spr_attackcell[self.selection == i and 1 or 0],
                        (0.69, 0.6 + 0.065 * i),
                    )
                    self.game.r_int.draw_text(
                        actionlist[i]["name"],
                        (0.725, 0.607 + 0.065 * i),
                        size=(0.20, 0.06),
                        bcol=None,
                        col="white",
                    )
                    self.game.r_int.draw_text(
                        f"{actionlist[i].pp}/{actionlist[i].pp}",
                        (0.93, 0.616 + 0.065 * i),
                        size=(0.20, 0.06),
                        bcol=None,
                        fsize=6,
                        col="white",
                    )

            elif self.state == states["swapmenu"]:
                self.game.r_int.draw_rectangle(
                    (0.685, 0.49), size=(0.22, 0.4), col="white"
                )

                for i, name in enumerate(self.game.inventory.fighter_names):
                    self.game.r_int.draw_image(
                        self.spr_ballcell[self.selection == i and 1 or 0],
                        (0.69, 0.5 + 0.065 * i),
                    )
                    self.game.r_int.draw_text(
                        name, (0.725, 0.507 + 0.065 * i), size=(0.20, 0.06), bcol=None,
                    )

            elif self.state == states["ballmenu"]:
                self.game.r_int.draw_rectangle(
                    (0.685, 0.49), size=(0.22, 0.4), col="white"
                )

                balls = self.game.inventory.get_pocket_items(3)
                if balls:
                    for i in range(len(balls)):
                        self.game.r_int.draw_image(
                            self.spr_ballcell[self.selection == i and 1 or 0],
                            (0.69, 0.5 + 0.065 * i),
                        )
                        self.game.r_int.draw_text(
                            balls[i].itemname,
                            (0.725, 0.507 + 0.065 * i),
                            size=(0.20, 0.06),
                            bcol=None,
                        )
                else:
                    self.game.r_int.draw_image(
                        self.spr_ballcell[1], (0.69, 0.5),
                    )
                    self.game.r_int.draw_text(
                        f"No balls!", (0.725, 0.507), size=(0.20, 0.06), bcol=None,
                    )
        # HP Bars & EXP bar
        # Ally
        lining = 0.008
        fighter = self.board.get_actor((0, self.board.get_active(0)))
        rel_hp = self.board.get_relative_hp((0, self.board.get_active(0)))
        x_off = 0.08
        x_size = 0.28

        # HP bar
        self.game.r_int.draw_rectangle(
            (x_off + 0.028, 0.14), size=(x_size, 0.035), col="grey",
        )
        if rel_hp > 0 and self.lock_state != "user_switch":
            self.game.r_int.draw_rectangle(
                (x_off + 0.028, 0.14),
                size=(x_size * rel_hp, 0.035),
                col=rel_hp > 0.5 and "green" or rel_hp > 0.2 and "yellow" or "red",
            )
        # EXP bar
        self.game.r_int.draw_rectangle(
            (x_off + 0.029, 0.19), size=(0.223, 0.014), col="grey",
        )
        rel_xp = self.board.get_relative_xp((0, self.board.get_active(0)))
        if rel_xp > 0 and self.lock_state != "user_switch":
            self.game.r_int.draw_rectangle(
                (x_off + 0.029, 0.19), size=(0.223 * rel_xp, 0.014), col="blue",
            )

        self.game.r_int.draw_image(
            self.spr_battlestatus[0], (x_off, 0.08), centre=False,
        )

        if self.lock_state != "user_switch":
            self.game.r_int.draw_text(
                fighter.name, (x_off + 0.015, 0.09), size=(x_size / 2, 0.05), bcol=None,
            )

        for i in range(6):
            print(self.board.teams[0][i][1])
            self.game.r_int.draw_image(
                self.spr_teamstatus[
                    (0 if self.board.teams[0][i][1]["can_fight"] else 2)
                    if i < len(self.board.teams[0])
                    else 1
                ],
                (x_off + 0.168 + 0.026 * i, 0.107),
                centre=True,
            )

        # Enemy
        lining = 0.008
        fighter = self.board.get_actor((1, self.board.get_active(1)))
        rel_hp = self.board.get_relative_hp((1, self.board.get_active(1)))
        x_off = 0.6
        x_size = 0.28
        # HP bar
        self.game.r_int.draw_rectangle(
            (x_off + 0.028, 0.14), size=(x_size, 0.035), col="grey",
        )
        if rel_hp > 0:
            self.game.r_int.draw_rectangle(
                (x_off + 0.028, 0.14),
                size=(x_size * rel_hp, 0.035),
                col=rel_hp > 0.5 and "green" or rel_hp > 0.2 and "yellow" or "red",
            )
        # self.game.r_int.draw_rectangle(
        #     (x_off - lining, 0.05 - lining),
        #     size=(x_size / 2 + 2 * lining, 0.05 + 2 * lining),
        #     col="black",
        # )
        # self.game.r_int.draw_rectangle(
        #     (x_off - lining, 0.10 - lining),
        #     size=(x_size + 2 * lining, 0.05 + 2 * lining),
        #     col="black",
        # )
        self.game.r_int.draw_image(
            self.spr_battlestatus[1], (x_off, 0.08), centre=False,
        )
        self.game.r_int.draw_text(
            fighter.name, (x_off + 0.175, 0.09), size=(x_size / 2, 0.05), bcol=None,
        )
        self.game.r_int.draw_image(
            self.spr_own, (x_off + 0.172, 0.11), centre=True,
        )
        for i in range(6):
            self.game.r_int.draw_image(
                self.spr_teamstatus[
                    (0 if self.board.teams[1][i][1]["can_fight"] else 2)
                    if i < len(self.board.teams[1])
                    else 1
                ],
                (x_off + 0.016 + 0.026 * (5 - i), 0.107),
                centre=True,
            )

        # Narrator
        # self.game.r_int.draw_rectangle((0, 0.9), to=(1, 1), col="black")
        self.game.r_int.draw_image(
            self.spr_statusbox, (0.0035, 0.9),
        )
        self.game.r_int.draw_text(
            self.narrate, (0.01, 0.91), to=(0.99, 0.99), bcol=None
        )

