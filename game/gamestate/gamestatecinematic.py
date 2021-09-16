from .basegamestate import BaseGameState


class GameStateCinematic(BaseGameState):
    def on_enter(self):
        self.game.r_int.letterbox = True

        self.selection = 0
        self.options = []

        self.dialogue = None
        self.author = None
        self.prev_dialogue = None
        self.need_to_redraw = True

        self.spr_talker = None

        self.spr_textbox = self.game.m_res.get_interface("textbox")
        self.spr_namebox = self.game.m_res.get_interface("namebox")

    def on_tick(self, time, frame_time):
        self.time = time
        self.lock = self.game.m_ani.on_tick(time, frame_time)
        # self.redraw(time, frame_time)
        return False

    def on_exit(self):
        pass

    def on_render(self, time, frame_time):
        self.game.m_ent.render()
        if self.need_to_redraw or (self.dialogue != self.prev_dialogue) or True:
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.prev_dialogue = self.dialogue
            # self.need_to_redraw = False

    def set_locked(self, bool):
        self.lock = bool

    def event_keypress(self, key, modifiers):
        if self.lock == False:
            self.need_to_redraw = True
            if key == "down":
                if self.options:
                    self.selection = (self.selection + 1) % self.max_selection
                    self.game.r_aud.effect("select")
            elif key == "up":
                if self.options:
                    self.selection = (self.selection - 1) % self.max_selection
                    self.game.r_aud.effect("select")
            elif key == "interact":
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

        if self.spr_talker:
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
