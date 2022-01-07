from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.graphics import RenderContext, BindTexture, Rectangle, Color, Line
from kivy.graphics.texture import Texture
from kivy.core.image import Image, ImageData
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.core.window import Window
from kivy.resources import resource_find, resource_add_path, resource_remove_path
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

import os
import numpy as np
import lark
import termcolor

from mapmanager import MapManager


from osc.JoystickDemo import JoystickDemo

# with open(resource_find("ulivy_shaders/basic_tile.glsl")) as file:
#     shader = file.read()

with open(resource_find("ulivy_shaders/basic_tile_fs.glsl")) as file:
    shader_fs = file.read()

with open(resource_find("ulivy_shaders/basic_tile_vs.glsl")) as file:
    shader_vs = file.read()

VIEW_WIDTH = 8


class FPSCounter(AnchorLayout):
    # property to set the source code for fragment shader
    counter = NumericProperty()
    age = NumericProperty()

    def __init__(self, **kwargs):
        super(FPSCounter, self).__init__(anchor_x="left", anchor_y="top")
        Clock.schedule_interval(self.update_counter, 0)
        Clock.schedule_interval(self.update_label, 1 / 4)

    def update_counter(self, dt):
        self.counter += 1
        self.age += dt

    def update_label(self, dt):
        if self.age > 0.6:
            self.age = self.age / 2
            self.counter = self.counter / 2
        self.clear_widgets()
        self.add_widget(
            Label(
                text=f"[color=3333dd]{(self.counter+self.age) // self.age:.0f}[/color]",
                size=(50, 15),
                size_hint=(None, None),
                markup=True,
            )
        )


class TileLayerWidget(FloatLayout):
    # property to set the source code for fragment shader
    fs = StringProperty(None)
    vs = StringProperty(None)

    def __init__(self, tiles, texture_file, **kwargs):
        # Instead of using Canvas, we will use a RenderContext,
        # and change the default shader used.
        self.canvas = RenderContext()

        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(TileLayerWidget, self).__init__(**kwargs)

        print(f"{texture_file}.png")
        self.tex1 = Image.load(resource_find(f"{texture_file}.png")).texture

        self.tex1.mag_filter = "nearest"

        self.canvas["texture0"] = 0
        self.canvas["texture1"] = 1

        self.rec1 = Rectangle(size=Window.size, texture=self.tex1)
        self.canvas.add(self.rec1)

        self.temp_map = tiles

        blittex = Texture.create(size=self.temp_map.shape[:2])

        buf = self.temp_map.flatten().tobytes()
        blittex.blit_buffer(buf, colorfmt="rgba", bufferfmt="ubyte")
        blittex.mag_filter = "nearest"

        self.blittex = blittex
        self.canvas.add(BindTexture(texture=blittex, index=1))

        self.camera_position = 0

        self.float_x = 0
        self.float_y = 0
        self.t = 0
        # We'll update our glsl variables in a clock
        Clock.schedule_interval(self.update_glsl, 0)  # 1 / 60.0)

    def on_fs(self, instance, value):
        # set the fragment shader to our source code
        shader = self.canvas.shader
        old_value = shader.fs
        shader.fs = value
        if not shader.success:
            shader.fs = old_value
            raise Exception("failed")

    def on_vs(self, instance, value):
        # set the vertex shader to our source code
        pass
        # shader = self.canvas.shader
        # old_value = shader.vs
        # shader.vs = value
        # if not shader.success:
        #     shader.vs = old_value
        #     raise Exception("failed")

    def update_glsl(self, dt):
        self.t += dt

        orig_w, orig_h = Window.size
        w = min(orig_h // 9 * 16, orig_w)
        h = min(w // 16 * 9, orig_h)

        self.rec1.pos = ((orig_w - w) / 2, (orig_h - h) / 2)
        self.rec1.size = (w, h)

        texture_size = (
            self.tex1.size[0] / 16 * 1.004,
            self.tex1.size[1] / 16 * 1.004,
        )

        self.float_x += self.parent.parent.joysticks.val_x
        self.float_y += self.parent.parent.joysticks.val_y

        self.camera_position = (
            self.float_x / 100,
            self.float_y / 100,
        )

        # viewport = (Window.size[0] / 32, Window.size[1] / 32)

        viewport = (float(21), float(12))
        # viewport = (float(38), float(16))

        # Invert for modulo
        viewport = (float(1 / viewport[0]), float(1 / viewport[1]))

        self.canvas["viewport"] = viewport
        self.canvas["time"] = Clock.get_boottime()
        self.canvas["resolution"] = list(map(float, self.size))
        self.canvas["texture_size"] = texture_size
        self.canvas["map_size"] = list(map(float, self.temp_map.shape[:2]))
        self.canvas["camera_position"] = self.camera_position
        # This is needed for the default vertex shader.
        win_rc = Window.render_context
        self.canvas["projection_mat"] = win_rc["projection_mat"]
        self.canvas["modelview_mat"] = win_rc["modelview_mat"]
        self.canvas["frag_modelview_mat"] = win_rc["frag_modelview_mat"]


class TileRenderer(Screen):
    def __init__(self, **kwargs):
        super(TileRenderer, self).__init__(**kwargs)
        self.size = Window.size
        # self.add_widget(TileLayerWidget(fs=shader, height=7))

        self.m_map = MapManager()
        self.m_map.load_world_data()

        pth = os.path.join("resources", "essentials", "graphics", "tilesets")
        resource_add_path(pth)
        pth = os.path.join("resources", "essentials", "graphics", "autotiles")
        resource_add_path(pth)
        pth = os.path.join("resources", "essentials", "graphics", "autocliffs")
        resource_add_path(pth)

        for h, mapdef in enumerate(self.m_map.current_tilesets):
            if mapdef[0] != "TILES":
                continue
            ltype, level, tiles, collision = mapdef

            if "collision" in level:
                continue
            if "cliff" in level:
                continue

            # if "water" not in level:
            #     continue

            tiles = tiles.copy()

            # l = self.spawn_tile_layer(h, tiles, level, offset=offset, fade=fade)
            for tile in tiles:
                temp_map = np.pad(
                    tile.copy(),
                    [(0, 0), (0, 0), (0, 2)],
                    mode="constant",
                    constant_values=0,
                ).astype(np.ubyte)

                level = level.split("/")[-1]

                print("LAYER!", h, level, tiles.shape, "->", temp_map.shape)
                self.add_widget(
                    TileLayerWidget(
                        fs=shader_fs, vs=shader_vs, tiles=temp_map, texture_file=level
                    )
                )


class Overlay2Layouts(Screen):
    def __init__(self, **kwargs):
        super(Overlay2Layouts, self).__init__(**kwargs)
        self.size = Window.size
        self.add_widget(TileRenderer())

        self.joysticks = JoystickDemo()
        self.add_widget(self.joysticks)
        self.add_widget(FPSCounter())


class UlivyApp(App):
    def build(self):
        return Overlay2Layouts()


if __name__ == "__main__":
    UlivyApp().run()
