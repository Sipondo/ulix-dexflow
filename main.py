from pathlib import Path

from game.renderer.audiorenderer import AudioRenderer
# from game.renderer.qinterfacerenderer import InterfaceRenderer

from game.renderer.entityrenderer import EntityRenderer
from game.renderer.worldrenderer import WorldRenderer
from game.renderer.pantool import PanTool

from game.manager.gamestatemanager import GameStateManager
from game.manager.resourcemanager import ResourceManager
from game.manager.animationmanager import AnimationManager
from game.manager.collisionmanager import CollisionManager

# from game.manager.dbmanager import DbManager
# from game.manager.pbsmanager import PbsManager
from game.manager.hotkeymanager import HotkeyManager
from game.manager.entitymanager import EntityManager

# # from game.manager.eventmanager import EventManager
# from game.manager.actionmanager import ActionManager

# from game.manager.aimanager import AiManager
# from game.manager.cameramanager import CameraManager

# from game.upl.uplmanager import UplManager

# # Swap these to get new/old particles
# from game.manager.p4 import ParticleManager

# from game.manager.particlemanager import ParticleManager


from game.manager.mapmanager import MapManager
from game.manager.savemanager import SaveManager

# from game.player.inventory import Inventory

import logging
import os

from termcolor import colored



# ULIVY

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

from game.renderer.ulivy_tilerenderer import TileRenderer
from osc.JoystickDemo import JoystickDemo
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


SIZE_X = 320
if SIZE_X % 16:
    SIZE_X -= SIZE_X % 16
    print(f"SIZE_X not divisible by 16, reverting to: {SIZE_X}")
SIZE_Y = int(SIZE_X / 16 * 9)
print(f"SIZE: {SIZE_X}x{SIZE_Y}, {SIZE_X/16}x{SIZE_Y/16}")


class PokeGame(Screen):
    def __init__(self, **kwargs):
        super(PokeGame, self).__init__(**kwargs)
        self.size = Window.size
        self.m_map = MapManager(self, False)
        self.add_widget(TileRenderer(self))

        self.joysticks = JoystickDemo()
        self.add_widget(self.joysticks)
        # self.add_widget(FPSCounter())

class NotPokeGame():
    title = "Ulix Dexflow"
    fullscreen = False
    vsync = False
    resource_dir = (Path(__file__) / "../").absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        [print(x, y) for x, y in self.ctx.info.items()]
        logger = logging.getLogger("moderngl_window")
        logger.setLevel(logging.WARNING)

        # Resources
        self.m_res = ResourceManager(self, self.ctx)
        self.m_res.init_noise()

        # Inventory, PBS & Data
        # self.inventory = Inventory(self)
        # self.m_dat = DbManager(self)
        # self.m_pbs = PbsManager(self)

        # Save & Map
        self.m_sav = SaveManager(self)
        self.m_map = MapManager(self, False)
        self.m_map.load_world_data()

        self.size = (SIZE_X, SIZE_Y)
        self.resolution_render = (1920, 1280)

        self.resolution_interface_width = 1280
        self.resolution_combat_particles = (320, 180)

        # TODO
        # self.r_int = InterfaceRenderer(self, self.ctx)
        # Top level renderers
        self.r_aud = AudioRenderer(self)
        self.r_ent = EntityRenderer(self, self.ctx)
        self.r_wld = WorldRenderer(self, self.ctx, False)

        self.m_res.init_types()
        self.pan_tool = PanTool(self.size)
        # TODO
        self.r_wld.offset = (0.5, 13 / 16)

        # Top level managers
        self.m_ani = AnimationManager(self)
        # self.m_act = ActionManager(self)
        self.m_col = CollisionManager(self)
        self.m_ent = EntityManager(self)
        self.m_gst = GameStateManager(self)
        self.m_key = HotkeyManager(self)

        self.m_sav.init_valueholders()

        self.query = self.ctx.query(primitives=True)

        # Keystates
        self.from_locking = False
        self.maphack = False

        # Rendering
        self.render_prog = self.m_res.get_program("texture_filter")
        self.render_prog["texture0"].value = 0
        self.quad_fs = geometry.quad_fs()

        # RGBA color/diffuse layer
        self.offscreen_diffuse = self.ctx.texture(self.resolution_render, 4)
        # self.offscreen_diffuse.filter = moderngl.NEAREST, moderngl.NEAREST

        # Texture for storing depth values
        self.offscreen_depth = self.ctx.depth_texture(self.resolution_render)

        # Create a framebuffer we can render to
        self.offscreen = self.ctx.framebuffer(
            color_attachments=[self.offscreen_diffuse,],
            depth_attachment=self.offscreen_depth,
        )

        # Initial map
        self.r_wld.set_map_via_manager(
            isinstance(self.m_sav.load("current_offset"), int)
            and (0, 0)
            or tuple(self.m_sav.load("current_offset"))
        )
        # Start game
        # self.m_gst.switch_state("intro")

        self.m_res.init_types()

        self.m_gst.switch_state("overworld")

        # TODO: TEMP, start rendering
        self.m_map.set_level(self.m_map.current_level_id)
        # self.render_start = False

    def render(self, time, frame_time):
        frame_time = min(2, max(0.0001, frame_time))

        """
        Rendering pipeline:
        Game State ->
        (Battle Renderer) ->
        CPU Renderer ->
        GPU Renderer ->
        Game Renderer
        """
        locking = self.m_gst.current_state.on_tick(time, frame_time)

        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.ctx.blend_equation = moderngl.FUNC_ADD
        self.pan_tool.on_tick(time, frame_time)
        self.r_ent.pan(self.pan_tool.pan_value, self.pan_tool.zoom_value)
        self.r_wld.render(time, frame_time, locking=locking)

    def key_event(self, key, action, modifiers):
        self.m_key.key_event(key, action, modifiers)

    def unicode_char_entered(self, char: str):
        self.m_key.unicode_char_entered(char)
        return super().unicode_char_entered(char)

    @property
    def render_entities_allowed(self):
        return True


if __name__ == "__main__":
    pass
    # run_window_config(PokeGame)


class UlivyApp(App):
    def build(self):
        return PokeGame()


if __name__ == "__main__":
    UlivyApp().run()
