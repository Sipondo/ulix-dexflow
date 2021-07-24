import moderngl
import numpy as np

from array import array
from moderngl_window import geometry
from PIL import Image


class TileLayer:
    def __init__(self, r_wld, offset, height, texture_map, spritemap, fade=True):
        self.game = r_wld.game
        self.ctx = r_wld.ctx
        self.r_wld = r_wld
        self.offset = offset
        self.texture_map = texture_map
        self.spritemap = spritemap
        self.height = height
        self.prog = self.game.m_res.get_program("tilelayer")

        self.render_enabled = self.spritemap is not None

        self.terminate = -1 if fade else 0
        self.terminate_step = 0.04
        self.terminated = False

    def temp_init(self):
        self.prog["displaySize"].value = self.game.size

        # self.prog["tilemapSize"].value = (
        #     self.spritemap.size[0] / 16,
        #     self.spritemap.size[1] / 16,
        # )
        self.prog["Zoom"].value = (100 / 2000, 100 / 2000)
        self.prog["Pan"].value = (0, 0)
        self.prog["offset"].value = self.offset

    def render(self, time, frame_time):
        if self.terminated or not self.render_enabled:
            return

        if self.terminate >= self.terminate_step:
            self.terminate += self.terminate_step * 60 * frame_time
            if self.terminate >= 1:
                self.terminated = True
        elif self.terminate <= -self.terminate_step:
            self.terminate += self.terminate_step * 60 * frame_time
        else:
            self.terminate = 0

        self.prog["Alpha"].value = (
            1.0 - (min(1, max(0, abs(self.terminate)))) ** 2.4
            if self.terminate
            else 1.0
        )

        self.temp_init()
        # temp
        self.prog["Pan"].value = (
            self.game.pan_tool.pan_value[0] / 16 + 10,
            self.game.pan_tool.pan_value[1] / 9 + 10,
        )
        self.prog["Zoom"].value = self.game.pan_tool.zoom_value
        # self.prog["tilemapSize"].value = (
        #     self.spritemap.size[0] / 16,
        #     self.spritemap.size[1] / 16,
        # )
        self.prog["layerHeight"].value = self.texture_map.size[2]
        self.prog["worldSize"].value = (
            self.texture_map.size[0],
            self.texture_map.size[1],
        )

        self.prog["texture_tileset"] = 0
        self.spritemap.use(location=0)
        self.prog["texturearray_masks"] = 1
        self.texture_map.use(location=1)
        self.r_wld.quad_fs.render(self.prog)


class EntityLayer:
    def __init__(self, r_wld, height, entity_height):
        self.r_wld = r_wld
        self.game = self.r_wld.game
        self.height = height
        self.entity_height = entity_height
        self.terminated = False
        self.terminate = 0
        self.terminate_step = 1

    def render(self, time, frame_time):
        if self.terminate:
            self.terminated = True
        self.game.r_ent.render(self.entity_height)


class WorldRenderer:
    def __init__(self, game, ctx, reserve="4MB"):
        self.game = game
        self.ctx = ctx
        self.offset = (0.5, 13 / 16)

        self.tile_layers = []
        self.quad_fs = geometry.quad_fs()

    def render(self, time, frame_time, locking=False):
        self.ctx.enable(moderngl.BLEND)

        if not locking:
            # print(len(self.tile_layers))
            for layer in self.tile_layers:
                if layer.terminated:
                    # self.tile_layers.remove(layer)
                    del layer
                else:
                    # TODO: pop from list (causes flickering?)
                    # elif layer.height < self.game.m_map.current_height:
                    layer.render(time, frame_time)
            # self.game.r_ent.render()
            # for layer in self.tile_layers:
            #     if layer.height >= self.game.m_map.current_height:
            #         # TODO: add entity layer and swap >= to >
            #         layer.render(time, frame_time)

        self.ctx.disable(moderngl.BLEND)

    def spawn_tile_layer(self, height, map, spritemap, offset=(0, 0), fade=True):

        if "collision" not in spritemap:
            spritemap = self.game.m_res.get_tileset(spritemap)
        else:
            spritemap = None

        map_b = map.tobytes()
        texture_map = self.ctx.texture_array(
            (map.shape[2], map.shape[1], map.shape[0]), 2, map_b, dtype="u2"
        )
        texture_map.filter = moderngl.NEAREST, moderngl.NEAREST
        texture_map.write(map_b)
        texture_map.use(location=1)

        offset = (offset[0] + self.offset[0], offset[1] + self.offset[1])
        self.tile_layers.append(
            TileLayer(self, offset, height, texture_map, spritemap, fade=fade)
        )
        self.tile_layers.sort(key=lambda x: x.height)

    def spawn_entity_layer(self, height, entity_height):
        self.tile_layers.append(EntityLayer(self, height, entity_height))
        self.tile_layers.sort(key=lambda x: x.height)

    def clear_tile_layers(self, fade):
        # self.tile_layers.clear()
        for layer in self.tile_layers:
            if not layer.terminated:
                if fade:
                    layer.terminate = layer.terminate_step
                else:
                    layer.terminated = True

    def set_map_via_manager(self, offset=(0, 0), fade=True):
        # TODO probably shouldn't be here
        self.game.m_sav.save("current_offset", offset)
        self.clear_tile_layers(fade)
        self.game.m_col.clear_collision()
        # self.game.m_evt.flush_events()
        self.game.m_ent.flush_regions()
        self.game.m_ent.flush_entities()
        self.game.m_ent.load_regions(offset)
        self.game.m_ent.load_entities(offset)
        self.game.m_col.set_offset(offset)

        entity_h = 0
        for h, mapdef in enumerate(self.game.m_map.current_tilesets):
            if mapdef[0] != "TILES":
                if mapdef[0] == "ENTITIES":
                    self.spawn_entity_layer(h, entity_h)
                    entity_h += 1
                continue
            ltype, level, tiles, collision = mapdef
            # if h < self.game.m_map.current_height:
            self.game.m_col.add_collision_layer(
                collision, entity_h, tiles if "collision" in level.lower() else None
            )
            self.spawn_tile_layer(h, tiles, level, offset=offset, fade=fade)

        if conns := self.game.m_map.current_connected_tilesets:
            for (tiles, portal_pos, target_pos, direction,) in conns:
                if direction == "E":
                    direction = (1, 0)
                elif direction == "S":
                    direction = (0, 1)
                elif direction == "W":
                    direction = (-1, 0)
                elif direction == "N":
                    direction = (0, -1)
                conn_offset = (
                    offset[0] - portal_pos[0] - direction[0] + target_pos[0],
                    offset[1] - portal_pos[1] - direction[1] + target_pos[1],
                )

                for h, mapdef in enumerate(tiles):
                    if mapdef[0] != "TILES":
                        continue
                    ltype, level, tiles, collision = mapdef
                    # if h < self.game.m_map.current_height:
                    #     self.game.m_col.add_collision_layer(collision)
                    self.spawn_tile_layer(
                        h, tiles, level, offset=conn_offset, fade=fade,
                    )
