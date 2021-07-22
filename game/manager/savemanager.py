import json
import types


class SaveManager:
    def __init__(self, game):
        self.game = game
        self.streaming = True
        self.last_save = 0

        self.settables = ValueHolder(holder_is_frozen=False)
        self.switches = ValueHolder(holder_is_frozen=False)

        try:
            with open("streamingsave.usave", "r") as infile:
                self.store = json.loads(infile.read())
        except Exception as e:
            print("Warning: No streaming save found. Defaulting...")
            self.store = {
                "player_pos": (15, 15),
                "current_level_id": 1000,
                "SETTABLES": {},
                "SWITCHES": {},
            }

        for k, v in self.store["SETTABLES"].items():
            if k != "holder_is_frozen":
                self.set_settable(k, v)
        for k, v in self.store["SWITCHES"].items():
            if k != "holder_is_frozen":
                self.set_switch(k, v)

        self.settables.holder_is_frozen = True
        self.switches.holder_is_frozen = True
        print("SETTABLES:", self.settables.__dict__)
        print("SWITCHES:", self.switches.__dict__)

    def save(self, loc, value):
        # print(f"Setting {loc}: {value}")
        self.store[loc] = value

    def save_new(self, loc, value):
        if loc not in self.store:
            self.save(loc, value)

    def load(self, loc, safe=True):
        if loc in self.store:
            return self.store[loc]
        if safe:
            print(f"Warning: {loc} not in store.")
            return 0
        else:
            raise NameError

    # def get_settable(self, loc):
    #     return getattr(self.settables, loc)

    def set_settable(self, loc, value, safe=True):
        # Check if it exists first
        if not safe and not hasattr(self.settables, loc):
            raise NameError
        setattr(self.settables, loc, value)

    def set_new_settable(self, loc, value):
        # Check if it exists first
        if not hasattr(self.settables, loc):
            setattr(self.settables, loc, value)

    # def get_switch(self, loc):
    #     return getattr(self.switches, loc)

    def set_switch(self, loc, value, safe=True):
        # Check if it exists first
        if not safe and not hasattr(self.switches, loc):
            raise NameError
        setattr(self.switches, loc, value)

    def set_new_switch(self, loc, value):
        # Check if it exists first
        if not hasattr(self.switches, loc):
            setattr(self.switches, loc, value)

    def render(self, time, frame_time):
        if time - self.last_save < 5:
            return
        self.last_save = time

        self.write_to_file("streamingsave.usave")

    def write_to_file(self, fname="save1.usave"):
        self.store["SETTABLES"] = self.settables.__dict__
        self.store["SWITCHES"] = self.switches.__dict__
        with open(fname, "w") as outfile:
            outfile.write(json.dumps(self.store, indent=4, sort_keys=True))


class ValueHolder(types.SimpleNamespace):
    def __setattr__(self, key, value):
        if (
            hasattr(self, "holder_is_frozen")
            and self.holder_is_frozen
            and not hasattr(self, key)
        ):
            raise TypeError(
                f"{key} is not a valid attribute. Did you add it to your LDTK world?"
            )
        object.__setattr__(self, key, value)
