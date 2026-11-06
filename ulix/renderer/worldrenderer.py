import json
import numpy as np
import os
import struct
import zengl

from PIL import Image


# ############## TODO: move this to some resource manager thing

# with open(resource_find("ulivy_shaders/basic_tile_fs.glsl")) as file:
#     tile_shader_fs = file.read()

# with open(resource_find("ulivy_shaders/basic_tile_vs.glsl")) as file:
#     tile_shader_vs = file.read()

# with open(resource_find("ulivy_shaders/basic_entity_fs.glsl")) as file:
#     enti_shader_fs = file.read()

# # with open(resource_find("ulivy_shaders/basic_entity_gs.glsl")) as file:
# #     enti_shader_gs = file.read()

# with open(resource_find("ulivy_shaders/basic_entity_vs.glsl")) as file:
#     enti_shader_vs = file.read()

# #####################

with open("ulix_shaders/tile_fs.glsl") as file:
    tile_shader_fs = file.read()
with open("ulix_shaders/tile_vs.glsl") as file:
    tile_shader_vs = file.read()

###

with open("ulix_shaders/entity_fs.glsl") as file:
    entity_shader_fs = file.read()
with open("ulix_shaders/entity_vs.glsl") as file:
    entity_shader_vs = file.read()


class EntityLayer:
    def __init__(self, game, h, entity_h, offset):
        self.game = game
        self.ctx = game.ctx

        self.h = h
        self.entity_h = entity_h
        self.offset = (float(offset[0]), float(offset[1]))

    def setup(self, ctx, target, atlas): 
        self.ctx = ctx

        self.capacity = 256 * 10 * 4
        self.vertex_buffer = ctx.buffer(size=self.capacity)

        self.pipeline = ctx.pipeline(
            vertex_shader=entity_shader_vs,
            fragment_shader=entity_shader_fs,
            layout=[
                {"name": "atlas", "binding": 0},
            ],
            resources=[
                {
                    "type": "sampler",
                    "binding": 0,
                    "image": atlas,
                    "min_filter": "nearest",
                    "mag_filter": "nearest",
                    "wrap_x": "clamp_to_edge",
                    "wrap_y": "clamp_to_edge",
                },
            ],
            uniforms={
                "camera": [0.0, 0.0],
                "view_size": [21.0, 12.0],
                "map_offset": [float(self.offset[0]), float(self.offset[1])],
            },
            blend={
                "enable": True,
                "src_color": "src_alpha",
                "dst_color": "one_minus_src_alpha",
            },
            framebuffer=[target],
            topology="triangles",
            vertex_buffers=zengl.bind(
                self.vertex_buffer, "2f 2f 2f 2f 2f", 0, 1, 2, 3, 4
            ),
            vertex_count=0,
        )

    def render(self, camera, view_size):

        vertices, _ = self.game.m_ent.vertices(entity_h=self.entity_h)
        if not vertices:
            return False
        self.vertex_count = len(vertices) // 10

        vertex_data = struct.pack(f"{len(vertices)}f", *vertices)
        if len(vertex_data) > self.capacity:
            self.capacity = max(len(vertex_data), self.capacity * 2)
            self.vertex_buffer = self.ctx.buffer(size=self.capacity)

            self.pipeline.vertex_buffers = zengl.bind(
                self.vertex_buffer, "2f 2f 2f 2f 2f", 0, 1, 2, 3, 4
            )
        self.vertex_buffer.write(vertex_data)
        self.pipeline.vertex_count = self.vertex_count
        return True


