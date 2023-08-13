from ulivy.generator.ai import create_level

from multiprocessing import Manager, Process


class ThreadingManager:
    def __init__(self, game):
        self.game = game
        self.thread = None

        self.manager = Manager()
        self.receiving_array = self.manager.list()
        self.receiving_array.append(None)

    def update(self, time, frame_time):
        pass

    def start_func(self, func):
        self.thread = Process(
            target=func,
            args=(),
        )
        self.thread.daemon = True
        self.thread.start()
