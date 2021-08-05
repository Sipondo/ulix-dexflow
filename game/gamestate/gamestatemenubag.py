from .basegamestate import BaseGameState


class GameStateMenuBag(BaseGameState):
    def on_enter(self):
        self.game.r_int.letterbox = False
        self.selection = 0
        self.selection_window = 0
        self.icon_frame = 0
        self.frame_counter = 0

        self.filter = 1

        self.filtericons = [
            self.game.m_res.get_item_icon(f"bagPocket{x}", size=0.5)
            for x in range(1, 9)
        ]

        self.need_to_redraw = True

    def on_tick(self, time, frame_time):
        self.time = time
        # self.lock = self.game.m_ani.on_tick(time, frame_time)
        self.redraw(time, frame_time)
        return False

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
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
                if (self.selection > 7) and (
                    (self.selection_window + 10) < self.max_selection
                ):
                    self.selection_window += 1
                elif self.selection + self.selection_window + 1 >= self.max_selection:
                    self.selection = 0
                    self.selection_window = 0
                else:
                    self.selection += 1
                self.game.r_aud.effect("select")
            elif key == "up":
                if (self.selection < 2) and ((self.selection_window) > 0):
                    self.selection_window -= 1
                elif self.selection + self.selection_window <= 0:
                    self.selection = 9
                    self.selection_window = self.max_selection - 10
                else:
                    self.selection -= 1
                self.game.r_aud.effect("select")

            elif key == "left":
                self.filter = ((self.filter - 2) % 8) + 1
                self.game.r_aud.effect("select")

            elif key == "right":
                self.filter = (self.filter % 8) + 1
                self.game.r_aud.effect("select")

            elif key == "menu" or key == "backspace":
                self.game.m_gst.switch_state("menuparty")
                self.game.r_aud.effect("cancel")

    @property
    def max_selection(self):
        return len(self.game.inventory.get_pocket_items(self.filter))

    def draw_interface(self, time, frame_time):
        """
        Party and Inspect view
        List pokemon and retrieve info via subview
        """
        self.game.r_int.draw_rectangle((0.07, 0.12), to=(0.93, 0.88), col="black")

        items = self.game.inventory.get_pocket_items(self.filter)[
            self.selection_window : self.selection_window + 10
        ]
        for i, item in enumerate(items):

            self.game.r_int.draw_text(
                f"{item.quantity}x",
                (0.55, 0.20 + 0.06 * i),
                size=(0.04, 0.05),
                bcol=self.selection == i and "yellow" or "white",
                align="right",
            )

            self.game.r_int.draw_text(
                f"{item.itemname}",
                (0.63, 0.20 + 0.06 * i),
                size=(0.24, 0.05),
                bcol=self.selection == i and "yellow" or "white",
            )

            self.game.r_int.draw_image(
                item.icon, (0.61, 0.225 + 0.06 * i), centre=True,
            )

        if len(items) > self.selection:
            item = items[self.selection]
            self.game.r_int.draw_text(
                f"{item.description}", (0.34, 0.25), size=(0.20, 0.6), fsize=10,
            )
            self.game.r_int.draw_image(item.icon, (0.25, 0.48), centre=True, size=3.0)
            self.game.r_int.draw_text(
                f"{item.itemname}", (0.25, 0.74), size=(0.14, 0.08), centre=True
            )

