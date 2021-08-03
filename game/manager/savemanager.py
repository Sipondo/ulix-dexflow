import json
import types
import numpy as np
from io import BytesIO
import pandas as pd

ENTITY_SERIALIZE = (int, str, bool, tuple, list, pd.Series)
ENTITY_SERIALIZE_BLACKLIST = "moving"


class SaveManager:
    def __init__(self, game):
        self.game = game
        self.streaming = True
        self.last_save = 0
        self.restored_entities = False

        self.settables = ValueHolder(holder_is_frozen=False)
        self.switches = ValueHolder(holder_is_frozen=False)
        self.globals = ValueHolder(holder_is_frozen=False)
        self.locals = ValueHolder(holder_is_frozen=False)
        self.memory = {}

        try:
            with open("streamingsave.usave", "rb") as infile:
                # self.store = json.loads(infile.read())
                sav = np.load(BytesIO(infile.read()), allow_pickle=True)
                self.store = {key: sav[key][()] for key in sav.files}
        except Exception as e:
            print("Warning: No streaming save found. Defaulting...")
            self.store = {
                "player_pos": (15, 15),
                "current_level_id": 1000,
                "MEMORY": {},
                "SETTABLES": {},
                "SWITCHES": {},
                "TEAM": [],
                "STORAGE": [],
                "ITEMS": [],
                "LEVEL_ENTITIES": {},
            }
        # print("\n".join([f"{k}: {v}\n" for k, v in self.store.items()]))

        for k, v in self.store["SETTABLES"].items():
            if k != "holder_is_frozen":
                self.set_settable(k, v)
        for k, v in self.store["SWITCHES"].items():
            if k != "holder_is_frozen":
                self.set_switch(k, v)

        for k, v in self.store["MEMORY"].items():
            self.memory[k] = {}
            for k_2, v_2 in v.items():
                self.memory[k][k_2] = ValueHolder(holder_is_frozen=False)
                for k_3, v_3 in v_2.items():
                    if k_3 != "holder_is_frozen":
                        setattr(self.memory[k][k_2], k_3, v_3)

        # self.store["MEMORY"] = {k: {k_2: v_2.__dict__ for k_2, v_2 in v.items()} for k,v self.memory.items()}

        self.settables.holder_is_frozen = True
        self.switches.holder_is_frozen = True
        # print("SETTABLES:", self.settables.__dict__)
        # print("SWITCHES:", self.switches.__dict__)

    def go_to_new_level(self):
        self.locals = ValueHolder(holder_is_frozen=False)

    def restore_entities(self):
        if self.restored_entities:
            return None
        self.restored_entities = True

        for entname, values in self.store["LEVEL_ENTITIES"].items():
            try:
                entity = self.game.m_ent.entities[entname]
                for k, v in values.items():
                    try:
                        setattr(entity, k, v)
                    except Exception:
                        continue
            except Exception:
                continue

    def get_memory_holder(self, level, entity):
        level = str(level)
        entity = str(entity)
        if level not in self.memory:
            self.memory[level] = {}

        if entity not in self.memory[level]:
            self.memory[level][entity] = ValueHolder(holder_is_frozen=False)

        return self.memory[level][entity]

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
        if (
            time - self.last_save < 5
            or self.game.m_gst.current_state_name != "overworld"
        ):
            return
        self.last_save = time

        self.write_to_file("streamingsave.usave")

    def get_lazy_data(self):
        # Party
        team = []
        for member in self.game.inventory.members:
            team.append(
                {k: getattr(v, "tolist", lambda: v)() for k, v in member.series.items()}
            )
        self.save("TEAM", team)

        # Storage
        storage = []
        for member in self.game.inventory.storage:
            storage.append(
                {k: getattr(v, "tolist", lambda: v)() for k, v in member.series.items()}
            )
        self.save("STORAGE", storage)

        # Items
        items = []
        for member in self.game.inventory.items:
            items.append(
                {k: getattr(v, "tolist", lambda: v)() for k, v in member.series.items()}
            )
        self.save("ITEMS", items)

        # Current Level Entities
        level_entities = {}
        for tag, entity in self.game.m_ent.entities.items():
            level_entities[tag] = {
                k: v
                for k, v in entity.__dict__.items()
                if type(v) in ENTITY_SERIALIZE and k not in ENTITY_SERIALIZE_BLACKLIST
            }
            level_entities[tag]["game_position"] = entity.start_pos

        self.save("LEVEL_ENTITIES", level_entities)

    def set_lazy_data(self):
        self.game.inventory.members = []

    def write_to_file(self, fname="save1.usave"):
        self.get_lazy_data()

        self.store["SETTABLES"] = self.settables.__dict__
        self.store["SWITCHES"] = self.switches.__dict__

        self.store["MEMORY"] = {
            str(k): {str(k_2): v_2.__dict__ for k_2, v_2 in v.items()}
            for k, v in self.memory.items()
        }

        # with open(fname, "w") as outfile:
        #     outfile.write(json.dumps(self.store, indent=4))
        f = BytesIO()
        np.savez_compressed(f, **self.store)
        f.seek(0)
        out = f.read()
        with open(fname, "wb") as outfile:
            outfile.write(out)


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
