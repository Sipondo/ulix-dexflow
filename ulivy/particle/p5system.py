# import moderngl
from .p5dyna.equation import Equation
from numpy.random import random
from kivy.graphics.instructions import TransformFeedback
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Mesh, MeshView, RenderContext, BindTexture, Rectangle
from kivy.core.image import Image, ImageData

from kivy.graphics.transformation import Matrix
import numpy as np


class ParticleSystem(FloatLayout):
    def __init__(self, game, brender, fname, target, miss, move_data, **kwargs):
        self.game = game

        super(ParticleSystem, self).__init__(**kwargs)

        self.brender = brender  # meh
        self.N = 500000
        self.particles = 0
        self.fname = fname
        self.target = target
        self.miss = miss
        self.move_data = move_data

        # TODO: convert to proper change
        self.basis = (-1.0, 1.0, 1.0) if self.target[0] == 0 else (1.0, 1.0, 1.0)
        print("Target:", self.target, self.basis)

        # TODO: temp
        self.time_alive = -0.6

        self.step_count = self.time_alive
        self.warp = 1
        self.step_warp = 1
        self.step_size = self.game.m_par.step_size * self.step_warp

        self.detonate = 10

        self.emitters = []
        self.renderers = []
        self.miscs = []
        self.equations = {}
        self.transformer = None
        self.load_context_objects()
        self.spawn_elements()

    def update(self, time=None, dt=None):
        return

    def on_tick(self, time, frame_time):
        # print("PARTICLE TICK A")

        frame_time *= self.warp * (3 if self.game.m_par.fast_forward else 1)
        self.step_size = self.game.m_par.step_size * self.step_warp

        if (not self.particles) and self.time_alive > 0.5:
            if self.detonate > 9:
                self.detonate = 0.3
            else:
                self.detonate -= frame_time
            if self.detonate < 0:
                return False
        # print("PARTICLE TICK B")

        for eq in self.equations.values():
            eq.reset_eval()

        self.time_alive += frame_time
        time = self.time_alive

        self.step_count += frame_time
        steps = 0
        if self.step_count > self.step_size:
            # # Matrix
            # self.warp = max(0.1, self.warp * 0.995)
            # self.step_warp = self.warp

            steps = int(self.step_count // self.step_size)
            self.step_count = self.step_count % self.step_size

            for _ in range(steps):
                self.transformer.render(time, self.step_size)
                for emitter in self.emitters:
                    emitter.render(time, self.step_size)
                for renderer in self.renderers:
                    renderer.set_multi_opacity(0.14, self.vboa_index)
                self.switch_buffers()

        for misc in self.miscs:
            misc.render(time)
        self.render(time, frame_time)

        # print(time)
        # if steps:
        #     self.switch_buffers()
        return True

    def render(self, time, frame_time):
        # return
        # Solid
        self.game.m_par.set_render(1)
        for renderer in (x for x in self.renderers if x.equation == 1):
            renderer.render(time, frame_time)

        # return
        # Alpha
        self.game.m_par.set_render(2)
        for renderer in (x for x in self.renderers if x.equation == 2):
            renderer.render(time, frame_time)

        # Anti
        self.game.m_par.set_render(4)
        for renderer in (x for x in self.renderers if x.equation == 3):
            renderer.render(time, frame_time)

        self.game.m_par.set_render(3)

    def r(self, owner, name, parse=True, throw=True):
        name = f"field_{name}"
        if name in owner.params:
            v = owner.params[name]
            if parse and "!" in str(v):
                return self.p(v)
            elif "?" in str(v):
                return v.replace("?key?", "key")
            return v
        if throw:
            raise UnboundLocalError(f"Entry is missing named: {name}.")
        return "0"

    def switch_buffers(self):
        self.vboa_index = self.vbob_index
        self.vbob_index = (self.vbob_index + 1) % len(self.vbos)
        return
        self.vbo1, self.vbo2 = self.vbo2, self.vbo1

        for renderer in self.renderers:
            renderer.switch_buffers()

        # self.transformer.switch_buffers()

        # err = self.game.ctx.error
        # if err != "GL_NO_ERROR":
        #     print(err)

    def delete_parts(self):
        for r in self.renderers:
            r.delete_parts()

    def load_context_objects(self):
        self.vbo_object_emit = ParticleHolder(self.game)
        self.add_widget(self.vbo_object_emit)
        self.vbo_emit = self.vbo_object_emit.mesh

        self.vbo_objects = []
        self.vbos = []
        self.vboa_index = 0
        self.vbob_index = 1
        for _ in range(8):
            vbo_object = ParticleHolder(self.game)
            self.vbo_objects.append(vbo_object)
            self.add_widget(vbo_object)
            self.vbos.append(vbo_object.mesh)

        # self.vbo_objectA = ParticleHolder(self.game)
        # self.add_widget(self.vbo_objectA)
        # self.vbo1 = self.vbo_objectA.mesh

        # self.vbo_objectB = ParticleHolder(self.game)
        # self.add_widget(self.vbo_objectB)
        # self.vbo2 = self.vbo_objectB.mesh

        # self.vbo1 = self.game.m_par.vbo_objectA.mesh
        # self.vbo2 = self.game.m_par.vbo_objectB.mesh
        # self.vbo_emit = self.game.m_par.vbo_emit.mesh

    @property
    def vbo1(self):
        return self.vbos[self.vboa_index]

    @property
    def vbo2(self):
        return self.vbos[self.vbob_index]

    def spawn_elements(self):
        js = self.game.m_res.get_particle(self.fname, self.move_data)
        self.transformer = Transformer(self.game, self)

        stage_dict = {}
        for node in js["nodes"]:
            if node["title"] == "Stage":
                stage = node["content"]["field_stage"]
                for output in node["outputs"]:
                    stage_dict[output["id"]] = stage

        filters = set()
        for node in js["nodes"]:
            if node["title"][:6].lower() == "filter":
                for output in node["outputs"]:
                    filters.add(output["id"])

        filters = list(filters)

        filter_edge_dict = {}
        for edge in js["edges"]:
            if edge["start"] in filters:
                filter_edge_dict[edge["end"]] = edge["start"]
            if edge["end"] in filters:
                filter_edge_dict[edge["start"]] = edge["end"]

        edge_dict = {}
        for edge in js["edges"]:
            if edge["start"] in stage_dict.keys():
                edge_dict[edge["end"]] = stage_dict[edge["start"]]
            if edge["end"] in stage_dict.keys():
                edge_dict[edge["start"]] = stage_dict[edge["end"]]

        for i, letter in enumerate("xyz"):
            self.equations[f"user_{letter}"] = Equation(
                self,
                f"user_{letter}",
                f"self.system.brender.get_loc_fighter({1 if self.target[0] == 0 else 0}, {self.basis})[{i}]",
            )
            self.equations[f"target_{letter}"] = Equation(
                self,
                f"target_{letter}",
                f"self.system.brender.get_loc_fighter({0 if self.target[0] == 0 else 1}, {self.basis})[{i}]",
            )

        for node in js["nodes"]:
            if node["title"] == "Equation":
                # print(node["title"])
                self.add_equation(node)

        for node in js["nodes"]:
            # print(node)
            if node["title"] == "Emit":
                # print(node["title"])
                stage = int(edge_dict[node["inputs"][0]["id"]])
                self.emitters.append(Emitter(self.game, self, node, stage))
            elif node["title"] == "Trigger":
                # print(node["title"])
                self.miscs.append(Trigger(self.game, self, node))
            elif node["title"] == "Actor":
                # print(node["title"])
                self.miscs.append(Actor(self.game, self, node))
            elif node["title"] == "Camera":
                # print(node["title"])
                self.miscs.append(Camera(self.game, self, node))
            elif node["title"] == "Equation":
                pass
            elif node["title"] == "Render":
                # print(node["title"])
                stage = int(edge_dict[node["inputs"][0]["id"]])
                self.renderers.append(Renderer(self.game, self, node, stage))

        for node in js["nodes"]:
            if node["title"].lower()[:3] == "geo":
                # print("geo")
                # print(node["title"])
                id = node["inputs"][0]["id"]
                if id in edge_dict:
                    # print("stagebound")
                    stage = int(edge_dict[id])
                    self.transformer.add_geoblock(node, None, stage)
                else:
                    # print("filterbound")
                    filter = int(filter_edge_dict[id])
                    self.transformer.add_geoblock(node, filter, None)

        for node in js["nodes"]:
            if node["title"][:6].lower() == "filter":
                # print(node["title"])
                # print(node["inputs"])
                stage_in = int(
                    edge_dict[
                        [x for x in node["inputs"] if x["socket_type"] == 3][0]["id"]
                    ]
                )
                stage_out = int(
                    edge_dict[
                        [x for x in node["inputs"] if x["socket_type"] == 0][0]["id"]
                    ]
                )
                self.transformer.add_geoblock(node, None, stage_in, stage_out)

        self.transformer.load_programs()
        # self.transformer.load_context_objects()

        if len(self.emitters) < 1:
            self.time_alive = 0.4  # nothing to show, clear quickly

    def add_equation(self, params):
        self.params = params["content"]  # meh
        self.equations[self.r(self, "label")] = Equation(
            self,
            self.r(self, "label", parse=False),
            self.r(self, "equation", parse=False),
        )

    def p(self, q, parse=True):
        if "!" in q:
            for key, value in self.equations.items():
                if f"!{key}!" in q:
                    q = q.replace(f"!{key}!", str(value.get(self.time_alive)))
        if parse:
            return eval(q)
        return q


from kivy.core.image import Image, ImageData
from kivy.resources import resource_find
from kivy.graphics import Mesh, MeshView, RenderContext, BindTexture, Rectangle

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


class Emitter:
    def __init__(self, game, system, params, stage):
        self.game = game
        self.system = system
        self.N = self.system.N
        self.params = params["content"]
        self.title = "Emitter"
        self.stage = stage

        self.emit_want = 0

        self.counters = 0
        self.alive = True

        self.load_programs()
        self.load_context_objects()
        self.set_fields()

    def set_fields(self):
        self.delay = float(self.system.r(self, "delay"))
        self.emit_count = float(self.system.r(self, "count"))
        self.duration = float(self.system.r(self, "duration"))

        self.prog_emit["Stage"] = float(self.stage)
        self.prog_emit["Position"] = (
            float(self.system.r(self, "pos_x"))
            + float(self.system.r(self, "vel_x")) / 45,
            float(self.system.r(self, "pos_y"))
            + float(self.system.r(self, "vel_y")) / 45,
            float(self.system.r(self, "pos_z"))
            + float(self.system.r(self, "vel_z")) / 45,
        )

        self.prog_emit["Position_sway"] = (
            float(self.system.r(self, "pos_range_x"))
            + float(self.system.r(self, "vel_x")) / 45,
            float(self.system.r(self, "pos_range_y"))
            + float(self.system.r(self, "vel_y")) / 45,
            float(self.system.r(self, "pos_range_z"))
            + float(self.system.r(self, "vel_z")) / 45,
        )

        self.prog_emit["Position_radial"] = 0

        self.prog_emit["Velocity"] = (
            float(self.system.r(self, "vel_x")),
            float(self.system.r(self, "vel_y")),
            float(self.system.r(self, "vel_z")),
        )

        self.prog_emit["Velocity_sway"] = (
            float(self.system.r(self, "vel_range_x")),
            float(self.system.r(self, "vel_range_y")),
            float(self.system.r(self, "vel_range_z")),
        )

        self.prog_emit["Velocity_radial"] = 0

        self.prog_emit["Size"] = float(self.system.r(self, "size"))
        self.prog_emit["Size_sway"] = float(self.system.r(self, "size_range"))

        self.prog_emit["Colour"] = (
            float(self.system.r(self, "col_r")),
            float(self.system.r(self, "col_g")),
            float(self.system.r(self, "col_b")),
        )

        self.prog_emit["Colour_sway"] = (
            float(self.system.r(self, "col_range_r")),
            float(self.system.r(self, "col_range_g")),
            float(self.system.r(self, "col_range_b")),
        )

        self.prog_emit["Rotation"] = float(self.system.r(self, "rot"))
        self.prog_emit["Rotation_sway"] = float(self.system.r(self, "rot_range"))

        self.prog_emit["Rotation_velocity"] = float(self.system.r(self, "rot_vel"))
        self.prog_emit["Rotation_velocity_sway"] = float(
            self.system.r(self, "rot_vel_range")
        )

        self.prog_emit["Life"] = float(self.system.r(self, "life"))
        self.prog_emit["Life_sway"] = float(self.system.r(self, "life_range"))

    def on_tick(self, time, frame_time):
        return self.render(time, frame_time)

    def on_exit(self):
        pass

    def load_programs(self):
        print("Program Emit!")
        vs = self.game.m_res.get_shader("p5_emit_vs")
        gs = self.game.m_res.get_shader("p5_emit_gs")
        # print(vs)
        print(self.game.m_par.vao_emit_def())

        self.prog_emit = TransformFeedback(
            vs=vs,
            gs=gs,
            max_primitives=1,
            in_format=self.game.m_par.vao_emit_def(),
            out_varyings=self.game.m_par.get_varyings(),
        )
        # self.prog_emit = self.game.m_res.get_program_varyings(
        #     "p4_emit_ver", varyings=self.game.m_par.get_varyings(),
        # )

    def load_context_objects(self):
        return
        # self.widget = self.system.vbo_emit
        # self.vao_emit = self.widget.mesh

    def render(self, time, frame_time):
        self.set_fields()
        emit_count = 0
        self.counters += frame_time
        # self.active_particles = 0
        if self.delay < self.counters < self.delay + self.duration:
            self.emit_want += self.emit_count * frame_time
            emit_count = int(min(self.N - self.system.particles, self.emit_want))
            if emit_count > 0:  # and not int(time * 6) % 10:
                self.emit_want -= emit_count
                self.prog_emit["time"] = max(time, 0) + random() / 50

                # print("EMITTING:", emit_count, self.system.vbo2)
                testvalue = self.prog_emit.transform(
                    self.system.vbo_emit,
                    self.system.vbo2,
                    emit_count,
                    out_size=self.game.m_par.floats,
                    offset=self.system.particles * self.game.m_par.stride,
                    # debug=2,
                )
                self.system.particles += testvalue
                # print(
                #     testvalue,
                #     "|",
                #     self.system.particles,
                #     len(self.system.vbo2.indices),
                #     "in play",
                #     "with stride",
                #     self.game.m_par.stride,
                # )
                # exit()

                # exit()
                # with self.game.query:
                #     self.vao_emit.transform(
                #         self.system.vbo2,
                #         vertices=emit_count,
                #         buffer_offset=self.system.particles * self.game.m_par.stride,
                #     )
                # # print(self.system.particles, emit_count, self.game.query.primitives)
                # self.system.particles += self.game.query.primitives
                # print(self.system.particles)
            # print(
            #     f"Emitting on {self.counters} for {frame_time}, {emit_count} particles {self.active_particles}."
            # )`


class Renderer:
    def __init__(self, game, system, params, stage):
        self.game = game
        self.system = system
        self.N = self.system.N
        self.params = params["content"]
        self.stage = stage
        self.title = "Renderer"

        eqname = self.system.r(self, "equation").strip().lower()

        self.equation = 1 if eqname == "solid" else 3 if eqname == "anti" else 2

        # TODO: temp
        self.texture = self.game.m_res.get_texture(
            "particle", self.system.r(self, "file")
        )

        self.load_programs()
        self.load_context_objects()
        self.set_fields()

        self.step_quantity = self.game.m_par.step_quantity

        # TODO TEMP
        self.texture_noise = self.game.m_res.get_noise()
        self.prog["Size"] = 1.0
        self.prog["Stage"] = float(stage)
        self.prog["Basis"] = self.system.basis

        self.vao_receive_dict = {}
        self.buffer_requests = []
        self.current_active_buffer = 1

        # self.prog["texture0"] = 0
        self.prog["texturearray1"] = 10
        self.prog["Usenoise"] = float(self.equation != 1)
        self.prog["step_count"] = self.system.step_count

        self.rotvel = int(bool(self.system.r(self, "rotvel")))
        self.noise_speed = 0
        self.noise_id = 0

    def set_multi_opacity(self, amount, fresh):
        self.widget.multi_opacity -= amount
        self.widget.multi_opacity[self.widget.multi_opacity < 0] = 0.0
        self.widget.multi_opacity[fresh] = 1.0

    def set_fields(self):
        self.opacity = float(self.system.r(self, "opacity"))
        self.noise_speed = float(self.system.r(self, "noise"))

    def delete_parts(self):
        vis = self.game.m_gst.current_state.scene.environment.visuals

        # Solid
        if self.equation == 1:
            vis.solid_offscreen.fbo_remove_widget(self.widget)
        # Alpha
        if self.equation == 2:
            vis.alpha_offscreen.fbo_remove_widget(self.widget)

        del self.widget

    def load_programs(self):
        print("Program Renderer!")
        # Renders particle to the screen
        vs = self.game.m_res.get_shader("p5_render_vs")
        gs = self.game.m_res.get_shader("p5_render_gs")
        fs = self.game.m_res.get_shader("p5_render_fs")
        # print(vs, gs, fs)
        self.widget = RenderWidget(
            self.game,
            self.system,
            texture=self.texture,
            vs=vs,
            gs=gs,
            fs=fs,
            fmt=self.game.m_par.vao_def(),
        )
        # self.widget.canvas.add(BindTexture(texture=self.texture, index=7,))

        self.prog = self.widget.canvas

        # TODO: move
        # self.system.add_widget(self.widget)

        # TODO: change
        vis = self.game.m_gst.current_state.scene.environment.visuals

        # Solid
        if self.equation == 1:
            vis.solid_offscreen.fbo_add_widget(self.widget)
        # Alpha
        if self.equation == 2:
            vis.alpha_offscreen.fbo_add_widget(self.widget)
        # # Anti
        # if self.equation == 3:
        #     vis.anti_offscreen.add_widget(self.widget)

    def load_context_objects(self):
        return
        # Render vaos. The render to screen version of the tranform vaos above
        # self.vao1_rend = self.game.ctx.vertex_array(
        #     self.prog, [self.game.m_par.vao_def(self.system.vbo1, render=True)],
        # )
        # self.vao2_rend = self.game.ctx.vertex_array(
        #     self.prog, [self.game.m_par.vao_def(self.system.vbo2, render=True)],
        # )

    def render(self, time, frame_time):
        self.set_fields()
        self.prog["CameraPosition"] = self.game.m_cam.pos
        self.noise_id = (
            time * self.step_quantity * 2 * self.noise_speed
        ) % 5680  # 710 * 8
        self.prog["noise_id"] = float(self.noise_id // 8)

        # TODO: make native
        m = Matrix()
        m.set(array=(self.game.m_cam.bill_rot).astype("f4").tolist())
        self.prog["BillboardFace"] = m

        m2 = Matrix()
        m2.set(array=(self.game.m_cam.mvp).astype("f4").tolist())
        self.prog["projection"] = m2
        self.prog["texture0"] = 7

        self.emit_gpu(time, frame_time)

    def switch_buffers(self):
        return
        self.widget.mesh.gbatch = self.system.vbo2.gbatch
        return
        self.vao1_rend, self.vao2_rend = self.vao2_rend, self.vao1_rend

    def emit_gpu(self, time, frame_time):
        self.prog["step_count"] = self.system.step_count
        self.widget.opacity = self.opacity  # self.prog["opacity"]
        self.prog["Usenoise"] = float((self.equation != 1) and (self.noise_speed != 0))
        self.prog["Rotvel"] = int(self.rotvel)

        # print(self.widget.mesh.indices)
        # self.texture.use(0)
        # self.texture_noise.use(10)
        # self.vao1_rend.render(moderngl.POINTS, vertices=self.system.particles)


from kivy.graphics.instructions import Callback

from kivy.graphics.opengl import (
    glBlendFunc,
    glBlendFuncSeparate,
    glBlendEquation,
    glEnable,
    glDisable,
    glDepthMask,
    GL_DEPTH_TEST,
    GL_BLEND,
    GL_CULL_FACE,
    GL_SRC_ALPHA,
    GL_ONE,
    GL_ZERO,
    GL_SRC_COLOR,
    GL_ONE_MINUS_SRC_COLOR,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_DST_ALPHA,
    GL_ONE_MINUS_DST_ALPHA,
    GL_DST_COLOR,
    GL_ONE_MINUS_DST_COLOR,
    GL_FUNC_ADD,
    GL_FUNC_SUBTRACT,
    GL_FUNC_REVERSE_SUBTRACT,
)


class RenderWidget(FloatLayout):
    def __init__(self, game, system, texture, vs, gs, fs, fmt, **kwargs):
        self.game = game
        self.system = system
        self.canvas = RenderContext(fs=fs, gs=gs, vs=vs)
        self.texture = texture

        super(RenderWidget, self).__init__(**kwargs)

        self.multi_opacity = np.zeros(10, dtype=float)
        self.opacity = 1.0
        self.opacity_index = 0
        # with self.canvas:
        #     self.mesh = MeshView(host_mesh=self.system.vbo2, fmt=fmt)

        with self.canvas:
            Callback(self._set_blend_func)
            BindTexture(
                texture=self.texture, index=7,
            )
            for i, v in enumerate(self.system.vbos):
                Callback(self._set_opacity)
                self.mesh = MeshView(host_mesh=v, fmt=fmt)
            Callback(self._reset_blend_func)

    def _set_blend_func(self, instruction):
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glBlendFunc(GL_ONE, GL_ONE)
        glBlendEquation(GL_FUNC_ADD)
        glDepthMask(False)
        self.opacity_index = 0

    def _reset_blend_func(self, instruction):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glDepthMask(True)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquation(GL_FUNC_ADD)

    def _set_opacity(self, instruction):
        self.canvas["opacity"] = float(
            self.multi_opacity[self.opacity_index] * self.opacity
        )
        # print(
        #     self.multi_opacity[self.opacity_index],
        #     self.opacity,
        #     float(self.multi_opacity[self.opacity_index] * self.opacity),
        # )
        self.opacity_index += 1

    def update(self, time=None, dt=None):
        return


class Transformer:
    def __init__(self, game, system):
        self.game = game
        self.system = system
        self.geo_declarations = set(["\n"])
        self.geo_code = ""
        self.geo_target = {}
        self.uniforms = set()

    def add_geoblock(self, params, target_filter, stage_in, stage_out=None):
        title = (
            params["title"].strip().lower().replace(" ", "_")
            if "filter" in params["title"].lower()
            else params["title"][4:].strip().lower().replace(" ", "_")
        )
        block = self.game.m_res.get_geoblock(title)

        self.params = params["content"]

        constants = block.split("// CONSTANTS")[1].split("// CONSTANTS_END")[0].strip()
        dict_block = {}

        if stage_out is not None:
            dict_block["%TARGET_STAGE%"] = f"{stage_out}."  # str(stage_out)

        for line in constants.split("\n"):
            if line[:5] == "// --":
                continue

            perc_parts = line.split("%")
            typ = perc_parts[0]
            varn = perc_parts[1]

            if typ in ("float",):
                typ_val = str(self.r(varn))
                # typ_val = typ_val if "." in typ_val else f"{typ_val}."
                dict_block[f"%{varn}%"] = typ_val
            if typ in ("int",):
                dict_block[f"%{varn}%"] = str(self.r(varn))
            if typ in ("bool",):
                dict_block[f"%{varn}%"] = "true" if self.r(varn, t="b") else "false"
            if typ == "vec3":
                dict_block[
                    f"%{varn}%"
                ] = f"""vec3{str((str(self.r(f"{varn}_X")), str(self.r(f"{varn}_Y")), str(self.r(f"{varn}_Z")))).replace("'","")}"""

        geo_declarations, geo_code = block.split("// DECLARATIONS_END")

        if stage_in is not None:
            # geo_code = "\n".join([f"\nif(pos.a=={stage_in}.)", "{", geo_code, "}"])
            geo_code = "\n".join(
                [
                    f"\n\n\nif((pos.a>={stage_in-1}.)&&(pos.a<={stage_in+1}.))",
                    "{",
                    geo_code,
                    "}",
                ]
            )

        geo_declarations = set(
            [
                f"{x.strip()};"
                for x in geo_declarations.split("// DECLARATIONS")[-1].split(";")
                if x.strip()
            ]
        )

        for k, v in dict_block.items():
            geo_code = geo_code.replace(k, v)

        self.geo_declarations = self.geo_declarations | geo_declarations

        if stage_out is not None:
            # is filter
            if params["outputs"][0]["id"] in self.geo_target:
                geo_code = geo_code.replace(
                    r"%GEOBLOCKS%", self.geo_target[params["outputs"][0]["id"]]
                )
            else:
                geo_code = geo_code.replace(r"%GEOBLOCKS%", "")
            # print(geo_code)

        if target_filter is not None:
            # print("I HAVE A FILTER")
            self.geo_target[target_filter] = geo_code
        else:
            # print("I HAVE NO FILTER")
            self.geo_code += geo_code

    def r(self, query, t="f"):
        # print("\n", query)
        unparsed = self.system.r(self, query, parse=False)
        # print(query, unparsed)
        if not isinstance(unparsed, bool) and "!" in unparsed:
            for key in self.system.equations.keys():
                if f"!{key}!" in unparsed:
                    unparsed = unparsed.replace(f"!{key}!", f"UNI_{key}")
                    self.uniforms.add(key)

            # key = f"UNI_{len(self.uniforms)}"
            # self.uniforms[key] = unparsed
            # if t == "f":
            #     if not "." in str(unparsed):
            #         return f"({unparsed}.)"
            return f"({unparsed})"

        if t == "b":
            result = self.system.r(self, query)
            return bool(result)

        if t == "f":
            if not "." in str(unparsed):
                return f"({unparsed}.)"
        return f"({unparsed})"

    def on_tick(self, time, frame_time):
        return self.render(time, frame_time)

    def load_programs(self):
        # print("\n".join(self.geo_declarations) + self.geo_code)

        vs, gs = self.game.m_res.get_shader_geoblocks(
            "p5_transform_vs",
            "p5_transform_gs",
            geoblocks="\n".join(self.geo_declarations) + self.geo_code,
            uniforms="\n".join(
                [f"uniform float UNI_{x};" for x in self.system.equations.keys()]
            ),
        )

        # gs = self.game.m_res.get_shader("p5_transform_fake_gs")
        print("Program Transform!")
        # print(vs, gs)

        # with open("interpreted_transform_vs.glsl", "w") as file:
        #     file.write(vs)

        # with open("interpreted_transform_gs.glsl", "w") as file:
        #     file.write(gs)

        self.prog_trans = TransformFeedback(
            vs=vs,
            gs=gs,
            max_primitives=4,
            in_format=self.game.m_par.vao_def(),
            out_varyings=self.game.m_par.get_varyings(),
        )

        # self.prog_trans = self.game.m_res.get_program_varyings(
        #     "p4_transform_ver",
        #     "p4_transform_geo",
        #     geoblocks="\n".join(self.geo_declarations) + self.geo_code,
        #     uniforms="\n".join(
        #         [f"uniform float UNI_{x};" for x in self.system.equations.keys()]
        #     ),
        #     varyings=self.game.m_par.get_varyings(),
        # )

    def render(self, time, frame_time):
        self.emit_gpu(time, frame_time)
        return

    def emit_gpu(self, time, frame_time):
        for key in self.uniforms:
            self.prog_trans[f"UNI_{key}"] = self.system.p(f"!{key}!")

        self.prog_trans["StepSize"] = self.system.step_size
        self.prog_trans["time"] = max(time, 0)
        # Transform all particle recoding how many elements were emitted by geometry shader

        # TODO: removes errors but breaks rendering
        # if int(self.system.particles) < 1:
        #     return

        # print("TRANSFORMING!", self.system.vbo2)
        self.system.particles = self.prog_trans.transform(
            self.system.vbo1,
            self.system.vbo2,
            int(self.system.particles),
            out_size=self.game.m_par.floats,
            # debug=2,
        )
        # print(
        #     # self.system.step_size,
        #     self.system.particles,
        #     len(self.system.vbo2.indices),
        #     "transformed",
        #     "with stride",
        #     self.game.m_par.stride,
        # )

        # Transform all particle recoding how many elements were emitted by geometry shader
        # with self.game.query:
        #     self.vao1_trans.transform(
        #         self.system.vbo2, moderngl.POINTS, vertices=self.system.particles
        #     )

        # self.system.particles = self.game.query.primitives


class Trigger:
    def __init__(self, game, system, params):
        self.game = game
        self.system = system
        self.N = self.system.N
        self.params = params["content"]
        self.title = "Trigger"
        self.sound = str(self.system.r(self, "sound_path"))
        self.game.r_aud.cache_effect(self.sound)

        self.emit_want = 0
        self.last_time = self.system.time_alive

        self.counters = 0
        self.alive = True
        self.set_fields()

    def set_fields(self):
        self.duration = float(self.system.r(self, "duration"))
        self.emit_count = float(self.system.r(self, "count"))
        self.delay = float(self.system.r(self, "delay"))
        self.hit = float(self.system.r(self, "hit"))
        self.hit_enabled = bool(self.system.r(self, "hit_enabled"))
        self.sound_enabled = bool(self.system.r(self, "sound_enabled"))
        self.shake = float(self.system.r(self, "shake"))
        self.shake_enabled = bool(self.system.r(self, "shake_enabled"))

        self.dark_enabled = bool(self.system.r(self, "dark_enabled"))
        self.dark_recover = bool(self.system.r(self, "dark_recover"))
        self.dark = float(self.system.r(self, "dark"))

        self.dark_speed = float(self.system.r(self, "dark_speed"))
        self.dark_speed_enabled = bool(self.system.r(self, "dark_speed_enabled"))

    def on_tick(self, time, frame_time):
        return self.render(time, frame_time)

    def on_exit(self):
        pass

    def render(self, time):
        self.set_fields()
        emit_count = 0
        # self.active_particles = 0
        if self.delay < time < self.delay + self.duration:
            self.emit_want += self.emit_count * (time - self.last_time)
            emit_count = int(self.emit_want + 1)
            if emit_count > 0:  # and not int(time * 6) % 10:
                self.emit_want -= emit_count
                self.game.r_aud.play_effect(self.sound)

                if self.dark_enabled:
                    self.system.brender.set_dark(
                        self.dark,
                        self.dark_speed if self.dark_speed_enabled else None,
                        self.dark_recover,
                    )
                if self.shake_enabled:
                    self.system.brender.battle_shake = self.shake
        self.last_time = time


class Actor:
    def __init__(self, game, system, params):
        self.game = game
        self.system = system
        self.N = self.system.N
        self.params = params["content"]
        self.title = "Trigger"

        self.emit_want = 0
        self.last_time = self.system.time_alive

        self.fired = False
        self.counters = 0
        self.alive = True
        self.set_fields()

    def set_fields(self):
        self.duration = float(self.system.r(self, "duration"))
        self.continuous = bool(self.system.r(self, "continuous"))
        self.delay = float(self.system.r(self, "delay"))

        self.user_enabled = bool(self.system.r(self, "user_enabled"))
        self.user_recover = bool(self.system.r(self, "user_recover"))
        self.user = (
            float(self.system.r(self, "user_x")),
            float(self.system.r(self, "user_y")),
            float(self.system.r(self, "user_z")),
        )

        self.user_speed = float(self.system.r(self, "user_speed"))
        self.user_speed_enabled = bool(self.system.r(self, "user_speed_enabled"))

        self.target_enabled = bool(self.system.r(self, "target_enabled"))
        self.target_recover = bool(self.system.r(self, "target_recover"))
        self.target = (
            float(self.system.r(self, "target_x")),
            float(self.system.r(self, "target_y")),
            float(self.system.r(self, "target_z")),
        )

        self.target_speed = float(self.system.r(self, "target_speed"))
        self.target_speed_enabled = bool(self.system.r(self, "target_speed_enabled"))

    def on_tick(self, time, frame_time):
        return self.render(time, frame_time)

    def on_exit(self):
        pass

    def render(self, time):
        self.set_fields()
        emit_count = 0
        # self.active_particles = 0
        if self.delay < time < self.delay + self.duration:
            if self.continuous or not self.fired:
                self.fired = True
                if self.user_enabled:
                    self.system.brender.set_movement(
                        1 if self.system.target[0] == 0 else 0,
                        (
                            self.user[0] * self.system.basis[0],
                            self.user[1] * self.system.basis[1],
                            self.user[2] * self.system.basis[2],
                        ),
                        self.user_speed if self.user_speed_enabled else None,
                        self.user_recover,
                    )

                if self.target_enabled:
                    self.system.brender.set_movement(
                        0 if self.system.target[0] == 0 else 1,
                        (
                            self.target[0] * self.system.basis[0],
                            self.target[1] * self.system.basis[1],
                            self.target[2] * self.system.basis[2],
                        ),
                        self.target_speed if self.target_speed_enabled else None,
                        self.target_recover,
                    )
        self.last_time = time


class Camera:
    def __init__(self, game, system, params):
        self.game = game
        self.system = system
        self.params = params["content"]
        self.title = "Camera"
        self.fired = False
        self.emit_want = 0
        self.last_time = self.system.time_alive

        self.counters = 0
        self.alive = True
        self.set_fields()

    def set_fields(self):
        self.duration = float(self.system.r(self, "duration"))
        self.emit_count = float(self.system.r(self, "count"))
        self.delay = float(self.system.r(self, "delay"))
        self.mirror = str(self.system.r(self, "mirror"))
        self.target = float(self.system.r(self, "target"))
        self.speed = float(self.system.r(self, "speed"))
        self.friction = float(self.system.r(self, "friction"))

        self.target = (
            (180 - self.target) % 360 if self.system.target[0] == 0 else self.target
        )

    def on_tick(self, time, frame_time):
        return self.render(time, frame_time)

    def on_exit(self):
        pass

    def render(self, time):
        self.set_fields()
        emit_count = 0
        # self.active_particles = 0
        if self.delay < time < self.delay + self.duration:
            self.emit_want += self.emit_count * (time - self.last_time)
            emit_count = int(self.emit_want + 1)
            if emit_count > 0:  # and not int(time * 6) % 10:
                self.emit_want -= emit_count
            self.game.m_cam.go_to(self.target, self.speed)


class Camrail:
    def __init__(self, game, system, params):
        self.game = game
        self.system = system
        self.params = params["content"]
        self.title = "Camera"

        self.counters = 0
        self.alive = True
        self.set_fields()

    def set_fields(self):
        self.mirror = str(self.system.r(self, "mirror"))
        self.delay = float(self.system.r(self, "delay"))
        self.target = float(self.system.r(self, "target"))
        self.speed = float(self.system.r(self, "speed"))
        self.friction = float(self.system.r(self, "friction"))

    def on_tick(self, time, frame_time):
        return self.render(time, frame_time)

    def on_exit(self):
        pass

    def render(self, time, frame_time):
        self.set_fields()
        emit_count = 0
        self.counters += frame_time
        # self.active_particles = 0
        if self.delay < self.counters < self.delay + self.duration:
            self.emit_want += self.emit_count * frame_time
            emit_count = int(self.emit_want + 1)
            if emit_count > 0:  # and not int(time * 6) % 10:
                self.emit_want -= emit_count
