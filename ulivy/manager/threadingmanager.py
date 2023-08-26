from ulivy.generator.ai import create_level

from multiprocessing import Manager, Process


class ThreadingManager:
    def __init__(self, game):
        self.game = game

        self.manager = Manager()
        self.receiving_lists = {}
        self.sending_lists = {}
        self.threads = []

        self.battlehandler = BattleHandler(self.game)

    def update(self, time, frame_time):
        for _, receiving in self.receiving_lists.items():
            if len(receiving):
                entry = receiving.pop(0)
                # entry[0](*entry[1:])
                self.battlehandler.handle(entry[1:])

    def start_func(self, name, func):
        sending, receiving = self.manager.list(), self.manager.list()
        thread = Process(
            target=func,
            args=(sending, receiving),
        )
        thread.daemon = True
        thread.start()

        self.sending_lists[name] = sending
        self.receiving_lists[name] = receiving

    def send(self, name, message):
        self.sending_lists[name].append(message)


# TODO: move
class BattleHandler:
    def __init__(self, game):
        self.game = game

    def handle(self, values):
        message = values[0]

        # print(f"`-----------\n\n[BattleHandler]{message}\n----------------")
        if isinstance(message, list):
            self.game.m_thr.send("showdown", message[0])
