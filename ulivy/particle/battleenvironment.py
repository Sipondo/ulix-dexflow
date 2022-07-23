from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Mesh, RenderContext, BindTexture, Rectangle
from kivy.core.window import Window
from kivy.core.image import Image
import os

# from kivy.lang import Builder
from kivy.resources import resource_find, resource_add_path


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
    def __init__(self, **kwargs):
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

        pth = os.path.join(
            "resources", "essentials", "graphics", "pokemon_anim"  # , "back"
        )
        resource_add_path(pth)
        self.add_widget(
            b := BattleBattlerImage(
                # texture_file=Image(resource_find(f"substitute.png")),
                # texture_file=Image(resource_find(f"001.png")),
                # size_hint=(1, 1),
                # pos_hint={"center_y": 0.5, "center_x": 0.5},
            )
        )
        b.scene = scene
        b.game = scene.game
        scene.img_battler.append(b)

        self.add_widget(
            b := BattleBattlerImage(
                # texture_file=Image(resource_find(f"substitute.png")),
                # texture_file=Image(resource_find(f"001.png")),
                # size_hint=(1, 1),
                # pos_hint={"center_y": 0.5, "center_x": 0.5},
            )
        )
        b.scene = scene
        b.game = scene.game
        scene.img_battler.append(b)

    def update(self, time, frame_time):
        for child in self.children:
            child.update(time, frame_time)


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
        self.canvas.add(BindTexture(texture=self.tex1, index=1))

        self.rec1 = Rectangle(size=self.size, pos=self.pos)
        self.canvas.add(self.rec1)

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
    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            fs=battler_shader_fs, gs=battler_shader_gs, vs=battler_shader_vs
        )

        self.texture_file = None
        self.face = 0
        self.ratio = 0.0
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
        self.bind_texture()

    def set_face(self, face):
        if self.face == face:
            return
        self.face = face
        self.bind_texture()

    def bind_texture(self):
        if self.texture_file is not None:
            back = 0 if self.face % 3 else 1
            self.ratio = self.texture_file[back].width / self.texture_file[back].height
            self.canvas["Size"] = (self.texture_file[1].height / 4) ** 0.5
            self.canvas["AnimationLength"] = self.ratio
            self.canvas["HeightShare"] = 1.0
            self.canvas["Mirror"] = float(-1 if self.face % 2 else 1)

            self.tex1 = self.texture_file[back].texture
            self.tex1.mag_filter = "nearest"

            self.canvas.clear()
            self.canvas.add(BindTexture(texture=self.tex1, index=4))
            self.canvas.add(self.mesh)

    def redraw(self):
        self.canvas["Texture"] = 4

    def update(self, time, dt):
        self.redraw()
