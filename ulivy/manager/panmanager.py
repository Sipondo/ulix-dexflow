class PanManager:
    def __init__(self, game, size):
        self.game = game
        self.total_x = 0.0
        self.total_y = 0.0

        # self.zoom = 800.0
        # self.zoom_level = 4
        # self.zoom_options = [12000, 7000, 4600, 3000, 2000, 1200, 800, 100]

        # self.size = size

    def set_pan(self, pos):
        self.total_x = pos[0] - (21 / 2) + 0.5
        self.total_y = pos[1] - (12 / 2) + 0.5

    # def on_tick(self, time, frame_time):
    #     target = self.zoom_options[self.zoom_level]
    #     speed = target - self.zoom

    #     # print(self.zoom, target, speed)

    #     if abs(speed) < 2:
    #         self.zoom = target
    #         return

    #     if abs(speed) < 10:
    #         if speed < 0:
    #             speed = -10
    #         else:
    #             speed = 10
    #     self.zoom += speed * frame_time * 4

    # def zoom_in(self):
    #     # self.zoom = max(500, self.zoom - 200)
    #     self.zoom_level = min(len(self.zoom_options) - 1, self.zoom_level + 1)

    # def zoom_out(self):
    #     # self.zoom = min(4000, self.zoom + 200)
    #     self.zoom_level = max(0, self.zoom_level - 1)

    # def zoom_encounter(self):
    #     # self.zoom = min(4000, self.zoom + 200)
    #     self.zoom_level = len(self.zoom_options) - 1

    # @property
    # def warp_x(self):
    #     return self.size[0] / 320

    # @property
    # def warp_y(self):
    #     return self.size[1] / 320

    # @property
    # def pan_value(self):
    #     panv = (
    #         round(16 * 5 * self.total_x),  # + 128,
    #         round(9 * -(5 * self.total_y)),  # + 42,
    #     )
    #     # print(panv)
    #     return panv

    # @property
    # def zoom_value(self):
    #     return 100 / self.zoom, 100 / self.zoom
