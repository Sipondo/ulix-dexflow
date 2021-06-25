import json


class SaveManager:
    def __init__(self, game):
        self.game = game
        self.streaming = True
        self.last_save = 0
        try:
            with open("streamingsave.sssave", "r") as infile:
                self.store = json.loads(infile.read())
        except Exception as e:
            print("Warning: No streaming save found. Defaulting...")
            self.store = {"player_pos": (15, 15), "current_level_id": 1000}

    def save(self, loc, value):
        # print(f"Setting {loc}: {value}")
        self.store[loc] = value

    def load(self, loc):
        if loc in self.store:
            return self.store[loc]
        print(f"Warning: {loc} not in store.")
        return 0

    def render(self, time, frame_time):
        if time - self.last_save < 5:
            return
        self.last_save = time
        with open("streamingsave.sssave", "w") as outfile:
            outfile.write(json.dumps(self.store, indent=4, sort_keys=True))

    def write_to_file(self):
        with open("save1.sssave", "w") as outfile:
            outfile.write(json.dumps(self.store, indent=4, sort_keys=True))
