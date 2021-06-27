from .baseentity import BaseEntity
from game.animation.moveanimation.basemoveanimation import BaseMoveAnimation
from game.animation.moveanimation.pathmoveanimation import PathMoveAnimation


class OpponentEntity(BaseEntity):
    def __init__(self, game, position, direction, sprites, dialogue, view_range=7):
        self.view_range = view_range
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
        self.game.m_evt.add_opponent_event(self)

    def start_move(self, direction, time, distance=1, lock=False):
        if not self.moving:
            if self.direction == direction:
                # anim = BaseMoveAnimation(
                #     self.game, time, direction, self, distance=distance, lock=lock
                # )
                print(self.game_position)
                print((19 - self.game.m_col.offset[0], 21 - self.game.m_col.offset[1]))
                path = self.game.m_col.a_star(
                    self.game_position,
                    (27 - self.game.m_col.offset[0], 12 - self.game.m_col.offset[1]),
                    # (self.game_position[0] - 5, self.game_position[1] - 8),
                    next_to=True,
                )
                print("PATH:", path)
                anim = PathMoveAnimation(
                    self.game,
                    time,
                    path.pop(0),
                    self,
                    distance=len(path) + 1,
                    lock=lock,
                    path=path,
                )
                if self.game.m_ani.add_animation(anim):
                    self.moving = True
            else:
                self.direction = direction
                self.set_current_sprite((self.movement_type, self.get_offset()))

    def after_move(self, time, frame_time):
        return
        self.game.m_act.check_regions(self.game_position)
        pass
        self.game.m_gst.current_state.lock = self.game.m_evt.check_events(
            time, frame_time
        )

    def on_step(self, time, frame_time):
        pass
