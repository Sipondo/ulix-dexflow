class SetLocalEncounters:
    def __init__(self, act, src, user, rate, encounters):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.rate = rate
        self.encounters = encounters

    def on_tick(self, time=None, frame_time=None):
        self.game.m_map.local_encounter_rate = self.rate
        self.game.m_map.local_encounters = self.encounters
        return True

    def on_read(self):
        return None
