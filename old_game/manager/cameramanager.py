import math
from re import S
from pyrr import Matrix44

DEFAULT_DISTANCE = 75.0
SHAKE_SPEED = 1 / 30

# Kutzooi
class CameraManager:
    def __init__(self, game):
        self.game = game
        self.turn_clock = True
        self.shake_value = 0.05
        self.shake_frame = 1
        self.shake_counter = 0

        self.angle = 30
        self.angle_t = 30
        self.speed = 3

        self.pos = (0, 0, 0)
        # self.pos_t = (0, 0, 0)

        self.distance = 50.0

        self.proj = Matrix44.perspective_projection(
            30.0, self.game.aspect_ratio, 0.1, 1000.0, dtype="f4"
        )
        self.set_lookat()

    def render(self, time: float, frame_time: float):
        # self.angle += frame_time * 30
        # Angle
        if (self.angle_t - self.angle) > 0:
            self.turn_clock = True if self.angle_t - self.angle < -180 else False
        else:
            self.turn_clock = False if self.angle_t - self.angle > 180 else True

        # print(self.angle_t, self.angle, self.turn_clock)

        if self.turn_clock:
            if self.angle - self.angle_t > 0:
                self.angle -= (
                    frame_time * max(0.5, self.angle - self.angle_t) / 1.0
                ) * self.speed
        else:
            if self.angle_t - self.angle > 0:
                self.angle += (
                    frame_time * max(0.5, self.angle_t - self.angle) / 1.0
                ) * self.speed
        self.angle %= 360

        # Position
        # if self.pos != self.pos_t:
        #     self.pos = (
        #         self.pos[0] + frame_time * (self.pos_t[0] - self.pos[0]) * 2,
        #         self.pos[1] + frame_time * (self.pos_t[1] - self.pos[1]) * 2,
        #         self.pos[2] + frame_time * (self.pos_t[2] - self.pos[2]) * 2,
        #     )

        self.shake_counter += frame_time
        if self.shake_counter > SHAKE_SPEED:
            self.shake_frame = -1 * self.shake_frame
            self.shake_counter -= SHAKE_SPEED
        self.set_lookat()

        self.bill_rot = Matrix44.from_z_rotation(-self.z_rotation, dtype="f4")
        self.rotate = Matrix44.from_z_rotation(self.z_rotation, dtype="f4")
        self.mvp = self.proj * self.lookat * self.rotate
        self.rotation_value = ((self.z_rotation / math.pi) % 2) * 2

    def go_to(self, target, speed):
        self.angle_t = target
        self.speed = speed

    def reset(self):
        self.speed = 3
        self.angle_t = 30
        self.turn_clock = True

    def set_lookat(self):
        self.lookat = Matrix44.look_at(
            (self.distance, 0, 14.0),  # self.distance / 5),
            (0.0, 0.0, self.distance / 25 * 3),
            (0.0, 0.0, 1.0),
            dtype="f4",
        )

    def set_dark(self, dark, recover, speed):
        pass

    @property
    def z_rotation(self):
        return (self.angle + 180) / 180 * math.pi

    @property
    def parallax_rotation(self):
        return -self.angle / 60 / 3

    @property
    def shake(self):
        return self.shake_frame * self.shake_value
