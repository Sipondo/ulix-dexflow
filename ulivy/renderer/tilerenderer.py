from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Mesh, RenderContext, BindTexture, Rectangle
from kivy.graphics.texture import Texture
from kivy.core.image import Image
from kivy.resources import resource_find, resource_add_path
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    ObjectProperty,
    NumericProperty,
    ReferenceListProperty,
    ListProperty,
)

import os
import numpy as np


############## TODO: move this to some resource manager thing

with open(resource_find("ulivy_shaders/basic_tile_fs.glsl")) as file:
    tile_shader_fs = file.read()

with open(resource_find("ulivy_shaders/basic_tile_vs.glsl")) as file:
    tile_shader_vs = file.read()

with open(resource_find("ulivy_shaders/basic_entity_fs.glsl")) as file:
    enti_shader_fs = file.read()

with open(resource_find("ulivy_shaders/basic_entity_gs.glsl")) as file:
    enti_shader_gs = file.read()

with open(resource_find("ulivy_shaders/basic_entity_vs.glsl")) as file:
    enti_shader_vs = file.read()

#####################


class EntityLayerWidget(FloatLayout):
    def __init__(self, game, h, offset, **kwargs):
        self.game = game
        self.canvas = RenderContext(
            fs=enti_shader_fs, gs=enti_shader_gs, vs=enti_shader_vs
        )

        self.h = h
        self.offset = (float(offset[0]) / 21, float(offset[1]) / 12)
        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(EntityLayerWidget, self).__init__(**kwargs)

        self.camera_position = 0

        self.float_x = 0
        self.float_y = 0

        with self.canvas:
            self.mesh = Mesh(
                vertices=[],
                indices=[],
                fmt=[
                    (b"aPos", 2, "float"),
                    (b"aSize", 2, "float"),
                    (b"aTexPos", 2, "float"),  # TODO: should be int
                    (b"aTexSize", 2, "float"),
                    (b"aTexFrame", 2, "float"),
                ],
            )

        self.canvas["texture0"] = 3
        self.canvas.add(
            BindTexture(texture=self.game.atlas.original_textures[0], index=3,)
        )

    def update(self, time, dt):
        self.canvas["texture0"] = 3
        self.game_position = (
            self.size[0] / Window.size[0],
            self.size[1] / Window.size[1],
        )

        vertices, indices = self.parent.parent.parent.parent.m_ent.vertices()

        self.mesh.vertices = vertices
        self.mesh.indices = indices

        self.camera_position = (
            self.game.m_pan.total_x / 21,
            self.game.m_pan.total_y / 12,
        )

        viewport = (float(21), float(12))

        # Invert for modulo
        viewport = (float(1 / viewport[0]), float(1 / viewport[1]))

        self.canvas["viewport"] = viewport

        self.canvas["camera_position"] = self.camera_position
        self.canvas["game_position"] = self.game_position
        self.canvas["offset"] = self.offset


class TileLayerWidget(FloatLayout):
    def __init__(self, game, tiles, texture_file, level, h, offset, **kwargs):
        self.game = game
        self.canvas = RenderContext(fs=tile_shader_fs, vs=tile_shader_vs)

        self.level = level
        self.h = h
        self.offset = (float(offset[0]) / 21, float(offset[1]) / 12)
        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(TileLayerWidget, self).__init__(**kwargs)

        self.texture_file = texture_file
        self.tex1 = texture_file.texture
        self.tex1.mag_filter = "nearest"

        self.canvas["texture0"] = 1
        self.canvas["texture1"] = 2

        self.rec1 = Rectangle(size=self.size, pos=self.pos)
        self.canvas.add(self.rec1)

        self.tiles = tiles

        self.blittex = Texture.create(size=self.tiles.shape[:2])
        self.blittex.add_reload_observer(self.populate_texture)
        self.populate_texture(self.blittex)

        self.blittex.mag_filter = "nearest"

        self.canvas.add(BindTexture(texture=self.tex1, index=1))
        self.canvas.add(BindTexture(texture=self.blittex, index=2))

        self.camera_position = 0

    def populate_texture(self, texture):
        self.buf = self.tiles.flatten().tobytes()
        self.blittex.blit_buffer(self.buf, colorfmt="rgba", bufferfmt="ubyte")

    def update(self, time, dt):
        self.rec1.pos = self.pos
        self.rec1.size = self.size

        self.camera_position = (
            self.game.m_pan.total_x / 21,
            self.game.m_pan.total_y / 12,
        )

        viewport = (float(21), float(12))

        # Invert for modulo
        viewport = (float(1 / viewport[0]), float(1 / viewport[1]))

        self.canvas["viewport"] = viewport

        self.canvas["camera_position"] = self.camera_position
        self.canvas["offset"] = self.offset
        # This is needed for the default vertex shader.
        win_rc = Window.render_context
        self.canvas["projection_mat"] = win_rc["projection_mat"]
        self.canvas["modelview_mat"] = win_rc["modelview_mat"]
        self.canvas["frag_modelview_mat"] = win_rc["frag_modelview_mat"]


