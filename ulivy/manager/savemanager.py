import json
import types
import numpy as np
import os
from io import BytesIO, TextIOWrapper
from ulivy.helpers.dataframe import Series


# from kivy.config import Config


ENTITY_SERIALIZE = (int, str, bool, tuple, list)
ENTITY_SERIALIZE_BLACKLIST = ["moving", "team"]


"""




Disabled, this stuff will see an overhaul soon anyway.





"""


class SaveManager:
    def __init__(self, game):
        self.game = game

        # Config.read(self.game.get_application_config())
        # Config.setdefaults("ulivy", {"savefile": "value1"})
        # Config.write()

        self.streaming = True
        self.last_save = 0
        self.restored_entities = False

        self.reset_store()
        # print("\n".join([f"{k}: {v}\n" for k, v in self.store.items()]))

    def reset_store(self):
        self.store = {
            "player_pos": (15, 12),
            "current_level_id": 1000,
            "current_hospital": "L1",
            "progression": 8,
            "winlist": set(),
            "cinskip": 0,
            "valid_save": 0,
            "MEMORY": {},
            "SETTABLES": {},
            "SWITCHES": {},
            "TEAM": [],
            "MOVES": [],
            "STORAGE": [],
            "ITEMS": [],
            "LEVEL_ENTITIES": {},
        }

        self.settables = ValueHolder(holder_is_frozen=False)
        self.settables.story_chapter = 0
        self.switches = ValueHolder(holder_is_frozen=False)
        self.globals = ValueHolder(holder_is_frozen=False)
        self.locals = ValueHolder(holder_is_frozen=False)
        self.memory = {}
        self.init_valueholders()
        self.load_save_soft()

    def load_save_soft(self):
        try:
            with open(self.game.get_application_config(), "rb") as infile:
                # self.store = json.loads(infile.read())
                sav = np.load(BytesIO(infile.read()), allow_pickle=True)
                store = {key: sav[key][()] for key in sav.files}

                if "progression" in store:
                    self.store["progression"] = store["progression"]
                if "winlist" in store:
                    self.store["winlist"] = store["winlist"]
                if "cinskip" in store:
                    self.store["cinskip"] = store["cinskip"]
                if "valid_save" in store:
                    self.store["valid_save"] = store["valid_save"]
        except Exception as e:
            pass

    def load_save_file(self):
        with open(self.game.get_application_config(), "rb") as infile:
            # self.store = json.loads(infile.read())
            sav = np.load(BytesIO(infile.read()), allow_pickle=True)
            self.store = {key: sav[key][()] for key in sav.files}

            self.game.inventory.reset_inventory()
            self.init_valueholders()

            self.game.m_map.levels = self.store["levels"]
            self.game.m_gen.overwrite_progress(self.store["levelsdone"])

            self.game.m_map.set_level(self.store["current_level_id"])

            o = (
                int(self.store["current_offset"][0]),
                int(self.store["current_offset"][1]),
            )
            self.game.r_fbo.r_til.set_map_via_manager(
                o,
                fade=False,
            )

            x, y = self.store["player_pos"]
            self.game.m_ent.player.set_position(x, y)

            # TODO: replace hack
            from ulivy.animation.jumpanimation import JumpAnimation

            self.anim = JumpAnimation(self.game, self.game.time, self.game.m_ent.player)
            if self.game.m_ani.add_animation(self.anim):
                self.game.m_ent.player.moving = True

    def init_valueholders(self):
        for k, v in self.store["SETTABLES"].items():
            if k != "holder_is_frozen":
                self.set_settable(k, v)
        for k, v in self.store["SWITCHES"].items():
            if k != "holder_is_frozen":
                self.set_switch(k, v)

        # print("CHECKING MEMORY")
        for k, v in self.store["MEMORY"].items():
            self.memory[k] = {}
            for k_2, v_2 in v.items():
                self.memory[k][k_2] = ValueHolder(holder_is_frozen=False)
                for k_3, v_3 in v_2.items():
                    if k_3 != "holder_is_frozen":
                        setattr(self.memory[k][k_2], k_3, v_3)
                        # print("HOLDER", k, k_2, k_3, v_3)

        for member in self.store["TEAM"]:
            hp, member = member
            new_m = self.game.inventory.init_member(Series().from_dict(member), 75)
            new_m.current_hp = hp
            self.game.inventory.add_member(new_m)

        for i, member in enumerate(self.store["MOVES"]):
            self.game.inventory.members[i].actions = [
                Series().from_dict(move) for move in member
            ]

        for member in self.store["STORAGE"]:
            member = member.copy()
            raw = self.game.m_pbs.get_fighter_by_name(member["name"])

            for k, v in member.items():
                raw[k] = v
            mem = self.game.inventory.init_member(raw, raw.level)
            self.game.inventory.add_member_to_storage(mem)

        for item in self.store["ITEMS"]:
            self.game.inventory.add_item(item[0], item[1])
        # self.store["MEMORY"] = {k: {k_2: v_2.__dict__ for k_2, v_2 in v.items()} for k,v self.memory.items()}

        if "money" in self.store:
            self.game.inventory.money = self.store["money"]
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

        # self.write_to_file()

    def get_lazy_data(self):
        # TODO: remove player name from here
        self.save("player_name", self.game.m_ent.player.name)
        self.save("player_gender", self.game.m_ent.player.gender)

        # Party
        team = [(x.current_hp, x.series.to_dict()) for x in self.game.inventory.members]
        # for member in self.game.inventory.members:
        #     team.append(
        #         {k: getattr(v, "tolist", lambda: v)() for k, v in member.series.items()}
        #     )
        self.save("TEAM", team)

        moves = [[y.to_dict() for y in x.actions] for x in self.game.inventory.members]
        # for member in self.game.inventory.members:
        #     team.append(
        #         {k: getattr(v, "tolist", lambda: v)() for k, v in member.series.items()}
        #     )
        self.save("MOVES", moves)

        # Storage
        storage = [x.series.to_dict() for x in self.game.inventory.storage]
        # for member in self.game.inventory.storage:
        #     storage.append(
        #         {k: getattr(v, "tolist", lambda: v)() for k, v in member.series.items()}
        #     )
        self.save("STORAGE", storage)

        # Items
        items = [(x.identifier, x.quantity) for x in self.game.inventory.items]
        # for member in self.game.inventory.items:
        #     items.append(
        #         {k: getattr(v, "tolist", lambda: v)() for k, v in member.series.items()}
        #     )
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
        return
        if True:  # self.game.m_map.allow_save:
            print("\n\n\nWRITING!!!!!!!!!")
            self.get_lazy_data()

            self.save("player_pos", self.game.m_ent.player.game_position)
            self.save("player_height", self.game.m_ent.player.height)
            self.save("current_level_id", self.game.m_map.current_level_id)

            self.store["SETTABLES"] = self.settables.__dict__
            self.store["SWITCHES"] = self.switches.__dict__

            self.store["levels"] = self.game.m_map.levels
            self.store["levelsdone"] = self.game.m_gen.get_done_progress()

            self.store["MEMORY"] = {
                str(k): {str(k_2): v_2.__dict__ for k_2, v_2 in v.items()}
                for k, v in self.memory.items()
            }

            # for k, v in self.store.items():
            #     if k == "levels":
            #         continue
            #     print(k, v)

            # with open(fname, "w") as outfile:
            #     outfile.write(json.dumps(self.store, indent=4))
            f = BytesIO()
            np.savez_compressed(f, **self.store)
            f.seek(0)
            out = f.read()
            with open(self.game.get_application_config(), "wb") as outfile:
                outfile.write(out)

            # buffer = TextIOWrapper(f, encoding="utf-8").read()
            # Config.set("ulivy", "savefile", buffer.encode("ascii", errors="ignore"))
            # Config.write()


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
