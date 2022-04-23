import numpy as np


class CollisionManager:
    def __init__(self, game):
        self.game = game
        self.offset = (0, 0)

    def clear_collision(self):
        self.colmap = []

    def set_offset(self, offset):
        self.offset = offset

    def add_collision_layer(self, colmap, height, force):
        if not len(self.colmap) > height:
            # TODO Rewrite
            # UNSAFE
            self.colmap.append(colmap)
        else:
            if force is not None:
                force = force[0].sum(axis=2) > 0
                # print("\n\n\nCOL LAYER!!!!!!", colmap.shape, force[0].sum(axis=2) > 0)
                self.colmap[height][0][force] = colmap[force]
            else:
                self.colmap[height] = self.colmap[height] | colmap

    def check_collision(self, pos, direction, height=0, off=True, src_entity=None):
        height = int(height)
        if off:
            pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])
        dx, dy = direction
        ox, oy = pos
        new_pos = ox + dx, oy + dy

        if self.game.maphack and src_entity == self.game.m_ent.player:
            return True

        # Mapcheck
        try:
            col_fr = self.colmap[height][0][
                pos[1], pos[0], self.get_direction_num(direction)
            ]
            col_to = self.colmap[height][0][
                new_pos[1], new_pos[0], self.get_rec_direction_num(direction)
            ]
        except IndexError as e:
            print("Indexerror!", pos, direction, src_entity)
            return False

        for entity in self.game.m_ent.all_entities_on_height(height):
            if entity == src_entity or not entity.visible or not entity.active:
                continue
            # print(entity.game_position)
            x1, y1 = entity.get_pos()
            x1 += self.offset[0]
            y1 += self.offset[1]
            x2, y2 = pos
            if entity.solid and abs(x1 - x2) < 1 and abs(y1 - y2) < 1:
                col_fr = not entity.col_override
            x2, y2 = new_pos
            if entity.solid and abs(x1 - x2) < 1 and abs(y1 - y2) < 1:
                col_to = not entity.col_override

        return not (col_fr or col_to)

    def check_collision_hop(self, pos, direction, height=0, off=True, src_entity=None):
        height = int(height)
        free = self.check_collision(
            pos, direction, height=height, off=off, src_entity=src_entity
        )

        dx, dy = direction
        ox, oy = pos
        new_pos = ox + dx, oy + dy

        if free:
            return 1, new_pos

        old_new_pos = new_pos
        flags = self.get_tile_flags(new_pos, height=height, off=off)

        new_pos = ox + dx * 2, oy + dy * 2

        if self.game.inventory.count_item("JUMPERS"):
            if not self.get_col_flag(new_pos, height=height, off=off):
                if (
                    (direction == (0, -1) and flags["Hop_N"])
                    or (direction == (0, 1) and flags["Hop_S"])
                    or (direction == (-1, 0) and flags["Hop_W"])
                    or (direction == (1, 0) and flags["Hop_E"])
                ):
                    return 2, new_pos

        return False

    def get_tile_flags(self, pos, height=0, off=True):
        height = int(height)
        if off:
            pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])
        try:
            return dict(
                zip(
                    self.game.m_map.enum_values,
                    self.colmap[height][0][pos[1], pos[0], 4:],
                )
            )
        except IndexError:
            return dict(
                zip(
                    self.game.m_map.enum_values,
                    [False for _ in self.game.m_map.enum_values],
                )
            )

    def get_col_flag(
        self, pos, height=0, off=True, src_entity=None, check_entities=True
    ):
        height = int(height)
        if off:
            pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])

        if check_entities:
            for entity in self.game.m_ent.all_entities_on_height(height):
                if entity == src_entity or not entity.visible:
                    continue
                x1, y1 = entity.get_pos()
                x1 += self.offset[0]
                y1 += self.offset[1]
                x2, y2 = pos
                if entity.solid and abs(x1 - x2) < 1 and abs(y1 - y2) < 1:
                    return not entity.col_override
        return np.all(self.colmap[height][0][pos[1], pos[0], :4])

    def a_star(self, fr, to, height=0, next_to=False, src_entity=None):
        fr = (fr[0] + self.offset[0], fr[1] + self.offset[1])
        to = (to[0] + self.offset[0], to[1] + self.offset[1])

        if (
            not (
                0 < fr[0] < self.colmap[0][0].shape[1]
                and 0 < fr[1] < self.colmap[0][0].shape[0]
            )
        ) or (
            not (
                0 < to[0] < self.colmap[0][0].shape[1]
                and 0 < to[1] < self.colmap[0][0].shape[0]
            )
        ):
            return None

        map = np.ones(self.colmap[0][0].shape[:2]) * 9999

        map[fr[0], fr[1]] = 0

        nodes = [(fr, [])]
        iter = 0
        while nodes:
            iter = iter + 1
            fr, pth = nodes.pop(0)

            if fr[0] == to[0] and fr[1] == to[1]:
                return pth

            for i, (x, y) in enumerate(((1, 0), (0, 1), (-1, 0), (0, -1))):
                dir = (x, y)
                x += fr[0]
                y += fr[1]

                if next_to and x == to[0] and y == to[1]:
                    return pth

                if (
                    0 < x < self.colmap[0][0].shape[0]
                    and 0 < y < self.colmap[0][0].shape[1]
                    and map[x, y] >= 9999
                ):
                    res = self.check_collision_hop(
                        fr, dir, height, off=False, src_entity=src_entity
                    )
                    if res:
                        # print(x, y, res)
                        # map[x, y] = len(pth)
                        x, y = res[1]
                        if map[x, y] >= 9999:
                            map[x, y] = len(pth)
                            nodes.append(((x, y), pth + [dir]))

        return None

    def get_direction_num(self, direction):
        if direction == (1, 0):
            return 0
        if direction == (0, 1):
            return 1
        if direction == (-1, 0):
            return 2
        if direction == (0, -1):
            return 3

    def get_rec_direction_num(self, direction):
        if direction == (1, 0):
            return 2
        if direction == (0, 1):
            return 3
        if direction == (-1, 0):
            return 0
        if direction == (0, -1):
            return 1
