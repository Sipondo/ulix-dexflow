from .basegamestate import BaseGameState

from game.particle.battlerender import BattleRender
from game.combat.combatscene import CombatScene
from game.combat.agent.agentrand import AgentRand
from game.combat.agent.agentuser import AgentUser
import traceback

import time as ti

states = {"action": 0, "topmenu": 1, "actionmenu": 2, "swapmenu": 3, "ballmenu": 4}


class GameStateBattle(BaseGameState):
    def on_enter(self, teams=None, agents=None):
        self.render = BattleRender(self.game)
        self.combat = CombatScene(
            self.game, [x.series for x in self.game.inventory.members], [1, 2]
        )
        self.render.camera.reset()
        self.board = self.combat.board
        self.pending_boards = []

        self.actor_1 = self.board.actor_1
        self.actor_2 = self.board.actor_2

        # TODO move away as it should be initiated as a move
        self.render.set_pokemon(self.actor_1[0].sprite, 0)
        self.render.set_pokemon(self.actor_2[0].sprite, 1)

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
        if self.state != states["action"]:
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
                        (("attack", tackle), (1, self.board.get_active(1)), (0, self.board.get_active(0)))
                    )
                    actions.append(
                        (("attack", tackle), (1, self.board.get_active(1)), (0, self.board.get_active(0)))
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
                        if self.lock_state:
                            for agent in self.agents:
                                if type(agent) == AgentUser:
                                    agent.set_sendout(self.selection)
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
                            self.lock_state = True
                            self.agents[i].set_action(None)
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
                self.render.set_pokemon(None, 0)  # empty spriteset for if poke is fainted
            else:
                self.render.set_pokemon(self.board.actor_1[0].sprite, 0)
            self.actor_1 = self.board.actor_1
        if self.board.actor_2 != self.actor_2:
            if self.board.actor_2 == -1:
                self.render.set_pokemon(None, 1)  # empty spriteset for if poke is fainted
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
            print(self.game.inventory.get_pocket_items(3)[self.selection])
            ball = self.game.inventory.get_pocket_items(3)[self.selection]
            return ball.description

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
                self.game.r_int.draw_rectangle(
                    (0.80, 0.53), size=(0.15, 0.32), col="black"
                )

                for i, name in enumerate(["Fight", "Pokemon", "Ball", "Run"]):
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{name}",
                        (0.81, 0.54 + 0.08 * i),
                        size=(0.13, 0.06),
                        bcol=self.selection == i and "yellow" or "white",
                    )

            elif self.state == states["actionmenu"]:
                self.game.r_int.draw_rectangle(
                    (0.68, 0.53), size=(0.22, 0.32), col="black"
                )

                actionnames = [x["name"] for x in self.actor_1[0].actions]
                for i in range(min(len(actionnames), 4)):
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{actionnames[i]}",
                        (0.69, 0.54 + 0.08 * i),
                        size=(0.20, 0.06),
                        bcol=self.selection == i and "yellow" or "white",
                    )

            elif self.state == states["swapmenu"]:
                self.game.r_int.draw_rectangle(
                    (0.68, 0.37), size=(0.22, 0.48), col="black"
                )

                for i, name in enumerate(self.game.inventory.fighter_names):
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{name}",
                        (0.69, 0.38 + 0.08 * i),
                        size=(0.20, 0.06),
                        bcol=self.selection == i and "yellow" or "white",
                    )

            elif self.state == states["ballmenu"]:
                self.game.r_int.draw_rectangle(
                    (0.68, 0.53), size=(0.22, 0.32), col="black"
                )

                balls = self.game.inventory.get_pocket_items(3)
                for i in range(4):
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{balls[i].name}",
                        (0.69, 0.54 + 0.08 * i),
                        size=(0.20, 0.06),
                        bcol=self.selection == i and "yellow" or "white",
                    )
        # HP Bars
        lining = 0.008
        fighters = []
        rel_hp = []
        for i in range(2):
            active_i = self.board.get_active(i)
            rel_hp.append(self.board.get_relative_hp((i, active_i)))
            fighters.append(self.board.get_actor((i, active_i)))
        for ((fighter, health), x, size_x) in (
            ((fighters[0], rel_hp[0]), 0.1, 0.3),
            ((fighters[1], rel_hp[1]), 0.6, 0.3),
        ):
            if health > 0:
                self.game.r_int.draw_rectangle(
                    (x - lining, 0.05 - lining),
                    size=(size_x / 2 + 2 * lining, 0.05 + 2 * lining),
                    col="black",
                )
                self.game.r_int.draw_rectangle(
                    (x - lining, 0.10 - lining),
                    size=(size_x + 2 * lining, 0.05 + 2 * lining),
                    col="black",
                )
                self.game.r_int.draw_text(
                    fighter.name, (x, 0.05), size=(size_x / 2, 0.05),
                )
                # HP bar
                self.game.r_int.draw_rectangle(
                    (x, 0.1), size=(size_x, 0.05), col="grey",
                )
                self.game.r_int.draw_rectangle(
                    (x, 0.1),
                    size=(size_x * health, 0.05),
                    col=health > 0.5 and "green" or health > 0.2 and "yellow" or "red",
                )
        # EXP bar
        self.game.r_int.draw_rectangle(
            (0.1, 0.158), size=(0.25, 0.012), col="grey",
        )
        rel_xp = self.board.get_relative_xp((0, self.board.get_active(0)))
        if rel_xp > 0:
            self.game.r_int.draw_rectangle(
                (0.1, 0.158),
                size=(0.25 * rel_xp, 0.012),
                col="blue",
            )
        # Narrator
        self.game.r_int.draw_rectangle((0, 0.9), to=(1, 1), col="black")
        self.game.r_int.draw_text(self.narrate, (0.01, 0.91), to=(0.99, 0.99))
