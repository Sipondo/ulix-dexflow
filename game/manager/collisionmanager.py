import numpy as np


class CollisionManager:
    def __init__(self, game):
        self.game = game
        self.offset = (0, 0)

    def clear_collision(self):
        self.colmap = []

    def set_offset(self, offset):
        self.offset = offset

    def add_collision_layer(self, colmap, height):
        if not len(self.colmap) > height:
            # TODO Rewrite
            # UNSAFE
            self.colmap.append(colmap)
        else:
            self.colmap[height] = self.colmap[height] | colmap

    def check_collision(self, pos, direction, height=0, off=True):
        height = int(height)
        if off:
            pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])
        dx, dy = direction
        ox, oy = pos
        new_pos = ox + dx, oy + dy

        if self.game.maphack:
            return True
        for entity in self.game.m_ent.all_entities_on_height(height):
            x1, y1 = entity.get_pos()
            x1 += self.offset[0]
            y1 += self.offset[1]
            x2, y2 = new_pos
            if entity.solid and abs(x1 - x2) < 1 and abs(y1 - y2) < 1:
                return False
        return not (
            self.colmap[height][pos[1], pos[0], self.get_direction_num(direction)]
            or self.colmap[height][
                new_pos[1], new_pos[0], self.get_rec_direction_num(direction)
            ]
        )

    def get_tile_flags(self, pos, height=0):
        pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])
        return dict(
            zip(self.game.m_map.enum_values, self.colmap[height][pos[1], pos[0], 4:])
        )

    def a_star(self, fr, to, height=0, next_to=False):
        fr = (fr[0] + self.offset[0], fr[1] + self.offset[1])
        to = (to[0] + self.offset[0], to[1] + self.offset[1])

        if (
            not (
                0 < fr[0] < self.colmap[0].shape[0]
                and 0 < fr[1] < self.colmap[0].shape[1]
            )
        ) or (
            not (
                0 < to[0] < self.colmap[0].shape[0]
                and 0 < to[1] < self.colmap[0].shape[1]
            )
        ):
            return None

        map = np.ones(self.colmap[0].shape[:2]) * 9999

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
                    0 < x < self.colmap[0].shape[0]
                    and 0 < y < self.colmap[0].shape[1]
                    and map[x, y] >= 9999
                    and self.check_collision(fr, dir, height, off=False)
                ):
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
