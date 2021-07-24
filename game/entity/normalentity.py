from .baseentity import BaseEntity
from game.animation.moveanimation.basemoveanimation import BaseMoveAnimation
from pathlib import Path


class NormalEntity(BaseEntity):
    def __init__(self, game, position, ldtk_info):
        print(ldtk_info)
        for k, v in ldtk_info.items():
            if k[:2] == "f_":
                setattr(self, k[2:], v)
            else:
                setattr(self, k, v)

        super().__init__(game, position, self.direction, [Path(self.sprite).stem])
        self.orig_pos = self.game_position

    def when_interact(self):
        direc = self.game.m_ent.player.get_dir()
        self.direction = (-direc[0], -direc[1])
        self.current_sprite = (0, self.get_offset())
        self.game.m_act.create_action(self.on_interact_action, self)

    def on_enter(self):
        self.current_sprite = (0, self.get_offset())
        self.game.m_act.create_action(self.on_create_action, self)

    # def start_move(self, direction, time, distance=1, lock=False):
    #     if not self.moving:
    #         if self.direction == direction:
    #             anim = BaseMoveAnimation(
    #                 self.game, time, direction, self, distance=distance, lock=lock
    #             )
    #             if self.game.m_ani.add_animation(anim):
    #                 self.moving = True
    #         else:
    #             self.direction = direction
    #             self.set_current_sprite((self.movement_type, self.get_offset()))

    # self.create_entity(
    #     OpponentEntity,
    #     (
    #         floor(entity["location"][0] / 16) - offset[0],
    #         ceil(entity["location"][1] // 16) - offset[1],
    #     ),
    #     entity["f_direction"],
    #     [Path(entity["f_sprite"]).stem],
    #     entity["f_dialogue"],
    #     entity,
    # )

