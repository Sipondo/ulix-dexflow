from .baseentity import BaseEntity


class PortalConnectionEntity(BaseEntity):
    def __init__(
        self, game, position, size, target_direction, target_level, target_location
    ):
        if target_direction == "E":
            position = (position[0] + 1, position[1])
            target_location = (target_location[0] - 1, target_location[1])
        elif target_direction == "S":
            position = (position[0], position[1] + 1)
            target_location = (target_location[0], target_location[1] - 1)
        elif target_direction == "W":
            position = (position[0] - 1, position[1])
            target_location = (target_location[0] + 1, target_location[1])
        elif target_direction == "N":
            position = (position[0], position[1] - 1)
            target_location = (target_location[0], target_location[1] + 1)
        self.size = size
        self.target_level = target_level
        self.target_location = target_location
        # ADD Y
        print("position", position, target_location)

        super().__init__(game, position, (0, 0), ["empty"])
        self.solid = False
        self.orig_pos = self.game_position
        self.fade = False
        # self.target_location = (target_location[0], target_location[1] - 1)

    def on_interact(self):
        pass

    def on_render(self):
        pass

    def on_enter(self):
        self.current_sprite = (0, self.get_offset())
        self.game.m_evt.add_portal_event(self)

    def after_move(self, time, frame_time):
        pass

    def on_step(self, time, frame_time):
        pass
