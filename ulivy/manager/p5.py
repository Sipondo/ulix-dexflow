from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Mesh, RenderContext
from kivy.clock import Clock

from ulivy.particle.p5system import ParticleSystem


class ParticleManager:
    def __init__(self, game):
        self.battle = None
        self.game = game
        self.systems = []
        self.step_quantity = 240
        self.step_size = 1 / self.step_quantity

        self.floats = 16
        self.stride = self.floats * 4

        self.fast_forward = False

        self.vbo_objectA = ShaderWidget(
            self.game, poffset=-0.25
        )  # ParticleVBO(self.game)
        self.game.add_widget(self.vbo_objectA)
        self.mesh1 = self.vbo_objectA.mesh

        self.vbo_objectB = ShaderWidget(
            self.game, poffset=0.25
        )  # ParticleVBO(self.game)
        self.game.add_widget(self.vbo_objectB)
        self.mesh2 = self.vbo_objectB.mesh

        self.vbo_emit = ShaderWidget(self.game, poffset=-0.5)  # EmitVBO(self.game)
        self.game.add_widget(self.vbo_emit)
        self.mesh_emit = self.vbo_emit.mesh

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
                ParticleSystem(self.game, brender, fname, target, miss, move_data)
            )

    def vao_def(self, buffer=None, render=False):
        # if render:
        #     return (
        #         buffer,
        #         "4f 3f 1f 3f 1f 1x4 1x4 1f 1x4",
        #         "in_pos",
        #         "in_vel",
        #         "in_size",
        #         "in_color",
        #         "in_rot",
        #         "in_noise",
        #     )
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
        # return [
        #     (b"inVec", 4, "float"),
        # ]
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

        #         return [
        #     ("out_pos", 4, "float"),
        #     ("out_vel", 3, "float"),
        #     ("out_size", 1, "float"),
        #     ("out_color", 3, "float"),
        #     ("out_rot", 1, "float"),
        #     ("out_rot_vel", 1, "float"),
        #     ("out_lifespan", 1, "float"),
        #     ("out_noise", 1, "float"),
        #     ("out_key", 1, "float"),
        # ]


class ParticleVBO(FloatLayout):
    def __init__(self, game, **kwargs):
        self.canvas = RenderContext()
        self.game = game

        super(ParticleVBO, self).__init__(**kwargs)

        with self.canvas:
            self.mesh = Mesh(
                vertices=[1.0] * 10 * 1024 * 12,
                indices=[],
                fmt=[(b"aPos", 2, "float"), (b"aSize", 2, "float"),],
            )

        # Clock.schedule_once(self.de_register, 10)

    def de_register(self, *largs):
        # filthy hack... TODO: remove, not sure if this is even required
        self.game.remove_widget(self)


class EmitVBO(FloatLayout):
    def __init__(self, game, **kwargs):
        self.canvas = RenderContext()
        self.game = game

        super(EmitVBO, self).__init__(**kwargs)

        with self.canvas:
            self.mesh = Mesh(
                vertices=[1.0] * 10 * 1024,
                indices=[],
                fmt=[(b"aPos", 2, "float"), (b"aSize", 2, "float"),],
            )

        # Clock.schedule_once(self.de_register, 10)

    def de_register(self, *largs):
        # filthy hack... TODO: remove, not sure if this is even required
        self.game.remove_widget(self)


from kivy.core.image import Image, ImageData
from kivy.resources import resource_find
from kivy.graphics import Mesh, MeshView, RenderContext, BindTexture, Rectangle

with open(resource_find("ulivy_shaders/tfeed_vs.glsl")) as file:
    enti_shader_vs = file.read()

with open(resource_find("ulivy_shaders/tfeed_gs.glsl")) as file:
    enti_shader_gs = file.read()

with open(resource_find("ulivy_shaders/tfeed_fs.glsl")) as file:
    enti_shader_fs = file.read()


class ShaderWidget(FloatLayout):
    def __init__(self, game, poffset, **kwargs):
        self.game = game
        self.canvas = RenderContext(
            fs=enti_shader_fs, gs=enti_shader_gs, vs=enti_shader_vs
        )

        # self.tex1 = Image.load(resource_find("tex4.jpg")).texture
        self.tex2 = Image.load(resource_find("tex2.jpg")).texture

        # self.tex1.mag_filter = "nearest"

        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(ShaderWidget, self).__init__(**kwargs)

        self.poffset = poffset
        self.camera_position = 0

        self.float_x = 0
        self.float_y = 0

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
                vertices=[1.0, 1.0, 1.0, 1.0] * 1024 * 3 * 12,
                indices=[0],  # , 1, 2, 3],
                fmt=fmt,  # [(b"aPos", 2, "float"), (b"aSize", 2, "float"),],
            )
            # self.mesh_clone = MeshView(host_mesh=self.mesh)

        self.canvas.add(BindTexture(texture=self.tex2, index=3,))

        # if poffset != -0.25:
        #     Clock.schedule_interval(self.update, 10 / 60.0)
        # else:
        Clock.schedule_once(self.update)
        Clock.schedule_once(self.de_register, 3)  # TODO: remove this terrible hack

    def update(self, *largs):

        self.float_x += 0.001
        # self.mesh.vertices = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

        # self.mesh.indices = self.mesh.indices

        self.canvas["texture0"] = 3
        self.canvas["poffset"] = float(self.poffset)
        # print("mesh", dir(self.mesh))
        # print(self.mesh_clone)

    def de_register(self, *largs):
        # filthy hack... TODO: remove, not sure if this is even required
        self.game.remove_widget(self)
