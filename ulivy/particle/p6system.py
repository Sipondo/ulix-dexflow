from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.gl_instructions import ClearColor, ClearBuffers
from kivy.graphics.instructions import Callback


import ulivy.particle.seer.EffekseerCore as ec

from random import random
import math


class ParticleSystem(FloatLayout):
    def __init__(self, game, fname, target, miss, move_data, **kwargs):
        self.game = game

        super(ParticleSystem, self).__init__(**kwargs)

        self.particles = 0
        self.fname = fname
        self.target = target
        self.miss = miss
        self.move_data = move_data

        with self.canvas:
            self.cb = Callback(self.draw_seer)

        print("PRE EFFEKSEER")
        backend = ec.EffekseerBackendCore.InitializeWithOpenGL()
        print(backend)

        manager = ec.EffekseerManagerCore()
        manager.Initialize(8000)
        print(manager)

        effects = ec.EffekseerEffectCore()
        print(effects)

        folder = "resources/light/assets/"

        # with open("assets/Laser03.efkefc", "rb") as file:
        # with open(f"{folder}LightningStrike.efkefc", "rb") as file:
        # with open(f"{folder}Flame.efkefc", "rb") as file:
        # with open(f"{folder}RampMap.efkefc", "rb") as file:
        with open(f"{folder}Light.efkefc", "rb") as file:
            # with open(f"{folder}snowstorm11.efkefc", "rb") as file:
            # with open(f"{folder}ForceFieldTornado.efkefc", "rb") as file:
            contents = file.read()
        effects.Load(contents, len(contents), 1.0)

        # Textures
        textypes = (
            ec.EffekseerTextureType_Color,
            ec.EffekseerTextureType_Normal,
            ec.EffekseerTextureType_Distortion,
        )
        for textype in textypes:
            count = effects.GetTextureCount(textype)
            print("textures", textype, count)
            for i in range(count):
                p = effects.GetTexturePath(i, textype)

                print(p)

                with open(f"{folder}{p}", "rb") as file:
                    contents = file.read()
                effects.LoadTexture(contents, len(contents), i, textype)

        # Models
        count = effects.GetModelCount()
        print("models", count)
        for i in range(count):
            p = effects.GetModelPath(i)

            print(p)

            with open(f"{folder}{p}", "rb") as file:
                contents = file.read()
            effects.LoadModel(contents, len(contents), i)

        # Materials
        count = effects.GetMaterialCount()
        print("materials", count)
        for i in range(count):
            p = effects.GetMaterialPath(i)

            print(p)

            with open(f"{folder}{p}", "rb") as file:
                contents = file.read()
            effects.LoadMaterial(contents, len(contents), i)

        # Models
        count = effects.GetCurveCount()
        print("models", count)
        for i in range(count):
            p = effects.GetCurvePath(i)

            print(p)

            with open(f"{folder}{p}", "rb") as file:
                contents = file.read()
            effects.LoadCurve(contents, len(contents), i)

        print(effects)
        print("POST EFFEKSEER")

        self.manager = manager
        self.effects = effects
        self.handle = None
        self.time = 0.0
        self.frame_time = 0.0
        self.prevtime = 0.0
        self.time_since = 0.0

        # TODO: remove, temp dark
        self.game.m_gst.current_state.scene.set_dark(0, 1.0, False)

        self.sound = r"C:\dev\projects\pokejets\simple_ulix\resources\light\assets\light_sound.mp3"
        self.sound_preload = self.game.r_aud.get_effect_preload(self.sound)
        self.sound_preload.play()

        self.camera_step = 0

    def on_tick(self, time, frame_time):
        self.update(time, frame_time)

    def update(self, time, frame_time):
        self.time = time
        self.frame_time = frame_time

    def draw_seer(self, instr):

        t = self.time

        delta = self.frame_time

        if self.time_since == 0.0:
            self.handle = self.manager.Play(self.effects)
            print("handle!", self.handle, 0.01 * t)

            self.manager.SetEffectPosition(self.handle, -20.0, 0.0, 0.0)  # t / 6.0)

            rot = math.pi * 0.5
            self.manager.SetEffectRotation(self.handle, rot, rot, rot)  # ?

            scale = 1.0
            self.manager.SetEffectScale(self.handle, scale, scale, scale)

        self.time_since += delta

        self.do_light_move(self.time)

        if self.time_since > 45.0:  # 2.0:
            self.time_since = 0.0
            self.camera_step = 0

        ClearColor(0, 0, 0, 1)
        ClearBuffers(clear_depth=True)

        self.manager.SetViewProjectionMatrixWithSimpleWindow(1920, 1080)

        self.manager.SetProjectionMatrix(
            *[float(y) for x in list(map(list, zip(*self.game.m_cam.proj))) for y in x]
        )

        self.manager.SetCameraMatrix(
            *[
                float(y)
                for x in list(
                    map(list, zip(*(self.game.m_cam.lookat * self.game.m_cam.rotate)))
                )
                for y in x
            ]
        )

        self.manager.Update(delta * 60)
        self.manager.DrawBack()
        self.manager.DrawFront()

    def do_light_move(self, time):

        # self.game.m_gst.current_state.scene.set_movement(
        #     0, (20.0, 0.0, math.sin(time)), None, False
        # )
        self.game.m_gst.current_state.scene.set_movement(
            0,
            (
                -1.0,
                0.0,
                math.sin(self.time_since) * 0.05 + min(0.07, self.time_since / 10),
            ),
            None,
            False,
        )

        camera_want = 0

        if self.camera_step == camera_want:
            self.game.m_cam.go_to(95, 2)
            self.camera_step += 1
            self.game.m_cam.battle_shake = 0.9
            self.game.m_cam.shake_dampen = False
            return

        camera_want += 1
        if self.time_since < 3:
            return

        if self.camera_step == camera_want:
            self.game.m_cam.go_to(170, 0.4)
            self.game.m_cam.dist_to(20, 0.3)
            self.game.m_cam.battle_shake = 0.9
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 9.5:
            return

        if self.camera_step == camera_want:
            # self.game.m_cam.go_to(200, 0.5)
            self.game.m_gst.current_state.scene.set_fighter_visible(1, False)
            self.game.m_cam.go_steady(30)
            self.game.m_cam.dist_to(160, 0.12)
            # self.game.m_cam.dist_to(20, 1.5)
            # self.game.m_cam.battle_shake = 0.9
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 14:
            return

        if self.camera_step == camera_want:
            # self.game.m_cam.go_to(150, 0.15)
            # self.game.m_cam.dist_to(25, 1.5)
            # self.game.m_cam.battle_shake = 0.9
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 20.5:
            return

        if self.camera_step == camera_want:
            self.game.m_cam.go_to(170, 0.2)
            self.game.m_cam.dist_to(50, 6)
            self.game.m_cam.height_to(15, 3)
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 22:
            return

        if self.camera_step == camera_want:
            self.game.m_gst.current_state.scene.set_fighter_visible(1, False)
            # self.game.m_cam.go_to(170, 2)
            self.game.m_cam.dist_to(100, 6)
            self.game.m_cam.height_to(40, 3)
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 24.5:
            return

        if self.camera_step == camera_want:
            # self.game.m_cam.go_to(170, 2)
            self.game.m_cam.dist_to(500, 2)
            self.game.m_cam.height_to(50, 3)
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 24.7:
            return

        if self.camera_step == camera_want:
            self.game.m_gst.current_state.scene.set_fighter_visible(0, False)
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 26.0:
            return

        if self.camera_step == camera_want:
            # self.game.m_gst.current_state.scene.set_fighter_visible(0, False)
            self.game.m_gst.current_state.scene.set_fighter_visible(1, True)
            self.game.m_cam.go_set(300)
            self.game.m_cam.go_to(190, 1)
            # self.game.m_cam.go_to(70, 1)
            # self.game.m_cam.go_to(200, 1)
            self.game.m_cam.dist_set(50)
            # self.game.m_cam.dist_set(200)
            self.game.m_cam.dist_to(150, 0.5)
            self.game.m_cam.height_set(0)
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 26.5:
            return

        if self.camera_step == camera_want:
            self.game.m_cam.battle_shake = 1.0
            # self.game.m_cam.go_to(170, 2)
            # self.game.m_cam.dist_to(80, 1000)
            # self.game.m_cam.height_to(0, 1000)
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 27.5:
            return

        if self.camera_step == camera_want:
            self.game.m_cam.battle_shake = 0.7
            # self.game.m_cam.go_to(170, 2)
            # self.game.m_cam.dist_to(80, 1000)
            # self.game.m_cam.height_to(0, 1000)
            self.camera_step += 1
            return

        camera_want += 1
        if self.time_since < 28.5:
            return

        if self.camera_step == camera_want:
            self.game.m_cam.battle_shake = 0.5
            # self.game.m_cam.battle_shake = 1.0
            # self.game.m_cam.go_to(170, 2)
            # self.game.m_cam.dist_to(80, 1000)
            # self.game.m_cam.height_to(0, 1.5)
            self.game.m_cam.focus_to(300, 1.5)
            self.game.m_cam.dist_to(800, 2.5)
            self.camera_step += 1
            return
