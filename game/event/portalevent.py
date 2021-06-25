from .baseevent import BaseEvent


class PortalEvent(BaseEvent):
    def __init__(self, game, location, entity, multitrigger=False, lock=False):
        super().__init__(game, location, lock=lock, multitrigger=multitrigger)
        self.location = location
        self.entity = entity

    def check_trigger(self):
        if self.game.m_ent.player.get_pos() in self.location:
            return True

    def on_trigger(self, time):
        print("\n\nPORTAL EVENT\n\n")
        self.triggered = True
        # print(self.entity.target_level)
        self.game.m_map.set_level(self.entity.target_level)

        direc = self.game.m_ent.player.get_dir()
        locat = self.location[0]
        self.game.r_wld.set_map_via_manager(
            (
                self.entity.target_location[0] - locat[0] + direc[0],
                self.entity.target_location[1] - locat[1] + direc[1],
            ),
            fade=self.entity.fade,
        )
