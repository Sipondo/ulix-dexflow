class BattleMovement:
    def __init__(self, game, render):
        self.t0 = (-1, 0, 0)
        self.t1 = (1, 0, 0)

        self.t0_base = self.t0
        self.t1_base = self.t1

        self.t0_to = None
        self.t0_speed = 1.0
        self.t0_recover = False
        self.t0_go = False

        self.t1_to = None
        self.t1_speed = 1.0
        self.t1_recover = False
        self.t1_go = False

    def set_movement(self, team, position, speed, recover):
        if team == 0:
            self.t0_recover = 0.005 if recover else False
            if speed is not None:
                self.t0_go = 0.005
                self.t0_to = position
                self.t0_speed = speed
            else:
                self.t0_to = None
                self.t0_speed = None
                self.t0 = position
        elif team == 1:
            self.t1_recover = 0.005 if recover else False
            if speed is not None:
                self.t1_go = 0.005
                self.t1_to = position
                self.t1_speed = speed
            else:
                self.t1_to = None
                self.t1_speed = None
                self.t1 = position

    def render(self, time, frame_time):
        if self.t0_to is not None:
            self.t0_go = self.t0_go + frame_time * 0.01
            f = self.t0_go * self.t0_speed
            f_i = 1.0 - f

            self.t0 = (
                f * self.t0_to[0] + f_i * self.t0[0],
                f * self.t0_to[1] + f_i * self.t0[1],
                f * self.t0_to[2] + f_i * self.t0[2],
            )

            if self.eucl(self.t0, self.t0_to) < 0.0001:
                self.t0 = self.t0_to
                self.t0_to = None
                self.t0_go = False
        elif self.t0_recover:
            self.t0_recover = self.t0_recover + frame_time * 0.01
            f = self.t0_recover
            f_i = 1.0 - f
            self.t0 = (
                f * self.t0_base[0] + f_i * self.t0[0],
                f * self.t0_base[1] + f_i * self.t0[1],
                f * self.t0_base[2] + f_i * self.t0[2],
            )

            if self.eucl(self.t0, self.t0_base) < 0.0001:
                self.t0 = self.t0_base
                self.t0_recover = False

        if self.t1_to is not None:
            self.t1_go = self.t1_go + frame_time * 0.01
            f = self.t1_go * self.t1_speed
            f_i = 1.0 - f

            self.t1 = (
                f * self.t1_to[0] + f_i * self.t1[0],
                f * self.t1_to[1] + f_i * self.t1[1],
                f * self.t1_to[2] + f_i * self.t1[2],
            )

            if self.eucl(self.t1, self.t1_to) < 0.0001:
                self.t1 = self.t1_to
                self.t1_to = None
                self.t1_go = False
        elif self.t1_recover:
            self.t1_recover = self.t1_recover + frame_time * 0.01
            f = self.t1_recover
            f_i = 1.0 - f
            self.t1 = (
                f * self.t1_base[0] + f_i * self.t1[0],
                f * self.t1_base[1] + f_i * self.t1[1],
                f * self.t1_base[2] + f_i * self.t1[2],
            )

            if self.eucl(self.t1, self.t1_base) < 0.0001:
                self.t1 = self.t1_base
                self.t1_recover = False

    def eucl(self, fr, to):
        return (fr[0] - to[0]) ** 2 + (fr[1] - to[1]) ** 2 + (fr[2] - to[2]) ** 2
