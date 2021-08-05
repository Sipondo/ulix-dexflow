class Battle:
    def __init__(self, act, src, user):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.act.game.r_int.fade = True

        self.encounter_init = False

    def on_tick(self, time=None, frame_time=None):
        if time - self.init_time < 0.5:
            return False

        if not self.encounter_init:
            self.act.game.m_gst.switch_state(
                "battle", battle_type="trainer", enemy_team=self.user.team
            )
            self.encounter_init = True
            return False
        return True

    def on_read(self):
        return None
