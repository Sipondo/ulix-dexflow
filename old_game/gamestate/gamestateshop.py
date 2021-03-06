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
        self.top_item = 0
        self.item_amount = None

        self.dialogue = None
        self.prev_dialogue = None
        self.need_to_redraw = True

        self.spr_textbox = "textbox"

        self.spr_shop_header = "shop_headertile"
        self.spr_shop_descript = "shop_descript"

        self.spr_shop_item_background = "shop_item_background_window"
        self.spr_shopwindow = "shopwindow_e"
        self.spr_itemcell = "shop_itemcell"
        self.spr_itemcell_selected = "shop_itemcell_selected"
        self.spr_shop_itemtext_cell = "shop_itemtext_cell"
        self.spr_shoplistwindow = "shop_list_window"

        for spr in (
            self.spr_textbox,
            self.spr_shop_header,
            self.spr_shop_descript,
            self.spr_shop_item_background,
            self.spr_shopwindow,
            self.spr_itemcell,
            self.spr_itemcell_selected,
            self.spr_shop_itemtext_cell,
            self.spr_shoplistwindow,
        ):
            self.game.r_int.load_sprite(spr)

        if self.shop.size == 0:
            self.dialogue = (
                "It seems you bought everything! Sorry, come back another time!"
            )
        self.game.r_int.init_sprite_drawer()

    def on_tick(self, time, frame_time):
        self.cd -= time - self.time
        self.time = time
        self.lock = self.game.m_ani.on_tick(time, frame_time)
        return False

    def on_exit(self):
        self.game.m_sav.save("money", self.game.inventory.money)
        self.shop.save_items()
        pass

    def on_render(self, time, frame_time):
        self.game.m_ent.render()
        self.draw_interface(time, frame_time)
        self.prev_dialogue = self.dialogue

    def set_locked(self, b):
        self.lock = b

    def event_keypress(self, key, modifiers):
        if self.cd > 0:
            return
        self.cd = 0.1
        if self.lock == False:
            self.need_to_redraw = True
            if key == "down":
                if self.shop.size > 0:
                    if self.item_amount is not None:
                        self.game.r_aud.effect("select")
                        self.item_amount -= 1
                        if self.item_amount < 1:
                            q = self.shop.get_quantity(self.selection)
                            self.item_amount = q or 99
                        return
                    self.selection = (self.selection + 1) % self.max_selection
                    self.top_item = max(self.selection - 6, 0)
                    self.game.r_aud.effect("select")
            elif key == "up":
                if self.shop.size > 0:
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
                if self.shop.size == 0:
                    self.game.m_gst.switch_state("cinematic")
                    return
                if self.item_amount is not None:
                    self.game.r_aud.effect("buy")
                    if self.shop.buy_item(self.selection, self.item_amount):
                        self.item_amount = None
                        self.dialogue = "Thank you for your purchase! Anything else?"
                        self.selection = 0
                        return
                    self.dialogue = "Uh-oh, you don't seem to have enough money!"
                    self.item_amount = None
                    return
                self.game.r_aud.effect("select")
                self.item_amount = 1
                return
            elif key == "backspace" or key == "menu":
                self.game.r_aud.effect("cancel")
                if self.item_amount is not None:
                    self.item_amount = None
                    return
                self.game.m_gst.switch_state("cinematic")

    @property
    def max_selection(self):
        return self.shop.size

    def draw_interface(self, time, frame_time):
        if self.dialogue:
            self.dialogue = (
                self.dialogue.replace("{player.name}", self.game.m_ent.player.name)
                .replace("{player.he}", self.game.m_ent.player.he)
                .replace("{player.his}", self.game.m_ent.player.his)
                .replace("{player.che}", self.game.m_ent.player.che)
                .replace("{player.chis}", self.game.m_ent.player.chis)
            )

        self.game.r_int.draw_image("shopwindow_e", (0.5, 0.44), centre=True)
        self.game.r_int.draw_image(
            "shop_item_background_window", (0.3, 0.465), centre=True
        )

        self.game.r_int.draw_image(
            "shop_headertile", (0.3, 0.18), centre=True
        )
        self.game.r_int.draw_image(
            "shop_headertile", (0.3, 0.275), centre=True
        )
        self.game.r_int.draw_image("shop_descript", (0.3, 0.6), centre=True)
        self.game.r_int.draw_image(
            "shop_list_window", (0.55, 0.23), centre=False
        )
        if self.dialogue:
            self.game.r_int.draw_image("textbox", (0.02, 0.82))
            self.game.r_int.draw_text(
                "How many of this article would you like?"
                if self.item_amount is not None
                else (self.dialogue if self.dialogue is not None else ""),
                (0.025, 0.825),
                to=(0.98, 0.98),
                bcol=None,
            )
        self.game.r_int.draw_text(
            f"Money: {self.game.inventory.money}",
            (0.27, 0.11),
            size=(0.14, 0.08),
            bcol=None,
            centre=True,
        )
        # self.game.r_int.draw_rectangle((0.19, 0.25), size=(0.37, 0.42), col="black")
        if self.shop.size == 0:
            return

        self.game.r_int.draw_image(
            self.shop.get_item_data(self.selection).icon,
            (0.3, 0.41),
            centre=True,
            size=3.0,
            safe=True
        )
        self.game.r_int.draw_text(
            f"{self.shop.get_item(self.selection).name}",
            (0.27, 0.21),
            size=(0.14, 0.08),
            bcol=None,
            centre=True,
        )
        self.game.r_int.draw_text(
            f"{self.shop.get_item_data(self.selection).description}",
            (0.3, 0.47),
            size=(0.35, 0.15),
            fsize=10,
            bcol=None,
            centre=True,
        )

        if self.item_amount is not None:
            self.game.r_int.draw_image(
                "shop_itemcell_selected", (0.56, 0.24)
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
                    "shop_itemcell_selected"
                    if self.selection == i
                    else "shop_itemcell",
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
                if self.shop.get_quantity(i) is not None:
                    self.game.r_int.draw_text(
                        f"x{self.shop.get_quantity(i)}",
                        (0.8, 0.26 + 0.08 * i),
                        size=(0.05, 0.06),
                        centre=False,
                        bcol=None,
                    )
