from .basegamestate import BaseGameState


class GameStateMenuBag(BaseGameState):
    def on_enter(self):
        self.game.r_int.letterbox = False
        self.selection = 0
        self.selection_window = 0
        self.icon_frame = 0
        self.frame_counter = 0

        self.filter = 1

        self.spr_inventory_tabs = tuple(
            [f"inventory_tab{x}" for x in (1, 2, 3, 4, 5, 6, 7, 8)]
        )
        self.spr_inventorywindow = "inventory_window"

        self.spr_cell = (
            "inventory_itemcell",
            "inventory_itemcell_selected",
        )

        self.spr_shop_header = "shop_headertile"
        self.spr_shop_descript = "shop_descript"
        self.spr_partyback = "partyback"
        self.spr_shop_item_background = "shop_item_background_window"

        for x in (
            self.spr_inventory_tabs
            + (self.spr_inventorywindow,)
            + self.spr_cell
            + (self.spr_shop_header,)
            + (self.spr_shop_descript,)
            + (self.spr_partyback,)
            + (self.spr_shop_item_background,)
        ):
            self.game.r_int.load_sprite(x)

        self.game.r_int.init_sprite_drawer()

    def on_tick(self, time, frame_time):
        self.game.m_ent.render()
        return

    def on_exit(self):
        pass

    def on_render(self, time, frame_time):
        self.draw_interface(time, frame_time)

    def set_locked(self, bool):
        self.lock = bool

    def event_keypress(self, key, modifiers):
        if self.lock == False:
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
        self.game.r_int.draw_image(self.spr_partyback, (0.5, 0.5), centre=True)

        items = self.game.inventory.get_pocket_items(self.filter)[
            self.selection_window : self.selection_window + 10
        ]

        self.game.r_int.draw_image(self.spr_inventorywindow, (0.55, 0.23), centre=False)
        self.game.r_int.draw_image(
            self.spr_inventory_tabs[self.filter - 1], (0.55, 0.199), centre=False
        )
        for i, item in enumerate(items):
            self.game.r_int.draw_image(
                self.spr_cell[1 if self.selection == i else 0], (0.56, 0.24 + 0.08 * i)
            )

            self.game.r_int.draw_text(
                f"{item.quantity}x",
                (0.57, 0.26 + 0.08 * i),
                size=(0.04, 0.05),
                bcol=False,
                align="right",
            )

            self.game.r_int.draw_text(
                f"{item.itemname}",
                (0.65, 0.26 + 0.08 * i),
                size=(0.24, 0.05),
                bcol=False,
            )

            self.game.r_int.draw_image(
                item.icon, (0.62, 0.28 + 0.08 * i), centre=True, safe=True
            )

        if len(items) > self.selection:
            item = items[self.selection]
            self.game.r_int.draw_image(
                self.spr_shop_item_background, (0.3, 0.465), centre=True
            )
            self.game.r_int.draw_image(item.icon, (0.3, 0.41), centre=True, size=3.0)
            self.game.r_int.draw_image(self.spr_shop_header, (0.3, 0.275), centre=True)
            self.game.r_int.draw_image(self.spr_shop_descript, (0.3, 0.6), centre=True)
            self.game.r_int.draw_text(
                f"{item.itemname}",
                (0.31, 0.21),
                size=(0.14, 0.08),
                bcol=None,
                centre=True,
            )
            self.game.r_int.draw_text(
                f"{item.description}",
                (0.31, 0.48),
                size=(0.35, 0.15),
                fsize=10,
                bcol=None,
                centre=True,
            )