class Background(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)


class Bounds(AnchorLayout):
    pass


class TileRenderer(FloatLayout):
    def __init__(self, game, **kwargs):
        super(TileRenderer, self).__init__(**kwargs)

        self.game = game

        self.gamecanvas = getattr(self.ids, "GameCanvas")

        self.size = Window.size
        # self.add_widget(TileLayerWidget(fs=shader, height=7))

        self.m_map = game.m_map
        self.m_map.load_world_data()
        self.layers = []

        pth = os.path.join("resources", "essentials", "graphics", "tilesets")
        resource_add_path(pth)
        pth = os.path.join("resources", "essentials", "graphics", "autotiles")
        resource_add_path(pth)
        pth = os.path.join("resources", "essentials", "graphics", "autocliffs")
        resource_add_path(pth)

        self.texmap = {}

        for h, mapdef in enumerate(self.m_map.current_tilesets):
            if mapdef[0] != "TILES":
                continue

            ltype, level, tiles, collision = mapdef
            level = level.split("/")[-1]

            if "collision" in level:
                continue

            if level not in self.texmap:
                self.texmap[level] = Image(resource_find(f"{level}.png"))

        self.spawn_tile_layers(self.m_map.current_tilesets)

        offset = (0, 0)  # TODO: TEMP

        # if conns := self.m_map.current_connected_tilesets:
        #     for (tiles, portal_pos, target_pos, direction,) in conns:
        #         if direction == "E":
        #             direction = (1, 0)
        #         elif direction == "S":
        #             direction = (0, 1)
        #         elif direction == "W":
        #             direction = (-1, 0)
        #         elif direction == "N":
        #             direction = (0, -1)
        #         conn_offset = (
        #             offset[0] - portal_pos[0] - direction[0] + target_pos[0],
        #             offset[1] - portal_pos[1] - direction[1] + target_pos[1],
        #         )

        #         self.spawn_tile_layers(tiles, offset=conn_offset)

    def update(self, time, dt):
        for layer in self.layers:
            layer.update(time, dt)

    def add_layer(self, widget):
        self.layers.append(widget)
        self.gamecanvas.add_widget(widget)

    def spawn_tile_layers(self, tileset_defs, offset=(0, 0)):

        self.game.m_col.clear_collision()
        self.game.m_col.set_offset(offset)

        print("Spawn layers! Offset:", offset)
        entity_h = 0  # TODO fix
        for h, mapdef in enumerate(tileset_defs):
            if mapdef[0] != "TILES":
                continue

            ltype, level, tiles, collision = mapdef

            if "collision" in level:
                continue

            tiles = tiles.copy()

            self.game.m_col.add_collision_layer(
                collision, entity_h, tiles if "collision" in level.lower() else None
            )

            for tile in tiles:
                m = max(tile.shape[:2])
                new = np.zeros((m, m, 2))  # TODO: VERY DIRTY FIX, refactor!
                # height of renderer doesn't work properly when input map isn't square.
                new[: tile.shape[0], : tile.shape[1], :] = tile

                temp_map = np.pad(
                    new, [(0, 0), (0, 0), (0, 2)], mode="constant", constant_values=0,
                ).astype(np.ubyte)

                level = level.split("/")[-1]

                # print("LAYER!", h, level, tiles.shape, "->", temp_map.shape)
                self.add_layer(
                    TileLayerWidget(
                        game=self.game,
                        tiles=temp_map,
                        texture_file=self.texmap[level],
                        level=level,
                        h=h,
                        offset=offset,
                    )
                )

        self.entitylayer = EntityLayerWidget(game=self.game, h=0, offset=offset)
        self.add_layer(self.entitylayer)
        self.game.m_ent.load_entities(offset)
