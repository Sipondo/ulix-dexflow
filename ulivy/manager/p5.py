from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Mesh, RenderContext
from kivy.clock import Clock

from ulivy.particle.p5system import ParticleSystem


class ParticleManager:
    def __init__(self, game):
        self.battle = None
        self.game = game
        self.systems = []
        self.step_quantity = 24  # TODO: 240
        self.step_size = 1 / self.step_quantity

        self.floats = 16
        self.stride = self.floats * 4

        self.fast_forward = False

        self.vbo_object_emit = ParticleHolder(self.game)
        self.game.m_vis.add_widget(self.vbo_object_emit)
        self.vbo_emit = self.vbo_object_emit.mesh

        self.vbo_objects = []
        self.vbos = []

        for _ in range(8):
            vbo_object = ParticleHolder(self.game)
            self.vbo_objects.append(vbo_object)
            # self.game.m_vis.add_widget(vbo_object)
            self.vbos.append(vbo_object.mesh)
        # self.vbo_objectA = ShaderWidget(self.game, poffset=-0.25)
        # self.game.add_widget(self.vbo_objectA)
        # self.mesh1 = self.vbo_objectA.mesh

        # self.vbo_objectB = ShaderWidget(self.game, poffset=0.25)
        # self.game.add_widget(self.vbo_objectB)
        # self.mesh2 = self.vbo_objectB.mesh

        # self.vbo_emit = ShaderWidget(self.game, poffset=-0.5)
        # self.game.add_widget(self.vbo_emit)
        # self.mesh_emit = self.vbo_emit.mesh

    def on_tick(self, time, frame_time):  # , alpha_target, anti_target):
        # self.alpha_target = alpha_target
        # self.anti_target = anti_target
        busy = False

        marked = []
        for system in self.systems:
            succes = system.on_tick(time, frame_time)
            busy = busy or succes
            if not succes:
                marked.append(system)

        for system in marked:
            self.systems.remove(system)
            self.game.m_gst.current_state.scene.environment.remove_widget(system)
            for v in self.vbo_objects:
                # self.game.m_vis.remove_widget(v)
                system.remove_widget(v)
            system.delete_parts()
            del system
        return busy

    def set_render(self, t):
        return
        if t == 1:
            self.battle.solid_offscreen.use()
            self.battle.solid_offscreen.depth_mask = True
            self.ctx.disable(moderngl.BLEND)
            self.ctx.enable(moderngl.CULL_FACE | moderngl.DEPTH_TEST | moderngl.BLEND)
            return
        if t == 2:
            self.battle.alpha_offscreen.use()
            self.ctx.enable(moderngl.BLEND | moderngl.DEPTH_TEST | moderngl.CULL_FACE)
            self.ctx.blend_func = moderngl.ADDITIVE_BLENDING
            self.ctx.blend_equation = moderngl.FUNC_ADD
            self.alpha_target.depth_mask = False
            return
        if t == 3:
            self.game.offscreen.use()
            self.game.offscreen.depth_mask = True
            self.alpha_target.depth_mask = True
            self.anti_target.depth_mask = True
            self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)
            self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
            self.ctx.blend_equation = moderngl.FUNC_ADD
            return
        if t == 4:
            self.battle.anti_offscreen.use()
            self.ctx.enable(moderngl.BLEND | moderngl.DEPTH_TEST | moderngl.CULL_FACE)
            self.ctx.blend_func = moderngl.ADDITIVE_BLENDING
            self.ctx.blend_equation = moderngl.FUNC_ADD
            self.anti_target.depth_mask = False
            return

    def spawn_system(self, brender, fname, target, miss, move_data):
        if target:
            self.systems.append(
                n := ParticleSystem(self.game, brender, fname, target, miss, move_data)
            )
            for v in self.vbo_objects:
                # self.game.m_vis.remove_widget(v)
                n.add_widget(v)
            self.game.m_gst.current_state.scene.environment.add_widget(n)

    def vao_def(self, buffer=None, render=False):
        return [
            (b"in_pos", 4, "float"),
            (b"in_vel", 3, "float"),
            (b"in_size", 1, "float"),
            (b"in_color", 3, "float"),
            (b"in_rot", 1, "float"),
            (b"in_rot_vel", 1, "float"),
            (b"in_lifespan", 1, "float"),
            (b"in_noise", 1, "float"),
            (b"in_key", 1, "float"),
        ]

    def vao_emit_def(self, buffer=None, render=False):
        return [
            (b"in_index", 1, "float"),
        ]

    def get_varyings(render=False):
        return [
            "out_pos",
            "out_vel",
            "out_size",
            "out_color",
            "out_rot",
            "out_rot_vel",
            "out_lifespan",
            "out_noise",
            "out_key",
        ]


from kivy.resources import resource_find

with open(resource_find("ulivy_shaders/tfeed_vs.glsl")) as file:
    placeholder_shader_vs = file.read()

with open(resource_find("ulivy_shaders/tfeed_fs.glsl")) as file:
    placeholder_shader_fs = file.read()

MAX_PARTICLES = 2048


class ParticleHolder(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        self.canvas = RenderContext(fs=placeholder_shader_fs, vs=placeholder_shader_vs)

        super(ParticleHolder, self).__init__(**kwargs)

        fmt = [
            (b"in_pos", 4, "float"),
            (b"in_vel", 3, "float"),
            (b"in_size", 1, "float"),
            (b"in_color", 3, "float"),
            (b"in_rot", 1, "float"),
            (b"in_rot_vel", 1, "float"),
            (b"in_lifespan", 1, "float"),
            (b"in_noise", 1, "float"),
            (b"in_key", 1, "float"),
        ]

        with self.canvas:
            self.mesh = Mesh(
                vertices=[1.0, 1.0, 1.0, 1.0] * 4 * MAX_PARTICLES,
                indices=list(range(MAX_PARTICLES)),
                fmt=fmt,
            )

    def update(self, time=None, dt=None):
        return

    #     Clock.schedule_once(self.de_register, 2)  # TODO: remove this terrible hack

    # def de_register(self, *largs):
    #     # filthy hack... TODO: remove, not sure if this is even required
    #     self.game.remove_widget(self)
