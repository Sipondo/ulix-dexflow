from ulivy.generator.ai import create_level

from multiprocessing import Manager, Process


class GeneratorManager:
    def __init__(self, game):
        self.game = game
        self.thread = None
        self.levels = [
            [
                2000,
                2001,
                2002,
                2003,
                2004,
                2005,
                [],
                ([(58, 10), (58, 12)], [(26, 110), (26, 112)]),
                None,
            ]
        ]

        self.manager = Manager()
        self.receiving_array = self.manager.list()
        self.receiving_array.append(None)
        self.level_is_done = self.manager.list()

        self.target_id = 0

        for _ in range(len(self.levels)):
            # self.level_is_done.append(False) # Overwrite to disable
            self.level_is_done.append(True)

    def get_done_progress(self):
        l = []
        for v in self.level_is_done:
            l.append(v)
        return l

    def overwrite_progress(self, done):
        for i in range(len(done)):
            self.level_is_done[i] = bool(done[i])
        if self.thread is not None and self.thread.is_alive():
            self.thread.terminate()

    def update(self, time, frame_time):
        if self.receiving_array[0] is not None:
            print("Writing level!")
            try:
                i = self.level_is_done.index(False)
                if self.target_id == i:
                    print(f"Results for level {i}")
                    for k, v in self.receiving_array[0].items():
                        self.game.m_map.overwrite_level(k, v)
                    self.level_is_done[i] = True
            except Exception as e:
                pass
            self.receiving_array[0] = None

        if False not in self.level_is_done or (
            self.thread is not None and self.thread.is_alive()
        ):
            return
        print("CHECK GEN THREAD", self.level_is_done)

        i = self.level_is_done.index(False)
        self.target_id = i

        target_id = self.levels[i][0]
        levels = self.game.m_map.get_all_levels()
        self.thread = Process(
            target=dispatch_generate,
            args=(self.receiving_array, levels, self.levels[i]),
        )
        self.thread.daemon = True
        self.thread.start()


def dispatch_generate(
    receiving_array,
    levels_data,
    infos,
):
    print(f"Creating level")
    if content := create_level(levels_data, *infos):
        receiving_array[0] = content
