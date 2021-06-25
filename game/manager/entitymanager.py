from game.entity.civilianentity import CivilianEntity
from game.entity.playerentity import PlayerEntity
from game.entity.portalentity import PortalEntity
from game.entity.portalconnectionentity import PortalConnectionEntity
from game.entity.opponententity import OpponentEntity

from itertools import chain
from math import floor, ceil
from pathlib import Path


class EntityManager:
    def __init__(self, gui):
        self.game = gui
        self.entities = []
        self.regions = []
        self.textures = []  # lists of paths
        self.texture_names = []
        self.load_textures()
        self.load_player()

    def get_textures(self):
        return self.textures

    def load_textures(self):
        self.textures, self.texture_names = self.game.m_res.get_entity_textures()
        # TODO
        self.game.r_ent.set_texture_map(self.textures)

    def load_player(self):
        player_sprites = ["boy_walk", "boy_run", "boy_bike"]
        self.player = PlayerEntity(
            self.game, self.game.m_sav.load("player_pos"), (0, -1), player_sprites
        )

    def load_regions(self, offset=(0, 0)):
        # print("\n\nREGIONS:")
        for region in self.game.m_map.current_regions:
            # print(region)
            if region["identifier"] == "Portal":
                self.create_region(
                    PortalEntity,
                    (
                        floor(region["location"][0] / 16) - offset[0],
                        ceil(region["location"][1] // 16) - offset[1],
                    ),
                    (region["width"] // 16, region["height"] // 16),
                    None,
                    self.game.m_map.convert_mapstring_to_key(region["f_target_level"]),
                    region["f_target_coords"],
                )
            elif region["identifier"] == "PortalConnection":
                self.create_region(
                    PortalConnectionEntity,
                    (
                        floor(region["location"][0] / 16) - offset[0],
                        ceil(region["location"][1] // 16) - offset[1],
                    ),
                    (region["width"] // 16, region["height"] // 16),
                    region["f_direction"],
                    self.game.m_map.convert_mapstring_to_key(region["f_target_level"]),
                    region["f_target_coords"],
                )

    def load_entities(self, offset=(0, 0)):
        # print("\n\nENTITIES:")
        for entity in self.game.m_map.current_entities:
            # print(entity)
            if entity["identifier"] == "Opponent":
                self.create_entity(
                    OpponentEntity,
                    (
                        floor(entity["location"][0] / 16) - offset[0],
                        ceil(entity["location"][1] // 16) - offset[1],
                    ),
                    entity["f_direction"],
                    [Path(entity["f_sprite"]).stem],
                    entity["f_dialogue"],
                )
            if entity["identifier"] == "Civilian":
                self.create_entity(
                    CivilianEntity,
                    (
                        floor(entity["location"][0] / 16) - offset[0],
                        ceil(entity["location"][1] // 16) - offset[1],
                    ),
                    entity["f_direction"],
                    [Path(entity["f_sprite"]).stem],
                    entity["f_dialogue"],
                )

    def flush_entities(self):
        self.entities.clear()
        # self.entities = [self.entities[0]]

    def flush_regions(self):
        self.regions.clear()

    def create_region(
        self, regiontype, pos, size, target_direction, target_level, target_location
    ):
        self.regions.append(
            regiontype(
                self.game, pos, size, target_direction, target_level, target_location
            )
        )

    def create_entity(self, entitytype, pos, direction, sprite, dialogue):
        self.entities.append(entitytype(self.game, pos, direction, sprite, dialogue))

    def render(self):
        draw_entities = sorted(self.entities + [self.player], key=lambda x: x.y)
        (xoff, yoff) = self.game.pan_tool.pan_value
        xoff *= self.game.pan_tool.warp_x
        yoff *= self.game.pan_tool.warp_y

        yoff += 6 / 16
        list_of_entity_data = []
        for entity in draw_entities:
            entity.on_render()
            mt, cf = entity.get_draw()  # movement type and current frame
            text_id = self.find_texture_id(entity, mt)
            x, y = entity.get_pos()
            x *= 16
            y *= 16
            list_of_entity_data.append([x, y, entity.height, text_id, cf])
        # list_of_entity_data = list(chain.from_iterable(list_of_entity_data))
        # TODO
        self.game.r_ent.set_entity_info(list_of_entity_data)

    def find_texture_id(self, entity, mt):
        return self.texture_names.index(entity.sprites[mt])
