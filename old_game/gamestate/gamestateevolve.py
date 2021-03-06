from .basegamestate import BaseGameState


class GameStateEvolve(BaseGameState):
    def on_enter(self):
        self.game.r_int.fade = False
        self.to_evolve = []  # list of members who evolve, evolution target
        self.evolving = False
        self.evolve = False
        for member in self.game.inventory.members:
            evolution_data = member.data["evolutions"]
            if not evolution_data:
                continue
            evd = evolution_data.split(",")
            evolve_target, cond, cond_req = evd[0], evd[1], evd[2]

            if cond == "Level":
                if member.level >= int(cond_req):
                    self.to_evolve.append(
                        (member, self.game.m_pbs.get_fighter_by_name(evolve_target))
                    )

        self.spr_statusbox = "statusbox"
        self.game.r_int.load_sprite(self.spr_statusbox)
        self.game.r_int.init_sprite_drawer()

        self.evo = None
        self.evo_name = None
        self.evo_target = None

        # self.logo_engine = self.game.m_res.get_splash("ulix_logo_small")
        self.small_splash = None
        self.big_splash = None

        self.get_evolutions()

    def on_tick(self, time, frame_time):
        self.time = time

    def get_evolutions(self):
        if not self.evolving:
            if len(self.to_evolve) > 0:
                self.evo, self.evo_target = self.to_evolve.pop()
                self.evo_name = self.evo.name
                self.get_evo_data()
                self.evolving = True
                self.evolve = False
            else:
                self.game.m_gst.switch_state("overworld")

    def get_evo_data(self):
        self.small_splash = self.evo.sprite
        self.big_splash = self.game.m_res.get_sprite_from_anim(
            self.evo_target.id, size=2.0
        )

    def on_exit(self):
        self.game.r_int.fade = False

    def on_render(self, time, frame_time):
        self.game.r_int.draw_rectangle(
            (0, 0), to=(1, 1), col="black",
        )
        self.draw_interface(time, frame_time)

    def event_keypress(self, key, modifiers):
        if key == "interact":
            if self.evolving:
                self.evolve = True
                self.evo.evolve(self.evo_target)
            else:
                self.get_evolutions()
        if key == "backspace":
            self.evolving = False
            self.game.r_int.fade = True

    def draw_interface(self, time, frame_time):
        if self.evolving:
            self.game.r_int.draw_image(
                self.spr_statusbox, (0.0035, 0.9),
            )
            if not self.evolve:
                self.game.r_int.draw_image(self.small_splash, (0.5, 0.5), centre=True)
                self.game.r_int.draw_text(
                    f"{self.evo.name} is evolving!",
                    (0.01, 0.91),
                    to=(0.99, 0.99),
                    bcol=None,
                )
            else:
                self.game.r_int.draw_image(self.big_splash, (0.5, 0.5), centre=True)
                self.game.r_int.draw_text(
                    f"{self.evo_name} has evolved into {self.evo.name}!",
                    (0.01, 0.91),
                    to=(0.99, 0.99),
                    bcol=None,
                )
                self.evolving = False

