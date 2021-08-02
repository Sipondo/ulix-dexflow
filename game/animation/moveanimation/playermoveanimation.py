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
