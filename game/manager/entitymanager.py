from game.entity.civilianentity import CivilianEntity
from game.entity.playerentity import PlayerEntity
from game.entity.opponententity import OpponentEntity

from itertools import chain
from math import floor, ceil
from pathlib import Path


class EntityManager:
    def __init__(self, gui):
        self.game = gui
        self.entities = {}
        self.regions = []
        self.textures = []  # lists of paths
        self.texture_names = []
        self.load_textures()
        self.load_player()

        self.entity_autolabel = 0

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
            self.game.m_act.create_region(
                (
                    floor(region["location"][0] / 16) - offset[0],
                    ceil(region["location"][1] // 16) - offset[1],
                ),
                (region["width"] // 16, region["height"] // 16),
                region,
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
                    entity,
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
                    entity,
                )

    def flush_entities(self):
        self.entities.clear()
        # self.entities = [self.entities[0]]

    def flush_regions(self):
        # self.regions.clear()
        self.game.m_act.flush_regions()

    def delete_entity(self, ent):
        self.entities.remove(ent)
        del ent

    def create_entity(self, entitytype, pos, direction, sprite, dialogue, blueprint):
        if blueprint["f_entity_uid"]:
            label = blueprint["f_entity_uid"]
        else:
            label = f"UNLABELLED_ENTITY_{self.entity_autolabel}"
            self.entity_autolabel += 1
        self.entities[label] = entitytype(self.game, pos, direction, sprite, dialogue)
        # TODO: remove hack
        self.entities[label].name = blueprint["f_name"]

    def render(self):
        draw_entities = sorted(
            list(self.entities.values()) + [self.player], key=lambda x: x.y
        )
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

    def all_entities_on_height(self, height):
        return [self.player] + [
            x for x in list(self.entities.values()) if x.height == height
        ]

    @property
    def all_entities(self):
        return [self.player] + list(self.entities.values())
