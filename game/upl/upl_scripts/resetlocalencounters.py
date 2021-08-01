class ResetLocalEncounters:
    def __init__(self, act, src, user):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time

    def on_tick(self, time=None, frame_time=None):
        self.game.m_map.local_encounter_rate = 0
        self.game.m_map.local_encounters = ""
        return True

    def on_read(self):
        return None
