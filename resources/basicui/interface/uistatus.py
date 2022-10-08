from ulivy.interface.baseui import BaseUI, PixelImage
from kivy.lang import Builder
import math
import numpy as np
from kivy.graphics import Color, Rectangle

Builder.load_file("resources/basicui/interface/uistatus.kv")


class UIStatus(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False

        self.rewardsel = 0
        self.max_rewardsel = 6

        self.confirmsel = 1
        self.cancelsel = 1

        self.batsel = 0
        self.max_batsel = len(self.game.inventory.members)

        self.itemsel = 0
        self.max_itemsel = 0

        self.overlay_opacity = 0.0

        self.fighters = {}
        self.stats = {}

        self.state = "BATTLER"
        self.items_ready = False

        with self.canvas:
            Color(0.9, 0, 0)
            self.rec_hp = Rectangle(pos=(100, 265), size=(300, 42))
            Color(0.9, 0.5, 0.1)
            self.rec_atk = Rectangle(pos=(100, 215), size=(300, 42))
            Color(0.9, 0.8, 0)
            self.rec_def = Rectangle(pos=(100, 165), size=(300, 42))
            Color(0.4, 0.6, 1)
            self.rec_satk = Rectangle(pos=(100, 115), size=(300, 42))
            Color(0.4, 0.6, 0.1)
            self.rec_sdef = Rectangle(pos=(100, 65), size=(300, 42))
            Color(0.9, 0.3, 0.4)
            self.rec_spd = Rectangle(pos=(100, 15), size=(300, 42))

        # self.update_page()

    @property
    def max_page(self):
        return len(self.pages)

    def ready_items(self):
        self.max_itemsel = len(self.game.inventory.items)
        for i, x in enumerate(self.game.inventory.items):

            self.ids.ItemInfo.add_widget(
                PixelImage(
                    # id=f"Item{i}box",
                    source=f"resources/basicui/graphics/interface/itembox_{x.data.quality}.png",
                    pos_hint={
                        "center_x": 0.1 + 0.12 * (i % 8),
                        "center_y": 0.7 - 0.12 * (i // 8),
                    },
                )
            )
            self.ids.ItemInfo.add_widget(
                PixelImage(
                    # id=f"Item{i}box",
                    source=f"resources/base/graphics/items/{x.data.identifier.lower()}.png",
                    pos_hint={
                        "center_x": 0.1 + 0.12 * (i % 8),
                        "center_y": 0.7 - 0.12 * (i // 8),
                    },
                )
            )
            # f"resources/base/graphics/items/{self.rewards[0].identifier.lower()}.png"
        self.itemselectbox = PixelImage(
            source="resources/basicui/graphics/interface/itemboxsel.png",
            pos_hint={
                "center_x": 0.1,
                "center_y": 0.7,
            },
        )
        self.ids.ItemInfo.add_widget(self.itemselectbox)

        self.update_page()

    def update(self, time=None, frame_time=None):
        if time is None:
            return

        if not self.items_ready:
            self.items_ready = True
            self.ready_items()

        self.overlay_opacity = min(self.overlay_opacity + frame_time * 6, 1.0)
        self.ids.Overlay.opacity = self.overlay_opacity

        # self.ids.Card.pos_hint = {"center_x": 0.5 + time / 100, "center_y": 0.1}
        return False

    def event_keypress(self, key, modifiers):
        if key == "left":
            if self.state == "BATTLER":
                self.batsel = (self.batsel - 1) % self.max_batsel
            elif self.state == "ITEMPICK":
                self.itemsel = (self.itemsel - 1) % self.max_itemsel
            self.game.r_aud.effect("select")
        elif key == "right":
            if self.state == "BATTLER":
                self.batsel = (self.batsel + 1) % self.max_batsel
            elif self.state == "ITEMPICK":
                self.itemsel = (self.itemsel + 1) % self.max_itemsel
            self.game.r_aud.effect("select")

        elif key == "up":
            if self.state == "BATTLER":
                self.state = "ITEM"
            elif self.state == "ITEM":
                self.state = "BATTLER"
            elif self.state == "ITEMPICK":
                if self.itemsel - 8 > 0:
                    self.itemsel -= 8

            self.game.r_aud.effect("select")

        elif key == "down":
            if self.state == "BATTLER":
                self.state = "ITEM"
                self.game.r_aud.effect("select")
            elif self.state == "ITEM":
                self.state = "BATTLER"
            elif self.state == "ITEMPICK":
                if self.itemsel + 8 < self.max_itemsel:
                    self.itemsel += 8

            self.game.r_aud.effect("select")

        elif key == "interact":
            if self.state == "ITEM":
                self.state = "ITEMPICK"

        elif key == "backspace":
            if self.state == "ITEMPICK":
                self.state = "ITEM"
            else:
                self.game.m_gst.switch_state("overworld")

        self.update_page()

    def update_page(self):

        self.ids.BackgroundMember.source = (
            "resources/basicui/graphics/interface/bg_menucontinue.png"
            if self.state in ("ITEM", "ITEMPICK")
            else "resources/basicui/graphics/interface/bg_menugame.png"
        )

        self.itemselectbox.pos_hint = {
            "center_x": 0.1 + 0.12 * (self.itemsel % 8),
            "center_y": 0.7 - 0.12 * (self.itemsel // 8),
        }

        self.itemselectbox.opacity = 1 if self.state == "ITEMPICK" else 0

        # MoveSelector
        self.ids.MoveSelector.opacity = (
            1 if self.state in ("PICKREWARD", "BATTLER") else 0
        )

        # ConfirmationBox
        self.ids.ConfirmationBox.opacity = (
            1 if self.state in ("ITEM", "ITEMPICK") else 0
        )
        # Items

        self.ids.BattlerInfo.opacity = 1 if self.state == "BATTLER" else 0
        self.ids.ItemInfo.opacity = 1 if self.state in ("ITEM", "ITEMPICK") else 0

        # Pokemonselector
        self.ids.Card.opacity = 1 if self.state in ("BATTLER", "PICKREWARD") else 0
        self.ids.ArrowLeft.opacity = (
            0.6 if self.state in ("BATTLER", "PICKREWARD") else 0
        )
        self.ids.ArrowRight.opacity = (
            0.6 if self.state in ("BATTLER", "PICKREWARD") else 0
        )
        self.ids.Stats.opacity = 1 if self.state in ("BATTLER", "PICKREWARD") else 0
        self.ids.Battler_Type1.opacity = (
            1 if self.state in ("BATTLER", "PICKREWARD") else 0
        )
        self.ids.Battler_Type2.opacity = (
            1 if self.state in ("BATTLER", "PICKREWARD") else 0
        )

        self.ids.Move1.opacity = 1
        self.ids.Move2.opacity = 1
        self.ids.Move3.opacity = 1

        if self.state == "ITEM" or "ITEMPICK":
            self.ids.Name.text = self.game.inventory.items[self.itemsel].data.itemname
            self.ids.DialogueText.text = (
                str(self.game.inventory.items[self.itemsel].data.description)
                + " x"
                + str(self.game.inventory.items[self.itemsel].quantity)
            )

        if self.state == "BATTLER":
            self.ids.BackgroundMember.source = (
                "resources/basicui/graphics/interface/bg_menumovebattler.png"
            )
            member = self.game.inventory.members[self.batsel]

            self.ids.Name.text = member.name
            self.ids.MenuName.text = "Status"
            self.ids.Card.source = f"""resources/simple/graphics/cards/{member.name.lower().replace("'", "")}.png"""
            self.ids.Move1_Base.opacity = 1

            # Clear

            # ClearDone

            f = member
            self.ids.Battler_Type1.source = (
                f"resources/basicui/graphics/interface/types/{f.type1.lower()}.png"
            )
            if f.type2:
                self.ids.Battler_Type2.source = (
                    f"resources/basicui/graphics/interface/types/{f.type2.lower()}.png"
                )
            else:
                self.ids.Battler_Type2.opacity = 0

            stats = member.stats
            stats = stats / np.sum(stats)
            self.rec_hp.size = (650 * stats[0], 42)
            self.rec_atk.size = (650 * stats[1], 42)
            self.rec_def.size = (650 * stats[2], 42)
            self.rec_satk.size = (650 * stats[3], 42)
            self.rec_sdef.size = (650 * stats[4], 42)
            self.rec_spd.size = (650 * stats[5], 42)

            base = member.actions[0]
            self.ids.Move1_Prefix.text = base.prefix
            self.ids.Move1_Name.text = base.name
            self.ids.Move1_Description.text = f"{base.description} {base.suffix}"
            self.ids.Move1_Type.source = f"resources/basicui/graphics/interface/types/{str(base.type).lower()}.png"
            self.ids.Move1_Category.source = f"resources/basicui/graphics/interface/types/{str(base.damagecat).lower()}.png"
            self.ids.Move1_Border.source = f"resources/basicui/graphics/interface/moveborder_{str(base.quality)}.png"
            self.ids.Move1_PP.text = "-" if int(base.pp) > 40 else str(base.pp)

            if len(member.actions) < 2:
                self.battler_clear()
                return

            base = member.actions[1]
            self.ids.Move2_Prefix.text = base.prefix
            self.ids.Move2_Name.text = base.name
            self.ids.Move2_Description.text = f"{base.description} {base.suffix}"
            self.ids.Move2_Type.source = f"resources/basicui/graphics/interface/types/{str(base.type).lower()}.png"
            self.ids.Move2_Category.source = f"resources/basicui/graphics/interface/types/{str(base.damagecat).lower()}.png"
            self.ids.Move2_Border.source = f"resources/basicui/graphics/interface/moveborder_{str(base.quality)}.png"
            self.ids.Move2_PP.text = "-" if int(base.pp) > 40 else str(base.pp)

            if len(member.actions) < 3:
                self.battler_clear(both=False)
                return

            base = member.actions[2]
            self.ids.Move3_Prefix.text = base.prefix
            self.ids.Move3_Name.text = base.name
            self.ids.Move3_Description.text = f"{base.description} {base.suffix}"
            self.ids.Move3_Type.source = f"resources/basicui/graphics/interface/types/{str(base.type).lower()}.png"
            self.ids.Move3_Category.source = f"resources/basicui/graphics/interface/types/{str(base.damagecat).lower()}.png"
            self.ids.Move3_Border.source = f"resources/basicui/graphics/interface/moveborder_{str(base.quality)}.png"
            self.ids.Move3_PP.text = "-" if int(base.pp) > 40 else str(base.pp)
        else:
            self.rec_hp.size = (0, 42)
            self.rec_atk.size = (0, 42)
            self.rec_def.size = (0, 42)
            self.rec_satk.size = (0, 42)
            self.rec_sdef.size = (0, 42)
            self.rec_spd.size = (0, 42)

    def battler_clear(self, both=True):
        if both:
            self.ids.Move2.opacity = 0
            self.ids.Move2_Prefix.text = ""
            self.ids.Move2_Name.text = ""
            self.ids.Move2_Description.text = ""
            # self.ids.Move2_Type.source = "resources/basicui/graphics/interface/gamebounds.png"
            # self.ids.Move2_Category.source = "resources/basicui/graphics/interface/gamebounds.png"
            # self.ids.Move2_Border.source = "resources/basicui/graphics/interface/moveborder.png"
            self.ids.Move2_PP.text = ""

        self.ids.Move3.opacity = 0
        self.ids.Move3_Prefix.text = ""
        self.ids.Move3_Name.text = ""
        self.ids.Move3_Description.text = ""
        # self.ids.Move3_Type.source = "resources/basicui/graphics/interface/gamebounds.png"
        # self.ids.Move3_Category.source = "resources/basicui/graphics/interface/gamebounds.png"
        # self.ids.Move3_Border.source = "resources/basicui/graphics/interface/moveborder.png"
        self.ids.Move3_PP.text = ""
