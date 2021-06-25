from .baseentity import BaseEntity
from game.animation.moveanimation.basemoveanimation import BaseMoveAnimation


class CivilianEntity(BaseEntity):
    def __init__(self, game, position, direction, sprites, dialogue):
        super().__init__(game, position, direction, sprites)
        self.orig_pos = self.game_position
        self.dialogue = dialogue

    def on_interact(self):
        direc = self.game.m_ent.player.get_dir()
        self.direction = (-direc[0], -direc[1])
        self.current_sprite = (0, self.get_offset())

    def on_render(self):
        pass

    def on_enter(self):
        self.current_sprite = (0, self.get_offset())

    def start_move(self, direction, time, distance=1, lock=False):
        if not self.moving:
            if self.direction == direction:
                anim = BaseMoveAnimation(self.game, time, direction, self, distance=distance, lock=lock)
                if self.game.m_ani.add_animation(anim):
                    self.moving = True
            else:
                self.direction = direction
                self.set_current_sprite((self.movement_type, self.get_offset()))

    def after_move(self, time, frame_time):
        pass

    def on_step(self, time, frame_time):
        pass
