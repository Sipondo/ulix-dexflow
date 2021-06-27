from .basegamestate import BaseGameState

from game.particle.battlerender import BattleRender
from game.combat.combatscene import CombatScene
import traceback

states = {"action": 0, "topmenu": 1, "actionmenu": 2, "swapmenu": 3, "ballmenu": 4}


class GameStateBattle(BaseGameState):
    def on_enter(self):
        self.render = BattleRender(self.game)
        self.combat = CombatScene(
            self.game, [x.series for x in self.game.inventory.members], [1]
        )
        self.render.camera.reset()
        self.board = self.combat.board
        self.pending_boards = []

        # TODO move away as it should be initiated as a move
        self.render.set_pokemon(self.board.actor_1[0].sprite, 0)
        self.render.set_pokemon(self.board.actor_2[0].sprite, 1)

        self.need_to_redraw = True

        self.selection = 0
        self.state = states["topmenu"]
        self.game.r_aud.play_music("BGM/Battle wild.flac")
        self.particle_test = False
        self.particle_test_cooldown = 0.0

    def on_tick(self, time, frame_time):
        if self.particle_test and not self.lock:
            if self.particle_test_cooldown:
                self.particle_test_cooldown = max(
                    0, self.particle_test_cooldown - frame_time
                )
            elif self.state == states["action"]:
                self.advance_board()
            else:
                self.reg_action(("attack", self.board.actor_1[0].actions[0],))

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
                            ("attack", self.board.actor_1[0].actions[self.selection],)
                        )
                    elif self.state == states["swapmenu"]:
                        self.reg_action(("swap", self.selection,),)
                    elif self.state == states["ballmenu"]:
                        self.reg_action(("catch", self.selection))
                    self.selection = 0
                elif key == "backspace":
                    self.game.r_aud.effect("cancel")
                    if self.state == states["actionmenu"]:
                        self.selection = 0
                    elif self.state == states["swapmenu"]:
                        self.selection = 1
                    elif self.state == states["ballmenu"]:
                        self.selection = 2
                    self.state = states["topmenu"]
        else:
            # TODO: implement ff
            self.game.m_par.fast_forward = True

    @property
    def max_selection(self):
        if self.state == states["swapmenu"]:
            return len(self.game.inventory.members)
        return 4

    def reg_action(self, action):
        # TODO: src, trg
        self.selection = 0
        actions = []
        actions.append(
            (action, (0, self.board.get_active(0)), (1, self.board.get_active(1)))
        )
        actions.append(
            (action, (1, self.board.get_active(1)), (0, self.board.get_active(0)))
        )
        self.state = states["action"]
        self.pending_boards = self.combat.run_scene(actions)
        self.advance_board()

    def show_stuff(self, partname):
        print("PARTICLES!!!")

    def advance_board(self):
        if not self.pending_boards:
            self.state = states["topmenu"]
            self.render.camera.reset()
            print("--- RESET STATES")
            return

        self.board = self.pending_boards.pop(0)
        if self.board.battle_end:
            self.end_battle()
            return
        # TODO: do particle self.board.particle
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

    def synchronize(self):
        # TODO battle rewards/punish, save new party health, PP, etc
        pass

    def end_battle(self):
        self.synchronize()
        self.game.m_gst.switch_state("overworld")

    @property
    def narrate(self):
        if self.state == states["action"]:
            return self.board.narration

        if self.state == states["actionmenu"]:
            action = self.board.actor_1[0].actions[self.selection]
            return action.description

        if self.state == states["swapmenu"]:
            name = self.game.inventory.fighter_names[self.selection]
            return f"Swap with {name}."

        if self.state == states["ballmenu"]:
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

                actionnames = [x["name"] for x in self.board.actor_1[0].actions]
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
                for i, k in enumerate(balls):
                    self.game.r_int.draw_text(
                        f"{self.selection == i and '' or ''}{k.name}",
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
            self.game.r_int.draw_rectangle(
                (x, 0.1), size=(size_x, 0.05), col="grey",
            )
            self.game.r_int.draw_rectangle(
                (x, 0.1),
                size=(size_x * health, 0.05),
                col=health > 0.5 and "green" or health > 0.2 and "yellow" or "red",
            )
        # Narrator
        self.game.r_int.draw_rectangle((0, 0.9), to=(1, 1), col="black")
        self.game.r_int.draw_text(self.narrate, (0.01, 0.91), to=(0.99, 0.99))
