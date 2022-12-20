from math import cos, pi, sin
from ulivy.interface.baseui import BaseUI, PixelImage
from kivy.lang import Builder
import math

Builder.load_file("resources/armourui/interface/uimenustart.kv")

OPTIONS = [
    "charizard",
    "tyranitar",
    "stunfisk",
    "swanna",
    "venusaur",
    "volcarona",
    "hydreigon",
    "cubchoo",
    "garchomp",
    "gengar",
    "gardevoir",
    "togetic",
    "lucario",
    "grovyle",
    "mawile",
    "farfetch'd",
    "pikachu",
    "resume",
]


class UIMenuStart(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.overlay_opacity = 1.0
        self.game.r_aud.play_music("bgm/title.ogg", loop=False)

        self.winlist = self.game.m_sav.load("winlist")
        self.stars = []

        for i in range(18):
            p = PixelImage(
                # id=f"Item{i}box",
                source="resources/base/graphics/items/starpiece.png",
                pos_hint={"center_x": 0, "center_y": 0,},
            )
            if OPTIONS[i] in self.winlist:
                p.opacity = 1.0
            else:
                p.opacity = 0.2

            self.add_widget(p)
            self.stars.append(p)

        self.add_widget(
            p := PixelImage(
                # id="Logo",
                source="resources/armourui/graphics/interface/newlogo.png",
                allow_stretch=True,
                size_hint=(1.2, 1.2),
                pos_hint={"center_x": 0.5},
            )
        )
        self.ids["Logo"] = p
        self.update(time=0.5)

    def update(self, time=None, frame_time=None):
        if time is None:
            time = 0.5

        if self.overlay_opacity < 1.0:
            self.overlay_opacity -= frame_time * 2

            if self.overlay_opacity < 0.0:
                self.game.m_ent.player.set_position(15, 15)
                self.game.m_map.set_level(1000)
                self.game.r_fbo.r_til.set_map_via_manager(
                    (0, 0,), fade=False,
                )
                self.game.m_gst.switch_state("overworld", fade=False)
                return

            self.ids.Overlay.opacity = self.overlay_opacity
            self.ids.Logo.opacity = self.overlay_opacity

            for p in self.stars:
                p.opacity = min(p.opacity, self.overlay_opacity)

            self.ids.Background.opacity = 0.9 * (
                (max(self.overlay_opacity, 0.5) - 0.5) * 2
            )

        for i in range(18):
            p = self.stars[i]
            p.pos_hint = {
                "center_x": 0.5 + float(0.9 * 0.27 * sin(2 * pi * i / 18 + time / 4)),
                "center_y": 0.5 + float(0.9 * 0.48 * cos(2 * pi * i / 18 + time / 4)),
            }

        self.ids.Background.center_x = math.sin(time / 2) * 300
        self.ids.Background.center_y = math.cos(time / 2) * 300

        self.ids.Logo.y = math.sin(time / 1.2) * 30 - 70
        time += 0.1
        # self.ids.Subtitle.y = math.sin(time / 1.2) * 30 - 30
        # time += 0.1
        # self.ids.Title.y = math.sin(time / 1.2) * 30 - 50
        return False

    def event_keypress(self, key, modifiers):
        if key == "interact" and self.overlay_opacity > 0.99:
            self.overlay_opacity = 0.99
