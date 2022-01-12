from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import RenderContext, BindTexture, Rectangle
from kivy.graphics.texture import Texture
from kivy.core.image import Image
from kivy.properties import StringProperty
from kivy.resources import resource_find, resource_add_path
from kivy.uix.screenmanager import Screen

import os
import numpy as np

with open(resource_find("ulivy_shaders/basic_tile_fs.glsl")) as file:
    shader_fs = file.read()

with open(resource_find("ulivy_shaders/basic_tile_vs.glsl")) as file:
    shader_vs = file.read()


class TileLayerWidget(FloatLayout):
    # property to set the source code for fragment shader
    fs = StringProperty(None)
    vs = StringProperty(None)

    def __init__(self, tiles, texture_file, level, h, **kwargs):
        # Instead of using Canvas, we will use a RenderContext,
        # and change the default shader used.
        self.canvas = RenderContext()

        self.level = level
        self.h = h
        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(TileLayerWidget, self).__init__(**kwargs)

        print(f"{texture_file}")
        self.texture_file = texture_file
        self.tex1 = texture_file.texture
        self.tex1.mag_filter = "nearest"

        self.canvas["texture0"] = 1
        self.canvas["texture1"] = 2

        self.rec1 = Rectangle(size=Window.size)#, texture=self.tex1)
        self.canvas.add(self.rec1)

        self.tiles = tiles

        self.blittex = Texture.create(size=self.tiles.shape[:2])
        if True:#"water" in self.level:
            print(self.level, texture_file)
            # self.blittex.blit_buffer(self.buf, colorfmt="rgba", bufferfmt="ubyte")
            self.blittex.add_reload_observer(self.populate_texture)
            self.populate_texture(self.blittex)

        self.blittex.mag_filter = "nearest"

        self.canvas.add(BindTexture(texture=self.tex1, index=1))
        self.canvas.add(BindTexture(texture=self.blittex, index=2))

        self.camera_position = 0

        self.float_x = 55.0
        self.float_y = 55.0
        self.t = 0
        # We'll update our glsl variables in a clock
        Clock.schedule_interval(self.update_glsl, 0)  # 1 / 60.0)

    def populate_texture(self, texture):
        self.buf = self.tiles.flatten().tobytes()
        self.blittex.blit_buffer(self.buf, colorfmt="rgba", bufferfmt="ubyte")

        orig_w, orig_h = Window.size
        w = min(orig_h // 9 * 16, orig_w)
        h = min(w // 16 * 9, orig_h)

        self.rec1.pos = ((orig_w - w) / 2, (orig_h - h) / 2)
        self.rec1.size = (w, h)

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
        self.canvas["map_size"] = list(map(float, self.tiles.shape[:2]))
        self.canvas["camera_position"] = self.camera_position
        # This is needed for the default vertex shader.
        win_rc = Window.render_context
        self.canvas["projection_mat"] = win_rc["projection_mat"]
        self.canvas["modelview_mat"] = win_rc["modelview_mat"]
        self.canvas["frag_modelview_mat"] = win_rc["frag_modelview_mat"]


class TileRenderer(Screen):
    def __init__(self, game, **kwargs):
        super(TileRenderer, self).__init__(**kwargs)
        self.size = Window.size
        # self.add_widget(TileLayerWidget(fs=shader, height=7))

        self.m_map = game.m_map
        self.m_map.load_world_data()

        pth = os.path.join("resources", "essentials", "graphics", "tilesets")
        resource_add_path(pth)
        pth = os.path.join("resources", "essentials", "graphics", "autotiles")
        resource_add_path(pth)
        pth = os.path.join("resources", "essentials", "graphics", "autocliffs")
        resource_add_path(pth)

        texmap = {}
        for h, mapdef in enumerate(self.m_map.current_tilesets):
            if mapdef[0] != "TILES":
                continue
            
            
            ltype, level, tiles, collision = mapdef
            level = level.split("/")[-1]
            
            if "collision" in level:
                continue
            if "cliff" in level:
                continue

            if level not in texmap:
                texmap[level] = Image(resource_find(f"{level}.png"))
                # texmap[level].reload()


        for h, mapdef in enumerate(self.m_map.current_tilesets):
            if mapdef[0] != "TILES":
                continue
            
            # if h not in (1, 3, 4):
            #     continue
            ltype, level, tiles, collision = mapdef

            if "collision" in level:
                continue
            if "cliff" in level:
                continue

            # if "brick" not in level:
            #     continue

            # if "water" in level:
            #     continue

            tiles = tiles.copy()
            # if not np.amax(tiles):
            #     continue

            for tile in tiles:
                temp_map = np.pad(
                    tile,
                    [(0, 0), (0, 0), (0, 2)],
                    mode="constant",
                    constant_values=0,
                ).astype(np.ubyte) # < --- broken

                level = level.split("/")[-1]
                
                print("LAYER!", h, level, tiles.shape, "->", temp_map.shape)
                self.add_widget(
                    TileLayerWidget(
                        fs=shader_fs, vs=shader_vs, tiles=temp_map, texture_file=texmap[level], level=level, h=h
                    )
                )
