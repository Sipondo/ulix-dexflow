from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Mesh, RenderContext, BindTexture, Rectangle
from kivy.core.window import Window
from kivy.core.image import Image
import os

# from kivy.lang import Builder
from kivy.resources import resource_find, resource_add_path

from kivy.graphics import Fbo


from kivy.graphics.instructions import Callback

from kivy.graphics.opengl import (
    glBlendFunc,
    glBlendFuncSeparate,
    glBlendEquation,
    glEnable,
    glDisable,
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

# from kivy.lang import Builder

# Builder.load_file("ulivy/particle/battleoffscreen.kv")

############## TODO: move this to some resource manager thing

with open(resource_find("ulivy_shaders/battle_parallax_fs.glsl")) as file:
    tile_shader_fs = file.read()

with open(resource_find("ulivy_shaders/battle_parallax_vs.glsl")) as file:
    tile_shader_vs = file.read()

with open(resource_find("ulivy_shaders/battle_battler_fs.glsl")) as file:
    battler_shader_fs = file.read()

with open(resource_find("ulivy_shaders/battle_battler_gs.glsl")) as file:
    battler_shader_gs = file.read()

with open(resource_find("ulivy_shaders/battle_battler_vs.glsl")) as file:
    battler_shader_vs = file.read()
#####################


class BattleEnvironment(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        super(BattleEnvironment, self).__init__(**kwargs)
        # self.init_back()

    def init_back(self, scene):
        pth = os.path.join("resources", "base", "graphics", "environments")
        resource_add_path(pth)

        print("BATTLEENV", self.pos, self.size)
        for i in range(4, -1, -1):

            self.add_widget(
                BattleEnvironmentImage(
                    texture_file=Image(resource_find(f"forest_{i}.png")),
                    size_hint=(1, 1),
                    pos_hint={"center_y": 0.5, "center_x": 0.5},
                )
            )

        self.visuals = BattleVisuals(self.game)

        self.battler_float = BattlerContainer()
        self.alpha_float = BattlerContainer()

        self.add_widget(self.battler_float)
        self.visuals.alpha_offscreen.fbo_add_widget(self.alpha_float)
        self.scene = scene
        self.enemy_first = True

        scene.img_battler.append(
            (BattleBattlerImage(scene, self.game), BattleBattlerImage(scene, self.game))
        )
        scene.img_battler.append(
            (BattleBattlerImage(scene, self.game), BattleBattlerImage(scene, self.game))
        )
        self.set_battlers()

        self.add_widget(self.visuals)

    def update(self, time, frame_time):
        for child in self.children:
            child.update(time, frame_time)

        for a in self.scene.img_battler:
            for b in a:
                b.update(time, frame_time)

    def set_battlers(self, enemy_first=False):
        if self.enemy_first == enemy_first:
            return
        self.enemy_first = enemy_first
        self.battler_float.clear_widgets()
        self.alpha_float.clear_widgets()

        if enemy_first:
            self.battler_float.add_widget(self.scene.img_battler[1][0])
            self.alpha_float.add_widget(self.scene.img_battler[1][1])

        self.battler_float.add_widget(self.scene.img_battler[0][0])
        self.alpha_float.add_widget(self.scene.img_battler[0][1])

        if not enemy_first:
            self.battler_float.add_widget(self.scene.img_battler[1][0])
            self.alpha_float.add_widget(self.scene.img_battler[1][1])


class BattlerContainer(FloatLayout):
    def update(self, time, frame_time):
        pass


class BattleEnvironmentImage(FloatLayout):
    def __init__(self, texture_file, **kwargs):
        self.canvas = RenderContext(fs=tile_shader_fs, vs=tile_shader_vs)

        self.texture_file = texture_file
        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(BattleEnvironmentImage, self).__init__(**kwargs)

        self.init_image()
        self.bind(pos=self.redraw, size=self.redraw)

    def init_image(self):
        self.tex1 = self.texture_file.texture
        self.tex1.mag_filter = "nearest"
        self.tex1.wrap = "repeat"
        self.canvas["texture0"] = 1

        with self.canvas:
            BindTexture(texture=self.tex1, index=1)
            self.rec1 = Rectangle(size=self.size, pos=self.pos)

        self.camera_position = 0

    def redraw(self, *args):
        # TODO remove
        if not hasattr(self, "game"):
            if hasattr(self, "parent"):
                self.scene = self.parent.parent
                self.game = self.scene.game
            else:
                return

        self.rec1.pos = self.pos
        self.rec1.size = self.size

        speed = self.tex1.width / self.tex1.height / 16 * 9

        self.canvas["texture0"] = 1
        self.canvas["offset"] = self.game.m_cam.parallax_rotation * speed
        self.canvas["speed"] = speed
        self.canvas["brightness"] = float(self.scene.dark)
        self.canvas["shake"] = self.game.m_cam.shake
        # This is needed for the default vertex shader.
        win_rc = Window.render_context
        self.canvas["projection_mat"] = win_rc["projection_mat"]
        self.canvas["modelview_mat"] = win_rc["modelview_mat"]
        self.canvas["frag_modelview_mat"] = win_rc["frag_modelview_mat"]

    def update(self, time=None, dt=None):
        self.redraw()


class BattleBattlerImage(FloatLayout):
    def __init__(self, game, scene, **kwargs):
        self.game = game
        self.scene = scene
        self.canvas = RenderContext(
            fs=battler_shader_fs, gs=battler_shader_gs, vs=battler_shader_vs
        )

        self.texture_file = None
        self.face = 0
        self.ratio = 0.0
        self.summon_size = 0.0
        self.summon_size_to = 1.0
        self.theight = 0.0
        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(BattleBattlerImage, self).__init__(**kwargs)

        self.camera_position = 0

        self.float_x = 0
        self.float_y = 0

        self.mesh = Mesh(vertices=[], indices=[], fmt=[(b"in_pos", 3, "float"),],)

        self.canvas["Texture"] = 4

    def set_texture(self, texture_file):
        self.texture_file = texture_file
        if texture_file is None:
            self.summon_size_to = 0.0
        else:
            self.summon_size_to = 1.0
        self.bind_texture()

    def set_face(self, face):
        if self.face == face:
            return
        self.face = face
        self.bind_texture()

    def bind_texture(self):
        if self.texture_file is not None:
            back = 0 if self.face % 3 else 1
            self.theight = self.texture_file[back].height
            self.ratio = self.texture_file[back].width / self.texture_file[back].height
            self.canvas["Size"] = ((self.theight / 4) ** 0.7) * (self.summon_size ** 3)
            self.canvas["AnimationLength"] = self.ratio
            self.canvas["HeightShare"] = 1.0
            self.canvas["Mirror"] = float(-1 if self.face % 2 else 1)

            self.tex1 = self.texture_file[back].texture
            self.tex1.mag_filter = "nearest"

            self.canvas.clear()
            self.canvas.add(Callback(set_blend_battler))
            self.canvas.add(BindTexture(texture=self.tex1, index=4))
            self.canvas.add(self.mesh)
            self.canvas.add(Callback(reset_blend))

    def redraw(self):
        self.canvas["Texture"] = 4

    def update(self, time, dt):
        if self.summon_size > self.summon_size_to:
            self.summon_size -= dt * 1.8
            if self.summon_size <= self.summon_size_to:
                self.summon_size = self.summon_size_to

        if self.summon_size < self.summon_size_to:
            self.summon_size += dt * 1.8
            if self.summon_size >= self.summon_size_to:
                self.summon_size = self.summon_size_to

        self.canvas["Size"] = ((self.theight / 4) ** 0.5) * (self.summon_size ** 3)
        self.redraw()


class BattleVisuals(FloatLayout):
    def __init__(self, game, **kwargs):
        super(BattleVisuals, self).__init__(**kwargs)

        self.game = game

        # TODO: depth buffer should be shared by these first 3
        # self.solid_offscreen = BattleOffscreen(
        #     self.game, self.game.RENDER_SIZE_PARTICLES, self, set_blend_solid
        # )
        self.alpha_offscreen = BattleOffscreen(
            self.game, self.game.RENDER_SIZE_PARTICLES, self, set_blend_alpha
        )
        # self.anti_offscreen = BattleOffscreen(
        #     self.game, self.game.RENDER_SIZE_PARTICLES
        # )

        self.final_offscreen = BattleOffscreen(
            self.game, self.game.RENDER_SIZE, self, set_blend_final
        )

        # self.final_offscreen.fbo_add_widget(self.anti_offscreen) This one has to be rendered via the negative_blend program

        # Stack building

        # Background is handled in environment

        # self.ctx.depth_func = "1"
        # self.render_pokemon(time, frame_time, cutout=False, shadow=True)
        # self.render_pokemon(time, frame_time, cutout=False)
        # self.ctx.depth_func = "<="

        # self.final_offscreen.fbo_layout.canvas.add(Callback(set_blend_solid))
        # self.final_offscreen.fbo_add_widget(self.solid_offscreen)  # should be mesh

        # self.final_offscreen.fbo_layout.canvas.add(Callback(set_blend_alpha))
        self.final_offscreen.fbo_add_widget(self.alpha_offscreen)  # should be mesh

        # self.final_offscreen.fbo_layout.canvas.add(Callback(reset_blend))
        # self.canvas.add(Callback(set_blend_anti))
        # self.final_offscreen.add_widget(self.anti_offscreen) this works differently!!!

        self.add_widget(self.final_offscreen)
        # self.canvas.add(Callback(reset_blend))

    def update(self, time=None, dt=None):
        return


with open(resource_find("ulivy_shaders/offscreen_vs.glsl")) as file:
    offscreen_shader_vs = file.read()

with open(resource_find("ulivy_shaders/offscreen_fs.glsl")) as file:
    offscreen_shader_fs = file.read()

from kivy.graphics.gl_instructions import ClearColor, ClearBuffers

# from kivy.uix.button import Button


class BattleOffscreen(FloatLayout):
    def __init__(self, game, size, parent, blend, **kwargs):
        self.game = game

        self.canvas = RenderContext(fs=offscreen_shader_fs, vs=offscreen_shader_vs)

        super(BattleOffscreen, self).__init__(**kwargs)

        self.size = size
        self.fbo_layout = FloatLayout()

        # self.fbo = Fbo(size=self.size)  # , with_depthbuffer=True)
        # parent.canvas.add(self.fbo)  # ???

        # with self.canvas.before:
        #     Callback(blend)
        with self.canvas:
            self.fbo = Fbo(size=self.size, with_depthbuffer=True)
            Callback(blend)
            # create the fbo
            Callback(self.redraw)
            BindTexture(texture=self.fbo.texture, index=1)
            self.rec1 = Rectangle(size=(self.size), pos=self.pos)
            Callback(reset_blend)

        self.fbo.texture.mag_filter = "nearest"
        self.redraw(None)
        # self.fbo.add_reload_observer(self.populate_fbo)

        with self.fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers(clear_color=True, clear_depth=True)

        canvas = self.canvas
        self.canvas = self.fbo
        self.add_widget(self.fbo_layout)
        self.canvas = canvas

    def fbo_add_widget(self, widget):
        self.fbo_layout.add_widget(widget)

    def fbo_remove_widget(self, widget):
        self.fbo_layout.remove_widget(widget)

    def fbo_clear_widgets(self):
        self.fbo_layout.clear_widgets()

    def populate_fbo(self, fbo):
        pass

    def redraw(self, instruction):
        self.rec1.pos = self.pos
        self.rec1.size = self.size

        self.canvas["texture0"] = 1

        # This is needed for the default vertex shader.
        win_rc = Window.render_context
        self.canvas["projection_mat"] = win_rc["projection_mat"]
        self.canvas["modelview_mat"] = win_rc["modelview_mat"]
        # self.canvas["frag_modelview_mat"] = win_rc["frag_modelview_mat"]


def set_blend_solid(instruction):
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation(GL_FUNC_ADD)


def set_blend_alpha(instruction):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    glBlendFunc(GL_ONE, GL_ONE)
    glBlendEquation(GL_FUNC_ADD)


def set_blend_anti(instruction):
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glBlendEquation(GL_FUNC_ADD)


def set_blend_final(instruction):
    reset_blend(None)
    glBlendFunc(GL_ONE, GL_ONE)
    glBlendEquation(GL_FUNC_ADD)


def set_blend_battler(instruction):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation(GL_FUNC_ADD)


def reset_blend(instruction):
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation(GL_FUNC_ADD)
