from game.animation.baseanimation import BaseAnimation
from math import sin, cos, pi


class BaseMoveAnimation(BaseAnimation):
    def __init__(
        self, game, start, direction, entity, distance=1, lock=False, colcheck=True
    ):
        self.movement_type = entity.movement_type
        self.distance = distance
        self.duration = 0
        self.anim_speed = 0
        self.single_move_distance = 1
        self.get_anim_data()
        self.entity = entity
        self.direction = direction
        self.ended = False
        self.start_pos = self.entity.get_pos()
        # self.stop = start + self.duration
        self.start = start
        self.frame = self.get_offset()
        self.on_enter()
        self.colcheck = colcheck
        super().__init__(game, start, lock=lock)

    def on_enter(self):
        self.frame = self.get_offset()
        self.start_pos = self.entity.get_pos()

    def on_tick(self, time, frame_time):
        xdir, ydir = self.direction
        frame_number = self.frame
        if time > self.stop - 0.5 * frame_time:
            self.entity.set_position(
                int(self.start_pos[0] + xdir * self.single_move_distance),
                int(self.start_pos[1] + ydir * self.single_move_distance),
            )
            self.on_step(time, frame_time)
            if self.check_continue() and self.conditions():
                self.after_step(time, frame_time)
                self.continue_move(time, frame_time)
            else:
                self.after_step(time, frame_time)
                # self.entity.set_current_sprite((self.movement_type, frame_number))
                self.on_end(time, frame_time)
                return False
        else:
            frame_number += int(time * self.anim_speed) % 4
            self.entity.set_current_sprite((self.movement_type, frame_number))

            if self.single_move_distance == 1:
                progress = 1 - ((self.stop - time) / self.duration)
                self.entity.set_position(
                    self.start_pos[0] + xdir * progress * self.single_move_distance,
                    self.start_pos[1] + ydir * progress * self.single_move_distance,
                )

            elif self.single_move_distance > 1:
                progress = (1 + cos(pi * ((self.stop - time) / self.duration))) / 2

                progress += 1 - ((self.stop - time) / self.duration)
                progress /= 2
                self.entity.set_position(
                    self.start_pos[0] + xdir * progress * self.single_move_distance,
                    self.start_pos[1] + ydir * progress * self.single_move_distance,
                )

                progress = sin(pi * ((self.stop - time) / self.duration)) / 3
                self.entity.set_position_vertical(-progress)
        return self.lock

    def check_continue(self):
        self.game.m_act.check_regions(self.entity)
        if (
            self.entity == self.game.m_ent.player
            and self.movement_type == self.entity.movement_type
        ):
            if not self.game.m_gst.current_state.lock:
                return self.get_direction() in self.game.m_key.pressed_keys
        elif self.distance > 0:
            return True
        return False

    def on_step(self, time, frame_time):
        # self.entity.on_step(time, frame_time)
        self.distance -= 1

    def after_step(self, time, frame_time):
        self.entity.on_step(time, frame_time)

    def get_direction(self):
        if self.direction == (0, -1):
            return "up"
        elif self.direction == (0, 1):
            return "down"
        elif self.direction == (-1, 0):
            return "left"
        elif self.direction == (1, 0):
            return "right"

    def continue_move(self, time, frame_time):
        self.start = time
        self.on_enter()

    def get_offset(self):
        if self.direction == (0, -1):
            return 12
        elif self.direction == (0, 1):
            return 0
        elif self.direction == (-1, 0):
            return 4
        elif self.direction == (1, 0):
            return 8

    def get_anim_data(self):
        if self.single_move_distance != 1:
            self.duration = 0.4
            self.anim_speed = 0.1
        elif self.movement_type == 0:
            self.duration = 0.3
            self.anim_speed = 4
        elif self.movement_type == 1:
            self.duration = 0.2
            self.anim_speed = 8
        elif self.movement_type == 2:
            self.duration = 0.1
            self.anim_speed = 11

    def on_end(self, time, frame_time):
        self.entity.set_current_sprite((self.movement_type, self.frame))
        self.entity.after_move(time, frame_time)
        self.game.m_ani.remove_anim(self)
        self.ended = True

    def conditions(self):
        self.single_move_distance = 1

        if not self.colcheck:
            return True

        res = self.entity.check_collision(self.direction, flags=True)
        if res:
            self.single_move_distance = res[0]

        self.get_anim_data()
        return bool(res)

    @property
    def stop(self):
        return self.start + self.duration
