import abc


class BaseEntity(abc.ABC):
    def __init__(self, game, position, direction, sprites=None, height=0, solid=True):
        self.solid = solid  # Can you move through this
        self.exists = True
        self.game = game
        self.movement_type = 0
        self.moving = False
        self.game_position = position
        self.height = height
        self.pos_vertical = 0

        if isinstance(direction, int):
            if direction == 0:
                self.direction = (1, 0)
            elif direction == 1:
                self.direction = (0, 1)
            elif direction == 2:
                self.direction = (-1, 0)
            elif direction == 3:
                self.direction = (0, -1)
        elif isinstance(direction, str):
            if direction == "E":
                self.direction = (1, 0)
            elif direction == "S":
                self.direction = (0, 1)
            elif direction == "W":
                self.direction = (-1, 0)
            elif direction == "N":
                self.direction = (0, -1)
        else:
            self.direction = direction

        self.sprites = sprites
        self.current_sprite = (0, 0)
        self.on_enter()

    def set_current_sprite(self, sprite):
        self.current_sprite = sprite

    def set_position(self, x, y):
        self.game_position = (x, y)

    def set_position_vertical(self, z):
        self.pos_vertical = z

    def set_movement_type(self, m_type):
        self.movement_type = m_type
        x, sprite = self.current_sprite
        self.set_current_sprite((m_type, sprite))

    def move_position(self, direction):
        dx, dy = direction
        ox, oy = self.game_position
        self.game_position = (ox + dx, oy + dy)

    def check_collision(self, direction, flags=False):
        x = self.game.m_col.check_collision_hop(
            self.game_position, direction, self.height
        )
        return x

    def get_draw(self):
        return self.current_sprite

    def get_pos(self):
        return self.game_position

    def get_dir(self):
        return self.direction

    def get_offset(self):
        if self.direction == (0, -1):
            return 12
        elif self.direction == (0, 1):
            return 0
        elif self.direction == (-1, 0):
            return 4
        elif self.direction == (1, 0):
            return 8

    def on_interact(self):
        pass

    def after_move(self, time, frame_time):
        self.moving = False
        self.after_move(time, frame_time)

    def on_enter(self):
        pass

    def on_render(self):
        pass

    def on_step(self, time, frame_time):
        pass

    @property
    def y(self):
        return self.game_position[1]
