from pathlib import Path

# from game.renderer.audiorenderer import AudioRenderer
# # from game.renderer.qinterfacerenderer import InterfaceRenderer

# from game.renderer.entityrenderer import EntityRenderer
# from game.renderer.worldrenderer import WorldRenderer
# from game.renderer.pantool import PanTool

# from game.manager.gamestatemanager import GameStateManager
# from game.manager.resourcemanager import ResourceManager
# from game.manager.animationmanager import AnimationManager
# from game.manager.collisionmanager import CollisionManager

# # from game.manager.dbmanager import DbManager
# # from game.manager.pbsmanager import PbsManager
# from game.manager.hotkeymanager import HotkeyManager
# from game.manager.entitymanager import EntityManager

# # # from game.manager.eventmanager import EventManager
# # from game.manager.actionmanager import ActionManager

# # from game.manager.aimanager import AiManager
# # from game.manager.cameramanager import CameraManager

# # from game.upl.uplmanager import UplManager

# from game.manager.savemanager import SaveManager

# # from game.player.inventory import Inventory

import logging
import os

# from termcolor import colored


# ULIVY

from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

from ulivy.manager.actionmanager import ActionManager
from ulivy.manager.animationmanager import AnimationManager
from ulivy.manager.cameramanager import CameraManager
from ulivy.manager.collisionmanager import CollisionManager
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
from ulivy.upl.uplmanager import UplManager

from ulivy.renderer.audiorenderer import AudioRenderer
from ulivy.renderer.bufferrenderer import BufferRenderer, InterfaceBufferRenderer
from ulivy.renderer.faderenderer import FadeRenderer

from ulivy.renderer.uirenderer import UIRenderer

from ulivy.player.inventory import Inventory

# from ulivy.util.compile_world import compile_world


from kivy.utils import platform
from kivy.lang import Builder

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
        line_color=pretty_errors.RED + "> " + pretty_errors.default_config.line_color,
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

    def __init__(self, **kwargs):
        super(PokeGame, self).__init__(**kwargs)
        # Window.size = (1280, 720)

        ############## TODO: this should go to some resource manager

        from ulivy.util.fatlas import Fatlas

        atlas = Fatlas("resources/essentials/graphics/characteratlas.atlas")

        self.atlas = atlas

        ############

        self.size = Window.size

        self.m_res = ResourceManager(self)
        self.inventory = Inventory(self)

        self.m_sav = SaveManager(self)
        self.m_map = MapManager(self, False)

        self.m_pan = PanManager(self, self.size)

        self.m_ani = AnimationManager(self)
        self.m_col = CollisionManager(self)
        self.m_ent = EntityManager(self)
        self.m_act = ActionManager(self)
        self.m_gst = GameStateManager(self)
        self.m_key = HotkeyManager(self)
        self.m_pbs = PbsManager(self)
        self.m_upl = UplManager(self)
        self.m_dat = DbManager(self)
        self.m_par = ParticleManager(self)

        self.m_cam = CameraManager(self)

        self.r_aud = AudioRenderer(self)

        self.r_fbo = BufferRenderer(self)
        self.add_widget(self.r_fbo)

        self.r_fbi = InterfaceBufferRenderer(self)
        self.add_widget(self.r_fbi)

        self.r_uin = UIRenderer(self)
        self.r_fbi.fbo_add_widget(self.r_uin)

        self.r_fad = FadeRenderer(self)
        self.r_fbi.fbo_add_widget(self.r_fad)

        if platform == "android":
            self.m_osc = OscManager(self)
            self.add_widget(self.m_osc)
        else:
            self.m_osc = None

        self.add_widget(FPSCounter())

        self.maphack = False

        self.m_gst.switch_state("overworld", fade=True)
        self.m_map.set_level(self.m_map.current_level_id)
        self.time = 0
        Clock.schedule_interval(self.update, 0)

    def update(self, dt):
        dt = min(dt, 0.1)  # TODO: check if this is safe
        self.time += dt
        time = self.time

        self.r_fad.update(time, dt)
        lock = self.m_gst.update(time, dt)

        if self.r_fad.fade_done():
            self.r_uin.update(time, dt)

            if self.m_gst.current_state_name in ("cinematic", "overworld"):
                self.m_act.update(time, dt)

        self.r_fbo.update(time, dt)


class UlivyApp(App):
    def build(self):
        return PokeGame()


if __name__ == "__main__":
    # compile_world("world")
    UlivyApp().run()