class TileLayer:
    def __init__(self, game, tiles, level, size, h, offset):
        self.game = game
        self.ctx = game.ctx

        self.level = level
        self.map_size = size
        self.h = h
        self.offset = (float(offset[0]), float(offset[1]))

        self.tiles = tiles

        self.tiles_image = None
        self.pipeline = None


    def setup(self, ctx, target, atlas): 
        self.ctx = ctx
        h, w = self.tiles.shape[:2]

        self.tiles_image = ctx.image((w, h), "rg16uint", data=self.tiles.tobytes())

        self.pipeline = ctx.pipeline(
            vertex_shader=tile_shader_vs,
            fragment_shader=tile_shader_fs,
            layout=[
                {"name": "tiles", "binding": 0},
                {"name": "atlas", "binding": 1},
            ],
            resources=[
                {
                    "type": "sampler",
                    "binding": 0,
                    "image": self.tiles_image,
                    "min_filter": "nearest",
                    "mag_filter": "nearest",
                    "wrap_x": "clamp_to_edge",
                    "wrap_y": "clamp_to_edge",
                },
                {
                    "type": "sampler",
                    "binding": 1,
                    "image": atlas,
                    "min_filter": "nearest",
                    "mag_filter": "nearest",
                    "wrap_x": "clamp_to_edge",
                    "wrap_y": "clamp_to_edge",
                },
            ],
            uniforms={
                "camera": [0.0, 0.0],
                "view_size": [21.0, 12.0],
                "map_offset": [float(self.offset[0]), float(self.offset[1])],
            },
            blend={
                "enable": True,
                "src_color": "src_alpha",
                "dst_color": "one_minus_src_alpha",
            },
            framebuffer=[target],
            topology="triangles",
            vertex_count=3,
        )


