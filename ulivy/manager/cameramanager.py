import math
from pyrr import Matrix44

DEFAULT_DISTANCE = 75.0
SHAKE_SPEED = 1 / 30

# Kutzooi
class CameraManager:
    def __init__(self, game):
        self.game = game
        self.turn_clock = True
        self.shake_value = 0.0
        self.shake_frame = 1
        self.shake_counter = 0
        self.shake_dampen = True
        self.battle_shake = 1.0

        self.angle = 30
        self.angle_t = 30
        self.speed = 3
        self.distance_speed = 3
        self.height_speed = 3
        self.focus_speed = 3

        self.pos = (0.0, 0.0, 0.0)
        # self.pos_t = (0., 0., 0.)

        self.distance = 50.0
        self.distance_t = 50.0

        self.height = 0.0
        self.height_t = 0.0

        self.focus = 0.0
        self.focus_t = 0.0

        self.proj = Matrix44.perspective_projection(
            30.0, 16 / 9, 0.1, 1000.0, dtype="f4"
        )
        self.set_lookat()

    def render(self, time: float, frame_time: float):
        # print(self.proj)
        # self.angle += frame_time * 10

        # print(self.angle_t, self.angle, self.turn_clock)
        # print(self.distance_t, self.distance, self.distance_speed)
        # print(self.battle_shake, self.shake_value, frame_time)
        # Angle
        if (self.angle_t - self.angle) > 0:
            self.turn_clock = True if self.angle_t - self.angle < -180 else False
        else:
            self.turn_clock = False if self.angle_t - self.angle > 180 else True

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
        self.angle %= 720

        # Distance
        if self.distance_t > self.distance:
            self.distance += (
                frame_time * max(0.5, abs(self.distance_t - self.distance)) / 2.0
            ) * self.distance_speed
            if self.distance_t < self.distance:
                self.distance = self.distance_t

        if self.distance_t < self.distance:
            self.distance -= (
                frame_time * max(0.5, abs(self.distance_t - self.distance)) / 2.0
            ) * self.distance_speed
            if self.distance_t > self.distance:
                self.distance = self.distance_t

        # Height
        if self.height_t > self.height:
            self.height += (
                frame_time * max(0.5, abs(self.height_t - self.height)) / 2.0
            ) * self.height_speed
            if self.height_t < self.height:
                self.height = self.height_t

        if self.height_t < self.height:
            self.height -= (
                frame_time * max(0.5, abs(self.height_t - self.height)) / 2.0
            ) * self.height_speed
            if self.height_t > self.height:
                self.height = self.height_t

        # Focus
        if self.focus_t > self.focus:
            self.focus += (
                frame_time * max(0.5, abs(self.focus_t - self.focus)) / 2.0
            ) * self.focus_speed
            if self.focus_t < self.focus:
                self.focus = self.focus_t

        if self.focus_t < self.focus:
            self.focus -= (
                frame_time * max(0.5, abs(self.focus_t - self.focus)) / 2.0
            ) * self.focus_speed
            if self.focus_t > self.focus:
                self.focus = self.focus_t

        # # Position
        # if self.pos != self.pos_t:
        #     self.pos = (
        #         self.pos[0] + frame_time * (self.pos_t[0] - self.pos[0]) * 2,
        #         self.pos[1] + frame_time * (self.pos_t[1] - self.pos[1]) * 2,
        #         self.pos[2] + frame_time * (self.pos_t[2] - self.pos[2]) * 2,
        #     )

        if self.shake_dampen:
            self.shake_dampen = min(self.battle_shake + frame_time / 2, 1)
        self.shake_value = ((1.0 - self.battle_shake) / 2) ** 3.0

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

    def dist_to(self, target, speed):
        self.distance_t = target
        self.distance_speed = speed

    def height_to(self, target, speed):
        self.height_t = target
        self.height_speed = speed

    def focus_to(self, target, speed):
        self.focus_t = target
        self.focus_speed = speed

    def go_set(self, target):
        self.angle = target
        self.angle_t = target
        self.speed = 3

    def dist_set(self, target):
        self.distance = target
        self.distance_t = target
        self.distance_speed = 3

    def height_set(self, target):
        self.height = target
        self.height_t = target
        self.height_speed = 3

    def focus_set(self, target):
        self.focus = target
        self.focus_t = target
        self.focus_speed = 3

    def reset(self):
        self.speed = 3
        self.angle_t = 30
        self.turn_clock = True

    def set_lookat(self):
        self.lookat = Matrix44.look_at(
            (self.distance, 0, 14.0 + self.height),  # self.distance / 5),
            # (0.0, 0.0, self.distance / 25 * 3),
            (
                0.0,
                0.0,
                50 / 25 * 3 + max((150 / self.distance) - 3, 0) + self.height / 2 + self.focus,
            ),
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
