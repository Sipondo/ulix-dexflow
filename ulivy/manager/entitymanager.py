# from game.entity.civilianentity import CivilianEntity
from ulivy.entity.normalentity import NormalEntity
from ulivy.entity.playerentity import PlayerEntity

# from game.entity.opponententity import OpponentEntity

from itertools import chain
from math import floor, ceil
from pathlib import Path


class EntityManager:
    def __init__(self, gui):
        self.game = gui
        self.entities = {}
        self.regions = []
        self.textures = []  # lists of paths
        self.load_player()

        self.entity_autolabel = 0

    def get_textures(self):
        return self.textures

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
            print("INITIALISING ENTITY")
            # print(entity)
            if entity["identifier"] in ("Civilian", "Opponent", "Invisible", "Shop"):
                self.create_entity(
                    NormalEntity,
                    (
                        floor(entity["location"][0] / 16) - offset[0],
                        ceil(entity["location"][1] // 16) - offset[1],
                    ),
                    entity,
                )
        self.game.m_sav.restore_entities()

    def flush_entities(self):
        for ent in self.entities.values():
            ent.entity_is_deleted = True
            del ent
        self.entities.clear()

    def create_entity(self, entitytype, pos, ldtk_info):
        if ldtk_info["f_entity_uid"]:
            label = ldtk_info["f_entity_uid"]
        else:
            label = f"UNLABELLED_ENTITY_{self.entity_autolabel}"
            self.entity_autolabel += 1
        self.entities[label] = entitytype(self.game, pos, ldtk_info)

    def render(self):
        draw_entities = sorted(
            list(self.entities.values()) + [self.player],
            key=lambda x: (x.render_priority, x.y_g),
        )
        (xoff, yoff) = self.game.pan_tool.pan_value
        xoff *= self.game.pan_tool.warp_x
        yoff *= self.game.pan_tool.warp_y

        yoff += 6 / 16
        list_of_entity_data = []
        for entity in draw_entities:
            if not entity.visible or not entity.sprites:
                continue
            entity.on_render()
            mt, cf = entity.get_draw()  # movement type and current frame
            text_id = self.find_texture_id(entity, mt)
            x, y = entity.get_pos()
            y += entity.pos_vertical
            x *= 16
            y *= 16
            list_of_entity_data.append([x, y, entity.height, text_id, cf])
        # list_of_entity_data = list(chain.from_iterable(list_of_entity_data))
        # TODO
        self.game.r_ent.set_entity_info(list_of_entity_data)

    def find_texture_id(self, entity, mt):
        return self.game.atlas.ids[entity.sprites[mt]]

    def all_entities_on_height(self, height):
        return [self.player] + [
            x for x in list(self.entities.values()) if x.height == height
        ]

    def vertices(self):
        draw_entities = sorted(
            list(self.entities.values()) + [self.player],
            key=lambda x: (x.render_priority, x.y_g),
        )

        vertices = []
        indices = []
        for entity in draw_entities:
            if not entity.visible or not entity.sprites:
                continue
            # entity.on_render()
            mt, cf = entity.get_draw()  # movement type and current frame
            text_id = self.find_texture_id(entity, mt)
            x, y = entity.get_pos()
            y += entity.pos_vertical
            # x *= 16
            # y *= 16
            # vertices.append([x, y, entity.height, text_id, cf])
            vertices.extend(
                [
                    x,
                    y,
                    float(text_id[2]) / 32 / 4,  # TODO: make dynamic
                    float(text_id[3]) / 32 / 4,  # TODO: make dynamic
                    float(text_id[0]),
                    float(text_id[1]),
                    float(text_id[2]),
                    float(text_id[3]),
                    float(cf % 4),
                    float(cf // 4),
                ]
            )
            indices.append(len(indices))

        return list(map(float, vertices)), indices

    @property
    def all_entities(self):
        return [self.player] + list(self.entities.values())
