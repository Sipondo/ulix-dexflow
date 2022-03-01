from .basemoveanimation import BaseMoveAnimation


class PlayerMoveAnimation(BaseMoveAnimation):
    def __init__(self, game, start, direction):
        super().__init__(game, start, direction, game.m_ent.player, lock=True)

    def on_tick(self, time, frame_time):
        # Prevent "bolting problem"
        if self.game.m_gst.current_state_name in ("overworld"):
            return super().on_tick(time, frame_time)
        self.on_end(time, frame_time)
        return False

    def check_continue(self):
        self.game.m_act.check_regions(self.entity)
        if (
            self.entity == self.game.m_ent.player
            and self.movement_type == self.entity.movement_type
            and self.game.m_gst.current_state_name in ("overworld")
        ):
            if not self.game.m_gst.current_state.lock:
                return self.get_direction() in self.game.m_key.pressed_keys
        elif self.distance > 0:
            return True
        return False
