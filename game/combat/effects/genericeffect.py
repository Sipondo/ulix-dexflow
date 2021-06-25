from .baseeffect import BaseEffect


class GenericEffect(BaseEffect):
    def __init__(self, scene, message, particle="", particle_miss=False):
        super().__init__(scene)
        self.spd_on_action = 100
        self.message = message
        self.particle = particle
        self.particle_miss = particle_miss

    def __repr__(self):
        return "MessageEffect: " + self.message

    def on_action(self):
        self.scene.board.no_skip(self.message, particle=self.particle, particle_miss=self.particle_miss)
        return True, False, False
