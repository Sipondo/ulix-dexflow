from .baseevent import BaseEvent


class WalkEvent(BaseEvent):
    def __init__(self, game, location, entity, multitrigger=False, lock=True):
        super().__init__(game, location, lock=lock, multitrigger=multitrigger)
        self.entity = entity

    def check_trigger(self):
        if self.game.m_ent.player.get_pos() in self.location:
            return True

    def on_trigger(self, time):
        self.game.r_aud.play_effect("spotted")
        self.triggered = True
        self.entity.start_move(
            self.entity.direction, time, distance=self.entity.view_range, lock=True
        )
