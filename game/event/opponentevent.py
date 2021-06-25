from .baseevent import BaseEvent


class OpponentEvent(BaseEvent):
    def __init__(self, game, location, entity, multitrigger=False, lock=True):
        super().__init__(game, location, lock=lock, multitrigger=multitrigger)
        self.entity = entity

    def check_trigger(self):
        ox, oy = self.entity.get_pos()
        dx, dy = self.entity.get_dir()
        self.location = (ox + dx, oy + dy)
        if self.game.m_ent.player.get_pos() == self.location:
            return True

    def on_trigger(self, time):
        self.triggered = True
        self.game.m_gst.switch_state("battle")
