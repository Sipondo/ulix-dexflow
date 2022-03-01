"""function
Start a battle.

Start a battle between the user of this function and the player. The enemy team is taken from the user's `team` attribute.
This function is designed for battles against NPCs. Encounters should be handled with `Encounter()` instead.

in:
No arguments

"""


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
