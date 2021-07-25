from .baseentity import BaseEntity
from game.animation.moveanimation.basemoveanimation import BaseMoveAnimation
from pathlib import Path


class NormalEntity(BaseEntity):
    def __init__(self, game, position, ldtk_info):
        for k, v in ldtk_info.items():
            if k[:2] == "f_":
                setattr(self, k[2:], v)
            else:
                setattr(self, k, v)

        super().__init__(game, position, self.direction, [Path(self.sprite).stem])
        self.orig_pos = self.game_position
        self.memory = self.game.m_sav.get_memory_holder(self.level, self.entity_uid)

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
