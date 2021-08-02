from .baseentity import BaseEntity
from game.animation.moveanimation.basemoveanimation import BaseMoveAnimation
from pathlib import Path
import json


class NormalEntity(BaseEntity):
    def __init__(self, game, position, ldtk_info):
        self.direction = (1, 0)
        self.sprite = None
        for k, v in ldtk_info.items():
            print(k, v)
            if k[:2] == "f_":
                setattr(self, k[2:], v)
            else:
                setattr(self, k, v)

        super().__init__(
            game,
            position,
            self.direction,
            self.sprite and [Path(self.sprite).stem] or [],
        )
        self.orig_pos = self.game_position
        self.memory = self.game.m_sav.get_memory_holder(self.level, self.entity_uid)

        if hasattr(self, "splash") and self.splash:
            self.splash = self.game.m_res.get_trainer_splash(Path(self.splash).stem)

        if hasattr(self, "aggro_range"):
            print(self.name, "HAS AGGRO RANGE ", self.aggro_range)
            print("POKEMON ARE:", self.battlers, self.config)
            self.aggro_region = self.game.m_act.create_aggro_region(self, {})

            self.team = []
            for battler in self.battlers:
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

            print(self.team)

    def when_interact(self):
        direc = self.game.m_ent.player.get_dir()
        self.direction = (-direc[0], -direc[1])
        self.current_sprite = (0, self.get_offset())
        self.game.m_act.create_action(self.on_interact_action, self)

    def on_enter(self):
        print("ON ENTER!!!", self.name)
        self.current_sprite = (0, self.get_offset())
        self.game.m_act.create_action(self.on_create_action, self)

    @property
    def mem(self):
        return self.memory
