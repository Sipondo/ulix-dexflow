import traceback

import time as ti

from .basegamestate import BaseGameState

from ulivy.particle.battlescene import BattleScene

from ulivy.combat.combatscene import CombatScene

from ulivy.combat.agent.agentrand import AgentRand
from ulivy.combat.agent.agentuser import AgentUser

from ..combat.action import ActionType, Action
import enum


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
        print("STARTING A FIGHT AGAINST:", enemy_team)
        if particle_test:
            self.game.inventory.init_random_member()

        self.game.r_fbo.disable_overworld()
        # Renderer setup
        self.scene = BattleScene(self.game)
        self.game.r_fbo.fbo_add_widget(self.scene)

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
            print("NEW ACTORS!", self.actors)

        self.lock_state = False
        self.action_choice = 0
        self.selection = 0
        self.state = BattleStates.TOPMENU

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

    def update(self, time, frame_time):
        # self.scene.render(time, frame_time)
        # return  # TODO: ulivy
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
        self.scene.update(time, frame_time)
        self.lock = self.scene.render(time, frame_time)
        return True

    def set_to_action(self):
        # TODO: remove
        self.state = BattleStates.ACTION

    def on_exit(self):
        pass

    def event_keypress(self, key, modifiers):
        return

    def reg_action(self, action):
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
            # self.game.r_int.fade = True
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
                pass
                self.state = BattleStates.TOPMENU
            self.game.m_cam.reset()
            print("--- RESET STATES")
            # TODO: remove
            self.game.r_uin.current_ui.reset_state()
            return

        self.board = self.pending_boards.pop(0)
        for i in range(self.combat.teams_n):
            if self.board.get_active_actor(i) != self.actors[i]:
                # if self.board.get_active_actor(i) == -1:
                #     self.scene.set_pokemon(
                #         None, i
                #     )  # empty spriteset for if poke is fainted
                # else:
                #     self.scene.set_pokemon(self.board.get_active_actor(i).sprite, i)
                self.actors[i] = self.board.get_active_actor(i)

        if self.board.skip:
            self.advance_board()
            return
        self.game.m_par.fast_forward = False

        if self.particle_test:
            try:
                self.scene.do_particle(
                    self.particle_test,
                    self.board.user,
                    self.board.target,
                    miss=self.board.particle_miss,
                )
            except Exception as e:
                traceback.print_exc()
                self.particle_test_cooldown = 5.0
        else:
            self.scene.do_particle(
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
        # self.game.r_int.fade = False
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
                (0, 0,), fade=False,
            )
            self.game.m_gst.switch_state("overworld")
            return
        self.game.m_gst.switch_state("evolve")
