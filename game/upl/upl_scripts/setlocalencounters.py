"""function
Set local encounters, overriding level-wide settings.

Set local encounters. Typically only used within the **encounter** region.

in:
- Numeric: encounter rate
- String: encounter definition string
- Numeric: minimum level of encounters
- Numeric: maximum level of encounters

"""


class SetLocalEncounters:
    def __init__(self, act, src, user, rate, encounters, e_min, e_max):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.rate = rate
        self.encounters = encounters
        self.e_min = e_min
        self.e_max = e_max

    def on_tick(self, time=None, frame_time=None):
        self.game.m_map.local_encounter_rate = self.rate
        self.game.m_map.local_encounters = self.encounters
        self.game.m_map.local_encounter_level_min = self.e_min
        self.game.m_map.local_encounter_level_max = self.e_max
        return True

    def on_read(self):
        return None
