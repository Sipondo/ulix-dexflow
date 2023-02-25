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
        effects.Load(contents, len(contents), 25.0)

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

    def on_tick(self, time, frame_time):
        self.update(time, frame_time)

    def update(self, time, frame_time):
        self.time = time
        self.frame_time = frame_time

    def draw_seer(self, instr):
        # print("Draw!")
        t = self.time
        # self.canvas["time"] = t

        delta = self.frame_time

        # print(delta)

        # self.canvas["resolution"] = list(map(float, self.size))
        # This is needed for the default vertex shader.
        # win_rc = Window.render_context
        # self.canvas["projection_mat"] = win_rc["projection_mat"]
        # self.canvas["modelview_mat"] = win_rc["modelview_mat"]
        # self.canvas["frag_modelview_mat"] = win_rc["frag_modelview_mat"]

        # if random() > 0.9:
        # if random() > 0.9:
        if self.time_since == 0.0:
            self.handle = self.manager.Play(self.effects)
            print("handle!", self.handle, 0.01 * t)
            # self.manager.SetEffectPosition(self.handle, 125.0, 300.0, 0.0)
            # self.manager.SetEffectPosition(self.handle, 400.0, 100.0, 0.0)
            # self.manager.SetEffectPosition(
            #     self.handle,
            #     (0.2 + 0.6 * random()) * 800,
            #     (0.2 + 0.6 * random()) * 600,
            #     0.0,
            # )

            self.manager.SetEffectPosition(self.handle, -20.0, 0.0, 0.0)  # t / 6.0)
            # self.manager.SetEffectRotation(
            #     self.handle, 360 * random(), 360 * random(), 360 * random()
            # )
            # self.manager.SetEffectRotation(self.handle, 0.0, 3.14 / 4, 0.0)
            # self.manager.SetEffectRotation(self.handle, 2.0 * t, 2.0 * t, 2.0 * t)
            rot = math.pi * 0.5
            self.manager.SetEffectRotation(self.handle, rot, rot, rot)  # ?
            # print("ROTATE:", t * 2.0)
            # self.manager.SetEffectRotation(self.handle, 0.2, 0.0, 0.0)
            # self.manager.SetEffectScale(self.handle, random(), random(), random())
            scale = 1.0
            self.manager.SetEffectScale(self.handle, scale, scale, scale)

            # self.manager.SetEffectTransformMatrix(
            #     self.handle,
            #     scale,
            #     0.0,
            #     0.0,
            #     0.0,
            #     0.0,
            #     scale,
            #     0.0,
            #     0.0,
            #     0.0,
            #     0.0,
            #     scale,
            #     0.0,
            # )

        self.time_since += delta

        if self.time_since > 15.0:  # 2.0:
            self.time_since = 0.0

        ClearColor(0, 0, 0, 1)
        ClearBuffers(clear_depth=True)

        self.manager.SetViewProjectionMatrixWithSimpleWindow(1920, 1080)
        # self.manager.SetViewProjectionMatrixWithSimpleWindow(800, 600)
        # self.manager.SetViewProjectionMatrixWithSimpleWindow(320, 180)
        # self.manager.SetProjectionMatrix(
        #     *[float(y) for x in self.game.m_cam.proj for y in x]
        # )
        # print(self.game.m_cam.mvp)
        # print([float(y) for x in self.game.m_cam.mvp for y in x])
        # self.manager.SetProjectionMatrix(
        #     *[float(y) for x in self.game.m_cam.mvp for y in x]
        # )
        # self.manager.SetProjectionMatrix(
        #     *[
        #         float(y)
        #         for x in list(
        #             map(list, zip(*self.game.m_cam.proj * self.game.m_cam.rotate))
        #         )
        #         for y in x
        #     ]
        # )
        self.manager.SetProjectionMatrix(
            *[float(y) for x in list(map(list, zip(*self.game.m_cam.proj))) for y in x]
        )
        # self.manager.SetCameraMatrix(
        #     *[
        #         float(y)
        #         for x in list(
        #             map(list, zip(*(self.game.m_cam.lookat * self.game.m_cam.rotate)))
        #         )
        #         for y in x
        #     ]
        # )
        self.manager.SetCameraMatrix(
            *[
                float(y)
                for x in list(
                    map(list, zip(*(self.game.m_cam.lookat * self.game.m_cam.rotate)))
                )
                for y in x
            ]
        )
        # self.manager.SetCameraMatrix(
        #     *[
        #         float(y)
        #         for x in list(map(list, zip(*(self.game.m_cam.lookat))))
        #         for y in x
        #     ]
        # )

        self.manager.Update(delta * 60)
        self.manager.DrawBack()
        self.manager.DrawFront()
