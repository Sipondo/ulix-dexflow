from collections import deque


class ActionManager:
    def __init__(self, game):
        self.game = game
        self.animations = []
        self.queue = deque()

    def on_tick(self, time, frame_time):
        locked = False
        self.queue.clear()
        for anim in self.animations:
            self.queue.append(anim)
        while len(self.queue) != 0:
            if self.queue.popleft().on_tick(time, frame_time):
                locked = True
        return locked
