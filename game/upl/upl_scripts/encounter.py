from numpy import array
from numpy.random import choice


class Encounter:
    def __init__(self, act, src, user, encounters):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user

        options = []
        probabilities = []
        for encounter in encounters.split("\n"):
            encounter = encounter.strip()
            occurence, name = encounter.split("x ")

            options.append(name.strip())
            probabilities.append(int(occurence.strip()))

        probabilities = array(probabilities)
        probabilities = probabilities / probabilities.sum()

        res = choice(options, p=probabilities)
        self.act.game.m_gst.switch_state("battle", enemy_team=[res])

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
