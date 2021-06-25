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

    def check_collision(self, pos, direction, height=0):
        pos = (pos[0] + self.offset[0], pos[1] + self.offset[1])
        dx, dy = direction
        ox, oy = pos
        new_pos = ox + dx, oy + dy
        if self.game.maphack:
            return True
        for entity in self.game.m_ent.entities:
            x1, y1 = entity.get_pos()
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
