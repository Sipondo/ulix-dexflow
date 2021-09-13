from .basegamestate import BaseGameState
from ..interface.shopinterface import ShopInterface


class GameStateShop(BaseGameState):
    def on_enter(self, owner):
        self.game.r_int.letterbox = True

        self.time = 0

        self.selection = 0
        self.cd = 0
        self.goto = None
        self.shop = ShopInterface(self.game, owner)
        self.item_amount = None

        self.dialogue = None
        self.author = None
        self.prev_dialogue = None
        self.need_to_redraw = True

        self.spr_textbox = self.game.m_res.get_interface("textbox")

        self.spr_shop_header = self.game.m_res.get_interface("shop_headertile")
        self.spr_shop_descript = self.game.m_res.get_interface("shop_descript")
        self.spr_talker = None

        self.spr_shop_item_background = self.game.m_res.get_interface(
            "shop_item_background_window"
        )
        self.spr_shopwindow = self.game.m_res.get_interface("shopwindow")
        self.spr_itemcell = (
            self.game.m_res.get_interface("shop_itemcell"),
            self.game.m_res.get_interface("shop_itemcell_selected"),
        )
        self.spr_shop_itemtext_cell = self.game.m_res.get_interface(
            "shop_itemtext_cell"
        )
        self.spr_shoplistwindow = self.game.m_res.get_interface("shop_list_window")

    def on_tick(self, time, frame_time):
        self.cd -= time - self.time
        self.time = time
        self.lock = self.game.m_ani.on_tick(time, frame_time)
        self.redraw(time, frame_time)
        return False

    def on_exit(self):
        pass

    def redraw(self, time, frame_time):
        self.game.m_ent.render()
        if self.need_to_redraw or (self.dialogue != self.prev_dialogue):
            self.game.r_int.new_canvas()
            self.draw_interface(time, frame_time)
            self.prev_dialogue = self.dialogue
            self.need_to_redraw = False

    def set_locked(self, bool):
        self.lock = bool

    def event_keypress(self, key, modifiers):
        if self.lock == False:
            self.need_to_redraw = True
            if key == "down":
                if self.item_amount is not None:
                    self.game.r_aud.effect("select")
                    self.item_amount -= 1
                    if self.item_amount < 1:
                        q = self.shop.get_quantity(self.selection)
                        self.item_amount = q or 99
                    return
                self.selection = (self.selection + 1) % self.max_selection
                self.game.r_aud.effect("select")
            elif key == "up":
                if self.item_amount is not None:
                    self.game.r_aud.effect("select")
                    self.item_amount += 1
                    q = self.shop.get_quantity(self.selection)
                    q = q or 99
                    if self.item_amount > q:
                        self.item_amount = 1
                    return
                self.selection = (self.selection - 1) % self.max_selection
                self.game.r_aud.effect("select")
            elif key == "interact":
                if self.item_amount is not None:
                    if self.item_amount < 1:
                        self.game.r_aud.effect("cancel")
                        self.item_amount = None
                    else:
                        self.game.r_aud.effect("buy")
                        self.game.inventory.add_item(
                            self.shop.get_item_data(self.selection).identifier,
                            self.item_amount,
                        )
                        self.item_amount = None
                        self.dialogue = (
                            "Thank you for your purchase! Anything else?"
                        )
                else:
                    self.game.r_aud.effect("select")
                    self.item_amount = 1
                return
            elif key == "backspace" or key == "menu":
                self.game.r_aud.effect("cancel")
                print(self.cd)
                if self.item_amount is not None:
                    self.item_amount = None
                    self.cd = 0.1
                elif self.cd <= 0:
                    self.game.m_gst.switch_state("cinematic")

    @property
    def max_selection(self):
        return len(self.shop.items)

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

        self.game.r_int.draw_image(self.spr_shopwindow, (0.5, 0.45), centre=True)
        self.game.r_int.draw_image(
            self.spr_shop_item_background, (0.3, 0.465), centre=True
        )
        self.game.r_int.draw_image(self.shop.get_item_data(self.selection).icon, (0.3, 0.41), centre=True, size=3.0)
        self.game.r_int.draw_image(self.spr_shop_header, (0.3, 0.275), centre=True)
        self.game.r_int.draw_image(self.spr_shop_descript, (0.3, 0.6), centre=True)
        self.game.r_int.draw_image(
            self.spr_shoplistwindow, (0.55, 0.23), centre=False
        )
        if self.dialogue:
            self.game.r_int.draw_image(
                self.spr_textbox, (0.02, 0.82),
            )
            self.game.r_int.draw_text(
                "How many of this article would you like?"
                if self.item_amount is not None
                else (self.dialogue if self.dialogue is not None else ""),
                (0.025, 0.825),
                to=(0.98, 0.98),
                bcol=None,
            )

        # self.game.r_int.draw_rectangle((0.19, 0.25), size=(0.37, 0.42), col="black")
        self.game.r_int.draw_text(
            f"{self.shop.get_item(self.selection).name}",
            (0.31, 0.285),
            size=(0.14, 0.08),
            bcol=None,
            centre=True,
        )
        self.game.r_int.draw_text(
            f"{self.shop.get_item_data(self.selection).description}",
            (0.3, 0.622),
            size=(0.35, 0.15),
            fsize=10,
            bcol=None,
            centre=True,
        )

        if self.item_amount is not None:
            self.game.r_int.draw_image(
                self.spr_itemcell[1], (0.56, 0.24),
            )
            self.game.r_int.draw_text(
                f"Quantity: {self.item_amount}",
                (0.65, 0.26),
                size=(0.22, 0.06),
                centre=False,
                bcol=None,
            )
        else:

            # TODO add logic for more than 6 items
            for i, item in enumerate(self.shop.items):
                self.game.r_int.draw_image(
                    self.spr_itemcell[1 if self.selection == i else 0],
                    (0.56, 0.24 + 0.08 * i),
                )
                self.game.r_int.draw_text(
                    f"{self.selection == i and '' or ''}{item.price}",
                    (0.57, 0.26 + 0.08 * i),
                    size=(0.10, 0.06),
                    centre=False,
                    bcol=None,
                )
                self.game.r_int.draw_text(
                    f"{self.selection == i and '' or ''}{item.name}",
                    (0.65, 0.26 + 0.08 * i),
                    size=(0.22, 0.06),
                    centre=False,
                    bcol=None,
                )
