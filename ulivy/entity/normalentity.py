from .baseentity import BaseEntity
from pathlib import Path
import random


def charsum(s):
    return sum([ord(x) for x in s])


class NormalEntity(BaseEntity):
    def __init__(self, game, position, ldtk_info):
        self.direction = (1, 0)
        self.sprite = None
        for k, v in ldtk_info.items():
            if k[:2] == "f_":
                setattr(self, k[2:], v)
            else:
                setattr(self, k, v)

        super().__init__(
            game,
            position,
            self.direction,
            self.sprite and [Path(self.sprite).stem] or [],
            ldtk_info["layer"],
        )

        for k, v in ldtk_info.items():
            if k != "f_direction" and k != "f_sprite":
                # print(k, v)
                if k[:2] == "f_":
                    setattr(self, k[2:], v)
        # print("ACTIVE", self.active, self.sprites)

        self.orig_pos = self.game_position
        self.memory = self.game.m_sav.get_memory_holder(self.level, self.entity_uid)

        if hasattr(self, "aggro_range"):
            self.aggro_region = self.game.m_act.create_aggro_region(self, {})

            self.team = []
            for battler in self.battlers:  # TODO: re-enable
                self.team.append(self.game.m_pbs.get_fighter_by_name(battler))

            js = []
            try:
                js = eval(self.config)["team"]
            except Exception as e:
                pass
            for i, member in enumerate(self.team):
                if i < len(js):
                    battler_js = js[i]
                    for k, v in battler_js.items():
                        member[k] = v

                local_random = random.Random()
                local_random.seed(charsum(f"{self.entity_uid}{self.name}") % 429496729)
                try:
                    member["level"] = member.level
                except KeyError:
                    member["level"] = local_random.randint(
                        int(self.level) - 1, int(self.level) + 1
                    )
        # shops
        if hasattr(self, "items"):
            js = []
            try:
                js = eval(self.config)["items"]
            except Exception as e:
                print("Exception!", e)
                item_dict = {}
                for item in self.items:
                    item_dict[item] = {}
                self.items = item_dict
            self.items = js or self.items

    def when_interact(self):
        if self.active:
            direc = self.game.m_ent.player.get_dir()
            self.direction = (-direc[0], -direc[1])
            self.current_sprite = (0, self.get_offset())
            self.game.m_act.create_action(self.on_interact_action, self)

    def on_enter(self):
        print("ON ENTER!!!", self.name)
        self.current_sprite = (0, self.get_offset())
        if self.active:
            self.game.m_act.create_action(self.on_create_action, self)

    def on_step(self, time, frame_time):
        if hasattr(self, "aggro_range"):
            self.aggro_region.refresh_region()

    @property
    def mem(self):
        return self.memory
