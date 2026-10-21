from ulivy.particle.p6system import ParticleSystem


class ParticleManager:
    def __init__(self, game):
        self.game = game
        self.systems = []
        return

    def on_tick(self, time, frame_time):
        busy = False
        for system in self.systems:
            succes = system.on_tick(time, frame_time)
        return busy

    def set_render(self, t):
        return

    def spawn_system(self, fname, target, miss, move_data):
        # if target:
        self.systems.append(
            n := ParticleSystem(self.game, fname, target, miss, move_data)
        )
        # for v in self.vbo_objects:
        #     # self.game.m_vis.remove_widget(v)
        #     n.add_widget(v)
        # self.game.m_gst.current_state.scene.environment.add_widget(n)
        self.game.m_gst.current_state.scene.add_widget(n)
        # self.game.add_widget(n)
