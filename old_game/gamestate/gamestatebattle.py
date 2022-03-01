import traceback

import time as ti
import enum

from .basegamestate import BaseGameState

from game.particle.battlerender import BattleRender
from game.combat.combatscene import CombatScene
from game.combat.agent.agentrand import AgentRand
from game.combat.agent.agentuser import AgentUser

from ..combat.action import ActionType, Action


class BattleStates(enum.Enum):
    ACTION = enum.auto()
    TOPMENU = enum.auto()
    ACTIONMENU = enum.auto()
    SWAPMENU = enum.auto()
    BALLMENU = enum.auto()


class GameStateBattle(BaseGameState):
    def on_enter(
        self, battle_type="trainer", enemy_team=None, agents=None, particle_test=False
    ):
        if particle_test:
            self.game.inventory.init_random_member()

        # Renderer setup
        self.render = BattleRender(self.game)

        self.game.r_int.fade = False
        self.game.r_int.letterbox = False

        self.render.camera.reset()

        self.render.set_pokemon(None, 0)
        self.render.set_pokemon(None, 1)

        self.spr_battlecell = ("battlecell", "battlecell_selected")

        self.spr_battlestatus = (
            "battlestatus_ours",
            "battlestatus_theirs",
        )

        self.spr_teamstatus = (
            "battle/icon_ball",
            "battle/icon_ball_empty",
            "battle/icon_ball_faint",
            "battle/icon_ball_status",
        )

        self.spr_own = "battle/icon_own"

        self.spr_statusbox = "statusbox"

        self.spr_attackcell = (
            "attackcell",
            "attackcell_selected",
        )

        self.spr_ballcell = (
            "ballcell",
            "ballcell_selected",
        )

        self.spr_attackwindow = "attackwindow"
        self.spr_ballwindow = "ballwindow"
        self.spr_switchwindow = "switchwindow"

        self.spr_actionbuttons = ("attack", "switch", "throw_ball", "run")
        self.spr_attacktypes = self.game.m_res.attack_types

        for x in (
            self.spr_battlecell
            + self.spr_battlestatus
            + self.spr_teamstatus
            + (self.spr_own,)
            + (self.spr_statusbox,)
            + self.spr_attackcell
            + self.spr_ballcell
            + (self.spr_attackwindow,)
            + (self.spr_ballwindow,)
            + (self.spr_switchwindow,)
            + self.spr_actionbuttons
            + tuple(self.spr_attacktypes.values())
        ):
            self.game.r_int.load_sprite(x)

        self.game.r_int.init_sprite_drawer()

        if len(self.game.inventory.members) < 1:
            self.game.inventory.members.append(self.game.inventory.init_random_member())

        # Combat setup
        self.combat = CombatScene(
            self.game,
            ([x.series for x in self.game.inventory.members], enemy_team or [1, 2]),
            battle_type=battle_type,
        )

        self.battle_type = battle_type

        self.board = self.combat.board
        self.pending_boards = []

        self.actors = []
        for i in range(2):
            self.actors.append(self.board.get_active_actor(i))

        self.lock_state = False
        self.action_choice = 0
        self.selection = 0
        self.state = BattleStates.TOPMENU
        self.game.r_aud.play_music("BGM/battle wild.flac")
        self.particle_test = particle_test
        self.particle_test_cooldown = 0.0
        self.end_time = ti.time()
        self.max_time = 1

        self.to_end = False

        self.time_lock = 0.5
        self.time_press = None

        _agents = []
        if agents:
            _agents = agents
        else:
            _agents.append(self.init_agent("user", 0))
            _agents.append(self.init_agent("random", 1))

        self.init_battle(_agents)

    def init_battle(self, agents):
        actions = self.combat.init_battle(agents)
        self.pending_boards = self.combat.prepare_scene(actions)
        self.state = BattleStates.ACTION
        self.advance_board()

    def init_agent(self, agent_str: str, team: int):
        if agent_str == "random":
            return AgentRand(self.game, self.combat, team)
        if agent_str == "user":
            return AgentUser(self.game, self.combat, team)

    def on_tick(self, time, frame_time):
        if self.time_lock > 0:
            self.time_lock = max(0, self.time_lock - frame_time)

            if self.time_lock == 0 and self.time_press is not None:
                print("PRESSING", self.time_press)
                self.event_keypress(self.time_press, [])
                self.time_press = None
        else:
            if self.to_end:
                self.end_battle()
                return

        actions = []
        if self.state != BattleStates.ACTION or self.particle_test:
            if self.particle_test and not self.lock:
                if self.particle_test_cooldown:
                    self.particle_test_cooldown = max(
                        0, self.particle_test_cooldown - frame_time
                    )
                else:
                    tackle = self.game.m_pbs.get_move(399).copy()
                    tackle.power = 0
                    actions.append(
                        Action(
                            ActionType.ATTACK,
                            a_data=tackle,
                            user=(1, self.board.get_active(1)),
                            target=(0, self.board.get_active(0)),
                        )
                    )
                    actions.append(
                        Action(
                            ActionType.ATTACK,
                            a_data=tackle,
                            user=(1, self.board.get_active(1)),
                            target=(0, self.board.get_active(0)),
                        )
                    )

            else:
                actions = self.combat.get_actions()
            if actions:
                self.state = BattleStates.ACTION
                self.pending_boards = self.combat.prepare_scene(actions)
                self.lock_state = False
                self.advance_board()

        # self.redraw(time, frame_time)
        self.lock = self.render.render(time, frame_time)
        return True

    def on_exit(self):
        pass

    def on_render(self, time, frame_time):
        self.draw_interface(time, frame_time)

    def event_keypress(self, key, modifiers):
        if self.particle_test:
            return

        if self.time_lock > 0:
            self.time_press = key
            return

        if self.lock == False:
            if self.state == BattleStates.ACTION:
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
                    if self.state == BattleStates.TOPMENU:
                        self.selection = (self.selection - 2) % self.max_selection
                        self.game.r_aud.effect("select")
                elif key == "right":
                    if self.state == BattleStates.TOPMENU:
                        self.selection = (self.selection + 2) % self.max_selection
                        self.game.r_aud.effect("select")
                elif key == "interact":
                    self.game.r_aud.effect("confirm")
                    if self.state == BattleStates.TOPMENU:
                        if self.selection == 0:
                            self.state = BattleStates.ACTIONMENU
                            self.selection = self.action_choice
                        elif self.selection == 1:
                            self.state = BattleStates.SWAPMENU
                        elif self.selection == 2 and self.battle_type != "trainer":
                            self.state = BattleStates.BALLMENU
                        elif self.selection == 3 and self.battle_type != "trainer":
                            self.reg_action(Action(ActionType.RUN))
                    elif self.state == BattleStates.ACTIONMENU:
                        if self.lock_state:
                            self.reg_action(
                                Action(ActionType.FORGET_MOVE, a_index=self.selection)
                            )
                        else:
                            self.action_choice = self.selection
                            self.reg_action(
                                Action(ActionType.ATTACK, a_index=self.selection)
                            )
                    elif self.state == BattleStates.SWAPMENU:
                        if (
                            self.board.teams[0][self.selection][1].can_fight
                            and self.board.get_active(0) != self.selection
                        ):
                            if self.lock_state:
                                self.reg_action(
                                    Action(ActionType.SENDOUT, a_index=self.selection)
                                )
                            else:
                                self.reg_action(
                                    Action(ActionType.SWITCH, a_index=self.selection)
                                )
                    elif self.state == BattleStates.BALLMENU:
                        if self.game.inventory.get_pocket_items(3):
                            self.reg_action(
                                Action(ActionType.CATCH, a_index=self.selection)
                            )
                    if self.state != BattleStates.ACTIONMENU:
                        self.selection = 0
                elif key == "backspace" or key == "menu":
                    self.game.r_aud.effect("cancel")
                    if not self.lock_state:
                        self.game.r_aud.effect("cancel")
                        if self.state == BattleStates.ACTIONMENU:
                            self.selection = 0
                        elif self.state == BattleStates.SWAPMENU:
                            self.selection = 1
                        elif self.state == BattleStates.BALLMENU:
                            self.selection = 2
                        elif self.state == BattleStates.TOPMENU:
                            self.combat.deregister_action()
                        self.state = BattleStates.TOPMENU
        else:
            self.game.m_par.fast_forward = False  # True

    @property
    def max_selection(self):
        if self.state == BattleStates.SWAPMENU:
            return len(self.game.inventory.members)
        if self.state == BattleStates.ACTIONMENU:
            return len(self.actors[0].actions)
        if self.state == BattleStates.BALLMENU:
            return len(self.game.inventory.get_pocket_items(3))
        return 4

    def reg_action(self, action: Action):
        self.selection = 0

        user = (0, self.board.get_active(0))
        target = (1, self.board.get_active(1))
        if action.a_type == ActionType.ATTACK:
            action.a_data = self.board.get_actor(user).actions[action.a_index]
            user = (0, self.board.get_active(0))
            target = (1, self.board.get_active(1))
        if action.a_type == ActionType.SWITCH:
            user = (0, self.board.get_active(0))
            target = (0, action.a_index)
        if action.a_type == ActionType.CATCH:
            user = (0, self.board.get_active(0))
            target = (1, self.board.get_active(1))
        if action.a_type == ActionType.FORGET_MOVE:
            action.a_data = self.board.get_actor(user).actions[action.a_index]
            user = (0, self.board.get_active(0))
            target = (0, self.board.get_active(0))
        if action.a_type == ActionType.SENDOUT:
            user = (0, self.board.get_active(0))
            target = (0, action.a_index)
        if action.a_type == ActionType.RUN:
            user = (0, self.board.get_active(0))
            target = (0, self.board.get_active(0))
        action.user = user
        action.target = target
        self.combat.register_action(action)

    def advance_board(self):
        self.lock_state = False
        if self.board.battle_end:
            self.to_end = True
            self.game.r_int.fade = True
            self.time_lock = 0.5
            return
        if not self.pending_boards:
            if self.combat.board.new_move:
                self.state = BattleStates.ACTIONMENU
                self.lock_state = "user_forget_move"
            elif self.combat.board.fainted:
                self.state = BattleStates.SWAPMENU
                self.lock_state = "user_switch"
            else:
                self.state = BattleStates.TOPMENU
            self.render.camera.reset()
            print("--- RESET STATES")
            return

        self.board = self.pending_boards.pop(0)
        for i in range(self.combat.teams_n):
            if self.board.get_active_actor(i) != self.actors[i]:
                if self.board.get_active_actor(i) == -1:
                    self.render.set_pokemon(
                        None, i
                    )  # empty spriteset for if poke is fainted
                else:
                    self.render.set_pokemon(self.board.get_active_actor(i).sprite, i)
                self.actors[i] = self.board.get_active_actor(i)

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
                move_data=self.board.move_data,
            )
        self.end_time = ti.time()

    def synchronize(self):
        for i, member in enumerate(self.board.teams[0]):
            self.combat.board.sync_actor((0, i))
            self.game.inventory.members[i].from_series(
                self.board.get_actor((0, i)).series
            )

    def end_battle(self):
        self.synchronize()
        self.game.battle_result = 0 if self.board.has_fighter(0) else 1
        self.game.r_int.fade = False
        if self.game.battle_result == 1:
            for member in self.game.inventory.members:
                member.current_hp = member.stats[0]
                member.status = None
            self.game.m_act.flush()
            self.game.m_map.set_level(
                self.game.m_map.convert_mapstring_to_key(self.game.m_map.hospital)
            )
            self.game.m_ent.player.game_position = (7, 6)
            self.game.r_wld.offset = (0.5, 13 / 16)
            self.game.m_col.offset = (0.5, 13 / 16)
            self.game.r_wld.set_map_via_manager(
                (
                    0,
                    0,
                ),
                fade=False,
            )
            self.game.m_gst.switch_state("overworld")
            return
        self.game.m_gst.switch_state("evolve")

    @property
    def narrate(self):
        if self.state == BattleStates.ACTION:
            return self.board.narration

        if self.state == BattleStates.ACTIONMENU:
            action = self.actors[0].actions[self.selection]
            return (
                action.description
                if not self.lock_state
                else f"Forget {action['name']}?"
            )

        if self.state == BattleStates.SWAPMENU:
            name = self.game.inventory.fighter_names[self.selection]
            return f"Send out {name}."

        if self.state == BattleStates.BALLMENU:
            # ball = self.game.inventory.get_pocket_items(3)[self.selection]
            return "Throw a ball to catch the Pokémon!"  # ball.description

        if self.state == BattleStates.TOPMENU:
            strings = [
                "Attack the enemy!",
                "Choose a Pokemon!",
                "Throw a Poke Ball!",
                "Run away!",
            ]
            return strings[self.selection]
        return "ERROR: Missing String"

    def draw_interface(self, time, frame_time):
        if not len(self.pending_boards) or self.lock_state:
            if self.state == BattleStates.TOPMENU:
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
                    self.game.r_int.draw_image(
                        self.spr_actionbuttons[i],
                        (0.85 + 0.9 * 0.09 * (i // 2), 0.63 + 0.89 * 0.16 * (i % 2)),
                        centre=True,
                    )

            elif self.state == BattleStates.ACTIONMENU:
                # self.game.r_int.draw_rectangle(
                #     (0.685, 0.59), size=(0.29, 0.27), col="white"
                # )
                self.game.r_int.draw_image(self.spr_attackwindow, (0.685, 0.59))
                actionlist = self.actors[0].actions
                for i in range(min(len(actionlist), 5)):
                    self.game.r_int.draw_image(
                        self.spr_attacktypes[actionlist[i]["type"].lower()],
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
                        col="black",
                    )
                    self.game.r_int.draw_text(
                        f"{actionlist[i]['pp']}/{actionlist[i]['pp']}",
                        (0.93, 0.616 + 0.065 * i),
                        size=(0.20, 0.06),
                        bcol=None,
                        fsize=6,
                        col="black",
                    )

            elif self.state == BattleStates.SWAPMENU:
                self.game.r_int.draw_image(self.spr_switchwindow, (0.685, 0.49))

                for i, name in enumerate(self.game.inventory.fighter_names):
                    self.game.r_int.draw_image(
                        self.spr_ballcell[self.selection == i and 1 or 0],
                        (0.69, 0.5 + 0.063 * i),
                    )
                    self.game.r_int.draw_text(
                        name,
                        (0.725, 0.507 + 0.063 * i),
                        size=(0.20, 0.06),
                        bcol=None,
                    )

            elif self.state == BattleStates.BALLMENU:
                self.game.r_int.draw_image(self.spr_ballwindow, (0.685, 0.616))

                balls = self.game.inventory.get_pocket_items(3)
                if balls:
                    for i in range(len(balls)):
                        self.game.r_int.draw_image(
                            self.spr_ballcell[self.selection == i and 1 or 0],
                            (0.69, 0.626 + 0.063 * i),
                        )
                        self.game.r_int.draw_text(
                            balls[i]["itemname"],
                            (0.725, 0.633 + 0.063 * i),
                            size=(0.20, 0.06),
                            bcol=None,
                        )
                else:
                    self.game.r_int.draw_image(
                        self.spr_ballcell[1],
                        (0.69, 0.626),
                    )
                    self.game.r_int.draw_text(
                        f"No balls!",
                        (0.725, 0.633),
                        size=(0.20, 0.06),
                        bcol=None,
                    )
        # HP Bars & EXP bar
        # Ally
        lining = 0.008
        fighter = self.board.get_actor((0, self.board.get_active(0)))
        rel_hp = self.board.get_relative_hp((0, self.board.get_active(0)))
        level = self.board.get_data((0, self.board.get_active(0))).level
        x_off = 0.08
        x_size = 0.28

        # HP bar
        self.game.r_int.draw_rectangle(
            (x_off + 0.028, 0.14),
            size=(x_size, 0.035),
            col="grey",
        )
        if rel_hp > 0 and self.lock_state != "user_switch":
            self.game.r_int.draw_rectangle(
                (x_off + 0.028, 0.14),
                size=(x_size * rel_hp, 0.035),
                col=rel_hp > 0.5 and "darkgreen" or rel_hp > 0.2 and "yellow" or "red",
            )
        # EXP bar
        self.game.r_int.draw_rectangle(
            (x_off + 0.029, 0.19),
            size=(0.223, 0.014),
            col="grey",
        )
        rel_xp = self.board.get_relative_xp((0, self.board.get_active(0)))
        if rel_xp > 0 and self.lock_state != "user_switch":
            self.game.r_int.draw_rectangle(
                (x_off + 0.029, 0.19),
                size=(0.223 * rel_xp, 0.014),
                col="blue",
            )

        self.game.r_int.draw_image(
            self.spr_battlestatus[0],
            (x_off, 0.08),
            centre=False,
        )

        if self.lock_state != "user_switch":
            self.game.r_int.draw_text(
                f"Lv.{level}",
                (x_off + 0.01, 0.10),
                size=(x_size / 2, 0.05),
                bcol=None,
                fsize=6,
            )
            self.game.r_int.draw_text(
                fighter.name,
                (x_off + 0.04, 0.09),
                size=(x_size / 2, 0.05),
                bcol=None,
                fsize=10,
            )

        for i in range(6):
            self.game.r_int.draw_image(
                self.spr_teamstatus[
                    (0 if self.board.get_data((0, i)).can_fight else 2)
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
        level = self.board.get_data((1, self.board.get_active(1))).level
        x_off = 0.6
        x_size = 0.28
        # HP bar
        self.game.r_int.draw_rectangle(
            (x_off + 0.028, 0.14),
            size=(x_size, 0.035),
            col="grey",
        )
        if rel_hp > 0:
            self.game.r_int.draw_rectangle(
                (x_off + 0.028, 0.14),
                size=(x_size * rel_hp, 0.035),
                col=rel_hp > 0.5 and "darkgreen" or rel_hp > 0.2 and "yellow" or "red",
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
            self.spr_battlestatus[1],
            (x_off, 0.08),
            centre=False,
        )
        self.game.r_int.draw_text(
            f"Lv.{level}",
            (x_off + 0.178, 0.10),
            size=(x_size / 2, 0.05),
            bcol=None,
            fsize=6,
        )
        self.game.r_int.draw_text(
            fighter.name,
            (x_off + 0.205, 0.09),
            size=(x_size / 2, 0.05),
            bcol=None,
            fsize=10,
        )
        self.game.r_int.draw_image(
            self.spr_own,
            (x_off + 0.172, 0.11),
            centre=True,
        )
        for i in range(6):
            self.game.r_int.draw_image(
                self.spr_teamstatus[
                    (0 if self.board.get_data((1, i)).can_fight else 2)
                    if i < len(self.board.teams[1])
                    else 1
                ],
                (x_off + 0.016 + 0.026 * (5 - i), 0.107),
                centre=True,
            )

        # Narrator
        # self.game.r_int.draw_rectangle((0, 0.9), to=(1, 1), col="black")
        self.game.r_int.draw_image(
            self.spr_statusbox,
            (0.0035, 0.9),
        )
        self.game.r_int.draw_text(
            self.narrate, (0.01, 0.91), to=(0.99, 0.99), bcol=None
        )