class WorldRenderer:
    def __init__(self, game):

        self.game = game

        self.size = game.RENDER_SIZE

        self.m_map = game.m_map
        self.m_map.load_world_data()
        self.layers = []
        self.entitylayers = []

        self.set_map_via_manager()

    def setup(self, ctx, target):
        self.ctx = ctx
        self.target = target

        atlas_pil = Image.open(f"data/atlas_tiles.png").convert("RGBA")
        self.atlas = self.ctx.image(atlas_pil.size, 'rgba8unorm', data=atlas_pil.tobytes())

        # atlas_character = Image.open(f"resources/essentials/graphics/characteratlas-0.png").convert("RGBA")
        # self.atlas_character = self.ctx.image(atlas_character.size, 'rgba8unorm', data=atlas_character.tobytes())
        self.atlas_character = self.game.atlas.original_textures[0]
        with open("resources/essentials/graphics/characteratlas.atlas", "rb") as f:
            atlas_data = json.load(f)

        raw_ids = atlas_data.get("characteratlas-0.png", {})
        self.character_ids = { # TODO: move this to atlas creation?
            k: [float(v[0]), 4096.0 - v[1] - v[3], float(v[2]), float(v[3])]
            for k, v in raw_ids.items()
        }

        for layer in self.layers:
            if isinstance(layer, TileLayer):
                layer.setup(self.ctx,
                            self.target,
                            self.atlas)
            elif isinstance(layer, EntityLayer):
                layer.setup(self.ctx,
                            self.target,
                            self.atlas_character)

    def render(self, time, dt):
        camera = (self.game.m_pan.total_x, self.game.m_pan.total_y)
        view_size = (21.0 * self.game.m_pan.zoom_value, 12.0 * self.game.m_pan.zoom_value) # TODO: move to m_pan?

        self.target.clear()
        for layer in sorted(self.layers, key=lambda x: x.h):
            if isinstance(layer, EntityLayer):
                if not layer.render(camera, view_size):
                    continue

            uniforms = layer.pipeline.uniforms
            uniforms["camera"][:] = struct.pack("2f", *camera)
            uniforms["view_size"][:] = struct.pack("2f", *view_size)
            uniforms["map_offset"][:] = struct.pack(
                "2f", float(layer.offset[0]), float(layer.offset[1])
            )

            layer.pipeline.render()

    def clear_layers(self):
        for layer in self.layers:
            del layer

        self.layers = []
        self.entitylayers = []

    def update(self, time, dt):
        for layer in sorted(self.layers, key=lambda x: x.h):
            layer.update(time, dt)

    def add_layer(self, widget):
        self.layers.append(widget)

    def set_map_via_manager(self, offset=(0, 0), fade=True):
        # self.game.r_fad.go_to(0.0)
        self.clear_layers()

        self.game.m_sav.save("current_offset", offset)

        self.texmap = {}

        # print(self.m_map.current_tilesets)
        for mapdef in self.m_map.current_tilesets[-1]:
            if mapdef[0] != "TILES":
                continue

            ltype, level, tiles, collision = mapdef
            level = level.split("/")[-1]

            if "collision" in level:
                continue

        self.spawn_tile_layers(self.m_map.current_tilesets, offset=offset, primary=True)

        offset = tuple(offset)

        if conns := self.m_map.current_connected_tilesets:
            for (
                size,
                tiles,
                portal_pos,
                target_pos,
                direction,
            ) in conns:

                if direction == "E":
                    direction = (1, 0)
                elif direction == "S":
                    direction = (0, 1)
                elif direction == "W":
                    direction = (-1, 0)
                elif direction == "N":
                    direction = (0, -1)
                else:
                    raise Exception(
                        f"Got invalid portalconnection direction '{direction}'!"
                    )
                conn_offset = (
                    offset[0] - portal_pos[0] - direction[0] + target_pos[0],
                    offset[1] - portal_pos[1] - direction[1] + target_pos[1],
                )

                self.spawn_tile_layers((size, tiles), offset=conn_offset)

        self.game.m_act.flush_regions()
        self.game.m_ent.flush_entities()
        self.game.m_ent.load_regions(offset)
        self.game.m_ent.load_entities(offset)

    def spawn_tile_layers(self, tileset_defs, offset=(0, 0), primary=False):
        # print("Spawn layers! Offset:", offset)
        if primary:
            self.game.m_col.clear_collision()
            self.game.m_col.set_offset(offset)

        size = tileset_defs[0]
        tileset_defs = tileset_defs[1]

        entity_h = 0  # TODO fix
        h = 0.1 if primary else 0.2
        for mapdef in tileset_defs:
            h += 1
            if mapdef[0] != "TILES":
                if mapdef[0] == "ENTITIES":
                    # print("ENTITYLAYER!", h)
                    self.spawn_entity_layer(h, entity_h)
                    entity_h += 1
                continue

            ltype, level, tiles, collision = mapdef

            if "collision" in level:
                continue

            tiles = tiles.copy()

            if primary:
                self.game.m_col.add_collision_layer(
                    collision, entity_h, False
                )  # tiles if "collision" in level.lower() else None
                # )

            level_name = level.split("/")[-1]
            for tile in tiles:
                h += 1
                self.add_layer(
                    TileLayer(
                        game=self.game,
                        tiles=tile,
                        level=level_name,
                        size=size,
                        h=h,
                        offset=offset,
                    )
                )

                # h += 1
                # # m = max(tile.shape[:2])
                # # new = np.zeros((m, m, 2))  # TODO: VERY DIRTY FIX, refactor!
                # # height of renderer doesn't work properly when input map isn't square.
                # new[: tile.shape[0], : tile.shape[1], :] = tile

                # temp_map = np.pad(
                #     new,
                #     [(0, 0), (0, 0), (0, 2)],
                #     mode="constant",
                #     constant_values=0,
                # ).astype(np.ubyte)

                # level = level.split("/")[-1]

                # # print("LAYER!", h, level, tiles.shape, "->", temp_map.shape)
                # self.add_layer(
                #     TileLayer(
                #         game=self.game,
                #         tiles=temp_map,
                #         level=level,
                #         size=size,
                #         h=h,
                #         offset=offset,
                #     )
                # )

    def spawn_entity_layer(self, h, entity_h, offset=(0, 0)):
        layer = EntityLayer(
            game=self.game,
            h=h,
            entity_h=entity_h,
            offset=offset,
        )
        self.add_layer(layer)
