from game.animation.baseanimation import BaseAnimation
from math import sin, pi


class JumpAnimation(BaseAnimation):
    def __init__(self, game, start, entity):
        self.duration = 0
        self.anim_speed = 0
        self.duration = 0.2
        self.entity = entity
        self.ended = False
        self.start_pos = self.entity.get_pos()
        print("START_POS", self.start_pos)
        self.stop = start + self.duration
        self.on_enter()
        super().__init__(game, start, lock=False)

    def on_enter(self):
        pass

    def on_tick(self, time, frame_time):

        if time > self.stop - 0.5 * frame_time:
            print("CURR_POS", self.entity.get_pos())
            self.entity.set_position(int(self.start_pos[0]), int(self.start_pos[1]))
            self.on_end(time, frame_time)
        else:
            progress = sin(pi * ((self.stop - time) / self.duration)) / 2
            # self.entity.set_position(self.start_pos[0], self.start_pos[1] - progress)
            self.entity.set_position_vertical(-progress)
        return self.lock

    def continue_move(self, time, frame_time):
        self.start = time
        self.stop = self.start + self.duration
        self.on_enter()

    def on_end(self, time, frame_time):
        self.ended = True
        self.entity.after_move(time, frame_time)
        self.game.m_ani.remove_anim(self)

    def conditions(self):
        return True
