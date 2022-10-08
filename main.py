if __name__ == "__main__":
    from pathlib import Path

    import os
    import multiprocessing

    multiprocessing.freeze_support()

    # os.environ["KIVY_AUDIO"] = "sdl2"
    os.environ["KIVY_AUDIO"] = "android"
    # from termcolor import colored

    from kivy.config import Config

    Config.set("input", "mouse", "mouse,multitouch_on_demand")

    import logging

    # ULIVY

    from kivy.clock import Clock
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.screenmanager import Screen

    from ulivy.manager.actionmanager import ActionManager
    from ulivy.manager.animationmanager import AnimationManager
    from ulivy.manager.cameramanager import CameraManager
    from ulivy.manager.collisionmanager import CollisionManager
    from ulivy.manager.combatmanager import CombatManager
    from ulivy.manager.dbmanager import DbManager
    from ulivy.manager.entitymanager import EntityManager
    from ulivy.manager.gamestatemanager import GameStateManager
    from ulivy.manager.hotkeymanager import HotkeyManager
    from ulivy.manager.pbsmanager import PbsManager
    from ulivy.manager.mapmanager import MapManager
    from ulivy.manager.savemanager import SaveManager
    from ulivy.manager.oscmanager import OscManager, FPSCounter
    from ulivy.manager.panmanager import PanManager
    from ulivy.manager.resourcemanager import ResourceManager
    from ulivy.manager.p5 import ParticleManager
    from ulivy.manager.generatormanager import GeneratorManager
    from ulivy.upl.uplmanager import UplManager

    from ulivy.renderer.audiorenderer import AudioRenderer
    from ulivy.renderer.bufferrenderer import BufferRenderer, InterfaceBufferRenderer
    from ulivy.renderer.faderenderer import FadeRenderer

    from ulivy.renderer.uirenderer import UIRenderer

    from ulivy.player.inventory import Inventory

    # from ulivy.util.compile_world import compile_world

    from kivy.utils import platform
    from kivy.lang import Builder

    from kivy.uix.floatlayout import FloatLayout

    if platform == "android":
        from android.permissions import request_permissions, Permission

    Builder.load_file("ulivy/manager/oscmanager.kv")

    ###

    os.system("color")

    import sys

    if "pretty_errors" in sys.modules:
        import pretty_errors

        pretty_errors.configure(
            separator_character="*",
            filename_display=pretty_errors.FILENAME_EXTENDED,
            line_number_first=True,
            display_link=True,
            lines_before=5,
            lines_after=2,
            line_color=pretty_errors.RED
            + "> "
            + pretty_errors.default_config.line_color,
            code_color="  " + pretty_errors.default_config.line_color,
            truncate_code=True,
            display_locals=True,
        )

    class PokeGame(Screen):

        # RENDER_SIZE = (160, 90)
        # RENDER_SIZE = (640, 360)
        RENDER_SIZE = (1280, 720)
        # RENDER_SIZE = (1920, 1080)

        RENDER_SIZE_PARTICLES = (320, 180)
        # RENDER_SIZE_PARTICLES = (160, 90)
        # RENDER_SIZE_PARTICLES = (32, 18)

        def __init__(self, app, **kwargs):
            super(PokeGame, self).__init__(**kwargs)
            # Window.size = (1280, 720)
            self.app = app
            ############## TODO: this should go to some resource manager

            from ulivy.util.fatlas import Fatlas

            atlas = Fatlas("resources/essentials/graphics/characteratlas.atlas")

            self.atlas = atlas

            ############

            self.grace = 0  # Encounter CD
            self.last_visited_name = ""  # Area names

            self.size = Window.size

            self.m_res = ResourceManager(self)
            self.inventory = Inventory(self)

            self.m_sav = SaveManager(self)
            self.m_map = MapManager(self, False)
            self.m_gen = GeneratorManager(self)

            self.m_pan = PanManager(self, self.size)

            self.m_ani = AnimationManager(self)
            self.m_col = CollisionManager(self)
            self.m_com = CombatManager(self)
            self.m_ent = EntityManager(self)
            self.m_act = ActionManager(self)
            self.m_gst = GameStateManager(self)
            self.m_key = HotkeyManager(self)
            self.m_pbs = PbsManager(self)
            self.m_upl = UplManager(self)
            self.m_dat = DbManager(self)

            self.m_vis = FloatLayout()
            with self.m_vis.canvas:
                opacity = 0.0
            self.add_widget(self.m_vis)
            self.m_par = ParticleManager(self)

            self.m_cam = CameraManager(self)

            self.r_aud = AudioRenderer(self)
            self.r_fad = FadeRenderer(self)

            self.r_fbo = BufferRenderer(self)
            self.add_widget(self.r_fbo)

            self.r_fbi = InterfaceBufferRenderer(self)
            self.add_widget(self.r_fbi)

            self.r_uin = UIRenderer(self)
            self.r_fbi.fbo_add_widget(self.r_uin)

            self.r_fbi.fbo_add_widget(self.r_fad)

            if platform == "android":
                self.m_osc = OscManager(self)
                self.add_widget(self.m_osc)
            else:
                self.m_osc = None

            self.add_widget(FPSCounter())

            self.maphack = False

            # for _ in range(30):
            #     self.inventory.add_item(self.m_pbs.get_random_item().identifier, 1)

            self.m_gst.switch_state("menustart", fade=True)
            # self.m_map.set_level(self.m_map.current_level_id)
            self.time = 0
            Clock.schedule_interval(self.update, 0)

        def update(self, dt):
            dt = min(dt, 0.1)  # TODO: check if this is safe
            self.time += dt
            time = self.time

            if self.m_osc is not None:
                self.m_osc.update(time, dt)

            self.m_gen.update(time, dt)
            self.r_fad.update(time, dt)
            lock = self.m_gst.update(time, dt)

            if (
                not self.r_fad.blocking
                or self.r_fad.fade_done()
                or self.m_gst.current_state_name == "menustart"
            ):
                self.r_uin.update(time, dt)

                if self.m_gst.current_state_name in ("cinematic", "overworld"):
                    self.m_act.update(time, dt)

            self.r_fbo.update(time, dt)
            self.m_sav.render(time, dt)

        def get_application_config(self, defaultpath="./%(appname)s.sav"):
            from kivy.utils import platform
            from os.path import sep, expanduser

            if platform == "android":
                # defaultpath = "/sdcard/emulated/0/.%(appname)s.sav"
                defaultpath = self.app.get_application_config()
            elif platform == "win":
                defaultpath = defaultpath.replace("/", sep)

            return os.path.expanduser(defaultpath) % {
                "appname": self.app.name,
                "appdir": self.app.directory,
            }

    class UlivyApp(App):
        def build(self):
            if platform == "android":
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
            return PokeGame(self)

    # compile_world("world")
    UlivyApp().run()
