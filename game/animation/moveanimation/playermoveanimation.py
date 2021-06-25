from .basemoveanimation import BaseMoveAnimation


class PlayerMoveAnimation(BaseMoveAnimation):
    def __init__(self, game, start, direction):
        super().__init__(game, start, direction, game.m_ent.player, lock=True)

    def check_continue(self):
        if self.movement_type == self.entity.movement_type:
            if not self.game.m_gst.current_state.lock:
                return self.get_direction() in self.game.m_key.pressed_keys
        super().check_continue()
