from ulivy.particle.battlemovement import BattleMovement
from ulivy.particle.battleenvironment import BattleEnvironment
import numpy as np
from array import array
from kivy.uix.floatlayout import FloatLayout

from .battlemovement import BattleMovement

from kivy.graphics.transformation import Matrix


class BattleScene(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(**kwargs)

        # Add the widget with backgrounds and battlers
        self.add_widget(b := BattleEnvironment(self.game))

        self.environment = b

        # Init battler list (size: 2)
        self.img_battler = []

        # Load backkground and add both battlers to the list
        b.init_back(self)

        print("BATTLESCENE", self.pos, self.size)

        self.bmove = BattleMovement(game, self)

        self.set_fighter_image(None, 0)
        self.set_fighter_image(None, 1)

        # self.prog = self.game.m_res.get_program("flattened_battle_entity")
        # self.prog["Texture"] = 0

        self.dark = 1.0
        self.dark_to = None
        self.dark_speed = 1.0
        self.dark_recover = True
        self.dark_direction = 1

        self.battle_shake = 1.0
        self.camera = self.game.m_cam
        self.camera.reset()

        self.brightness = [1.0, 1.0]

        self.character_offset = 20

    def update(self, time, frame_time):
        for child in self.children:
            child.update(time, frame_time)

    @property
    def location_team0(self):
        return self.bmove.t0

    @property
    def location_team1(self):
        return self.bmove.t1

    def set_fighter_image(self, spriteset, team):
        if team == 0:
            self.poke1_set = spriteset
            for b in self.img_battler[0]:
                b.set_texture(self.poke1_set)
            # self.poke1_set = self.game.m_res.prepare_battle_animset(
            #     f"{str(id).zfill(3)}"
            # )
        else:
            self.poke2_set = spriteset
            for b in self.img_battler[1]:
                b.set_texture(self.poke2_set)
            # self.poke2_set = self.game.m_res.prepare_battle_animset(
            #     f"{str(id).zfill(3)}"
            # )

    def get_loc_fighter(self, team, base):
        if team == 1:
            l = self.location_team1
        else:
            l = self.location_team0

        return (l[0] * base[0], l[1] * base[1], l[2] * base[2])

    def set_dark(self, dark, speed, recover):
        self.dark_recover = recover
        if speed is not None:
            self.dark_to = dark
            self.dark_speed = speed
            if self.dark_to > self.dark:
                self.dark_direction = 1
            else:
                self.dark_direction = -1
        else:
            self.dark_to = None
            self.dark_speed = None
            self.dark = dark

    def set_movement(self, team, position, speed, recover):
        self.bmove.set_movement(team, position, speed, recover)

    def do_particle(self, name, user, target, miss=False, move_data=None):
        if name:
            name = name.replace(" ", "-")
            if miss:
                # TODO Particles miss to left/right
                pass
            self.game.m_par.spawn_system(
                self, name, target, miss, move_data=move_data
            )  # name)
        else:
            print("Empty particle!")

    def render(self, time: float, frame_time: float):
        self.camera.render(time, frame_time)
        self.render_pokemon(time, frame_time)
        self.render_pokemon(time, frame_time, cutout=True)
        self.bmove.render(time, frame_time)

        if self.dark_to is not None:
            self.dark = max(
                self.dark + frame_time / 2 * self.dark_speed * self.dark_direction, 0
            )

            if (self.dark - self.dark_to) * self.dark_direction > 0.01:
                self.dark = self.dark_to
                self.dark_to = None

        elif self.dark_recover:
            self.dark = min(self.dark + frame_time / 2.5, 1)

        self.battle_shake = min(self.battle_shake + frame_time / 2, 1)

        # self.prog_bg["Brightness"] = self.dark
        # self.render_prog["Contrast"] = 3.0 - 2 * self.dark
        # self.render_prog_neg["Contrast"] = 3.0 - 2 * self.dark
        # self.camera.shake_value = ((1.0 - self.battle_shake) / 2) ** 3.0
        # self.prog_bg["Shake"] = 0  # self.camera.shake
        # self.render_prog["Shake"] = 0  # self.camera.shake
        # self.render_prog_neg["Shake"] = self.camera.shake
        # self.prog["Shake"] = 0  # self.camera.shake * 6  # TODO: this is a temporary fix

        # # TODO
        # """redo:
        # 1. draw background and char on screen
        # 2. draw trans char on offscreen
        # 3. draw solids on offscreen
        # 4. draw offscreen (solids) on screen
        # 5. lock depth
        # 6. reset offscreen (not resetting depth)
        # 7. draw alphas on offscreen
        # 8. draw offscreen (alphas) on screen
        # """
        # self.game.m_par.battle = self  # TODO: this is stupid

        # # Init perspective
        # self.camera.render(time, frame_time)

        # # Clear
        # self.ctx.clear()
        # self.alpha_offscreen.clear(0.0, 0.0, 0.0, 0.0)
        # self.anti_offscreen.clear(0.0, 0.0, 0.0, 0.0)
        # self.solid_offscreen.clear(0.0, 0.0, 0.0, 0.0)
        # self.final_offscreen.clear(0.0, 0.0, 0.0, 0.0)
        # self.final_offscreen.use()

        # # Render main screen base
        # self.render_background()
        # self.ctx.depth_func = "1"
        # self.render_pokemon(time, frame_time, cutout=False, shadow=True)
        # self.render_pokemon(time, frame_time, cutout=False)
        # self.ctx.depth_func = "<="

        # self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        # self.ctx.blend_equation = moderngl.FUNC_ADD

        # # Render black cutout
        # # self.solid_offscreen.use()
        # # self.render_pokemon(cutout=True)
        # self.alpha_offscreen.use()
        # self.render_pokemon(time, frame_time, cutout=True)

        # Render
        locking = self.game.m_par.on_tick(
            time, frame_time  # , self.alpha_offscreen, self.anti_offscreen
        )

        # # ### Aggregate picture
        # self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        # self.ctx.blend_equation = moderngl.FUNC_ADD
        # self.final_offscreen.use()

        # # Solid
        # self.ctx.disable(moderngl.BLEND)
        # self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        # self.solid_diffuse.use(location=0)
        # self.quad_fs.render(self.render_prog)

        # # Alpha
        # self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        # self.ctx.enable(moderngl.BLEND)
        # self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE
        # # self.ctx.blend_equation = moderngl.FUNC_SUBTRACT
        # self.alpha_diffuse.use(location=0)
        # self.quad_fs.render(self.render_prog)

        # # Anti
        # self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        # self.ctx.enable(moderngl.BLEND)
        # self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE
        # # self.ctx.blend_equation = moderngl.FUNC_SUBTRACT
        # self.anti_diffuse.use(location=1)
        # # self.quad_fs.render(self.render_prog)

        # self.game.offscreen.use()
        # self.final_diffuse.use(location=0)
        # self.render_prog_neg["Contrast"] = 1.0
        # # self.ctx.disable(moderngl.BLEND)
        # # self.ctx.blend_func = moderngl.ONE, moderngl.ONE
        # self.quad_fs.render(self.render_prog_neg)
        # self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        # self.ctx.blend_equation = moderngl.FUNC_ADD
        return locking

    def render_pokemon(self, time, frame_time, cutout=False, shadow=False):
        if not cutout:
            for i in range(len(self.brightness)):
                self.brightness[i] += 10 * frame_time * (1.0 - self.brightness[i])

        # self.img_battler.canvas["CameraPosition"] = self.game.m_cam.pos
        # self.img_battler.canvas["Cutout"] = 1 if cutout else 0
        # self.img_battler.canvas["IsShadow"] = 1 if shadow else 0
        # # self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)

        # m = Matrix()
        # m.set(array=(self.camera.bill_rot).astype("f4").tolist())
        # self.img_battler.canvas["BillboardFace"] = m

        # m2 = Matrix()
        # m2.set(array=(self.camera.mvp).astype("f4").tolist())
        # self.img_battler.canvas["Mvp"] = m2
        # print(np.dot(self.img_battler.canvas["Mvp"], np.array([0.1, 0.1, 0.1, 1])))

        enemy_first = not (int((self.camera.rotation_value + 2) % 4) % 3)
        # if self.poke2_set and enemy_first:
        #     # TODO: support >2 chars
        #     self.prog["Brightness"] = ((1.5 - self.brightness[1]) * 2) ** 1.2
        #     self.vbo_pkm.write(
        #         np.asarray(
        #             [
        #                 self.camera.pos[0]
        #                 + self.location_team1[0] * self.character_offset,
        #                 self.camera.pos[1]
        #                 + self.location_team1[1] * self.character_offset,
        #                 self.camera.pos[2]
        #                 + self.location_team1[2] * self.character_offset,
        #             ],
        #             dtype="f4",
        #         ),
        #         offset=0,
        #     )
        #     self.prog["Texture"] = 0
        #     face = int((self.camera.rotation_value + 2) % 4)
        #     l = (
        #         self.poke2_set[0 if face % 3 else 1][0].size[0]
        #         // self.poke2_set[0 if face % 3 else 1][0].size[1]
        #     )
        #     self.prog["Size"] = (
        #         self.poke2_set[0 if face % 3 else 1][0].size[1] / 4
        #     ) ** 0.5
        #     self.prog["AnimationFrame"] = int(time * 8) % l
        #     self.prog["AnimationLength"] = l
        #     self.prog["HeightShare"] = self.poke2_set[0 if face % 3 else 1][1]
        #     self.prog["Mirror"] = -1 if face % 2 else 1

        #     self.poke2_set[0 if face % 3 else 1][0].use(location=0)
        #     self.vao_pkm.render(moderngl.POINTS, vertices=1)

        if True or self.poke1_set:
            self.render_battler(0, time, cutout, shadow)
            self.render_battler(1, time, cutout, shadow)
            # self.img_battler.canvas["Brightness"] = self.brightness[0]

            # self.img_battler.mesh.vertices = [
            #     self.camera.pos[0] + self.location_team0[0] * self.character_offset,
            #     self.camera.pos[1] + self.location_team0[1] * self.character_offset,
            #     self.camera.pos[2] + self.location_team0[2] * self.character_offset,
            # ]
            # self.img_battler.mesh.indices = [0]

            # # print(self.img_battler.mesh.vertices)

            # a = []
            # b = []

            # # for i in range(10):
            # #     a.extend([i / 10, -i / 10, i / 10])
            # #     b.append(i)

            # face = int((self.camera.rotation_value) % 4)
            # # l = (
            # #     self.poke1_set[0 if face % 3 else 1][0].size[0]
            # #     // self.poke1_set[0 if face % 3 else 1][0].size[1]
            # # )
            # # self.img_battler.canvas["Size"] = (
            # #     self.poke1_set[0 if face % 3 else 1][0].size[1] / 4
            # # ) ** 0.5
            # l = 4
            # self.img_battler.canvas["Size"] = 5.0
            # self.img_battler.canvas["AnimationFrame"] = int(time * 8) % l
            # self.img_battler.canvas["AnimationLength"] = l
            # # self.img_battler.canvas["HeightShare"] = self.poke1_set[
            # #     0 if face % 3 else 1
            # # ][1]
            # self.img_battler.canvas["HeightShare"] = 1.0
            # self.img_battler.canvas["Mirror"] = -1 if face % 2 else 1

            # # self.poke1_set[0 if face % 3 else 1][0].use(location=0)
            # # self.vao_pkm.render(moderngl.POINTS, vertices=1)

        # # TODO: remove duplicate
        # if self.poke2_set and not enemy_first:
        #     # TODO: support >2 chars
        #     self.prog["Brightness"] = ((1.5 - self.brightness[1]) * 2) ** 1.2
        #     self.vbo_pkm.write(
        #         np.asarray(
        #             [
        #                 self.camera.pos[0]
        #                 + self.location_team1[0] * self.character_offset,
        #                 self.camera.pos[1]
        #                 + self.location_team1[1] * self.character_offset,
        #                 self.camera.pos[2]
        #                 + self.location_team1[2] * self.character_offset,
        #             ],
        #             dtype="f4",
        #         ),
        #         offset=0,
        #     )
        #     self.prog["Texture"] = 0
        #     face = int((self.camera.rotation_value + 2) % 4)
        #     l = (
        #         self.poke2_set[0 if face % 3 else 1][0].size[0]
        #         // self.poke2_set[0 if face % 3 else 1][0].size[1]
        #     )
        #     self.prog["Size"] = (
        #         self.poke2_set[0 if face % 3 else 1][0].size[1] / 4
        #     ) ** 0.5
        #     self.prog["AnimationFrame"] = int(time * 8) % l
        #     self.prog["AnimationLength"] = l
        #     self.prog["HeightShare"] = self.poke2_set[0 if face % 3 else 1][1]
        #     self.prog["Mirror"] = -1 if face % 2 else 1

        #     self.poke2_set[0 if face % 3 else 1][0].use(location=0)
        #     self.vao_pkm.render(moderngl.POINTS, vertices=1)

        # self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)

    def render_battler(self, i, time, cutout=False, shadow=False):
        battler = self.img_battler[i][1 if cutout else 0]
        location = self.location_team0 if i == 0 else self.location_team1

        battler.canvas["CameraPosition"] = self.game.m_cam.pos
        battler.canvas["Cutout"] = 1 if cutout else 0
        battler.canvas["IsShadow"] = 1 if shadow else 0
        # self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.BLEND)

        # TODO: make native
        m = Matrix()
        m.set(array=(self.camera.bill_rot).astype("f4").tolist())
        battler.canvas["BillboardFace"] = m

        m2 = Matrix()
        m2.set(array=(self.camera.mvp).astype("f4").tolist())
        battler.canvas["Mvp"] = m2

        battler.canvas["Brightness"] = self.brightness[0]

        battler.mesh.vertices = [
            self.camera.pos[0] + location[0] * self.character_offset,
            self.camera.pos[1] + location[1] * self.character_offset,
            self.camera.pos[2] + location[2] * self.character_offset,
        ]
        battler.mesh.indices = [0]

        # print(battler.mesh.vertices)

        a = []
        b = []

        # for i in range(10):
        #     a.extend([i / 10, -i / 10, i / 10])
        #     b.append(i)

        if i == 0:
            face = int((self.camera.rotation_value) % 4)
        else:
            face = int((self.camera.rotation_value + 2) % 4)
        # l = (
        #     self.poke1_set[0 if face % 3 else 1][0].size[0]
        #     // self.poke1_set[0 if face % 3 else 1][0].size[1]
        # )
        # battler.canvas["Size"] = (
        #     self.poke1_set[0 if face % 3 else 1][0].size[1] / 4
        # ) ** 0.5

        if battler.texture_file is not None:
            battler.set_face(face)
            # TODO: remove hack
            a = float(int(time * 8) % battler.ratio)
            battler.canvas["AnimationFrame"] = 1.0 if a < 1.0 else a
            # print(float(int(time * 8) % battler.ratio))
