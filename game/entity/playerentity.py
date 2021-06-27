from .baseentity import BaseEntity
from game.animation.moveanimation.playermoveanimation import PlayerMoveAnimation
from game.animation.encounteranimation import EncounterAnimation
import random


class PlayerEntity(BaseEntity):
    def on_render(self):
        # Move camera with player!
        xoff = self.game.size[0] / 16 / 2
        yoff = self.game.size[1] / 16 / 2
        self.game.pan_tool.total_x = (
            (self.game_position[0] - xoff) * 64 / self.game.size[0]
        )
        self.game.pan_tool.total_y = (
            (-self.game_position[1] + yoff) * 64 / self.game.size[1]
        )

    def on_interact(self):
        pass

    def on_enter(self):
        print("direction:", self.direction)

    def start_move(self, direction_str, time):
        direction = self.direction_to_tuple(direction_str)
        if not self.moving:
            if self.direction == direction:
                anim = PlayerMoveAnimation(self.game, time, direction)
                if self.game.m_ani.add_animation(anim):
                    self.moving = True
            else:
                self.direction = direction
                self.set_current_sprite((self.movement_type, self.get_offset()))

    def after_move(self, time, frame_time):
        # self.game.m_act.check_regions(self.game_position)
        self.moving = False
        # self.game.m_gst.current_state.lock = self.game.m_evt.check_events(
        #     time, frame_time
        # )
        self.game.m_sav.save("player_pos", self.game_position)

        print(
            "A_STAR",
            self.game.m_col.a_star(
                self.game_position, (self.game_position[0] - 2, self.game_position[1])
            ),
        )

    def on_step(self, time, frame_time):
        if self.game.m_col.get_tile_flags(self.game_position)["Encounter"]:
            if random.random() < 0.1:
                self.game.m_ani.add_animation(EncounterAnimation(self.game, time))

    def direction_to_tuple(self, direction):
        if direction == "up":
            return (0, -1)
        elif direction == "down":
            return (0, 1)
        elif direction == "left":
            return (-1, 0)
        elif direction == "right":
            return (1, 0)
