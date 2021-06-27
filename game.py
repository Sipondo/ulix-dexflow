import moderngl_window as mglw
import moderngl

from moderngl_window import geometry
from pathlib import Path

from game.renderer.audiorenderer import AudioRenderer
from game.renderer.interfacerenderer import InterfaceRenderer

from game.renderer.entityrenderer import EntityRenderer
from game.renderer.worldrenderer import WorldRenderer
from game.renderer.pantool import PanTool

from game.manager.gamestatemanager import GameStateManager
from game.manager.resourcemanager import ResourceManager
from game.manager.animationmanager import AnimationManager
from game.manager.collisionmanager import CollisionManager

from game.manager.dbmanager import DbManager
from game.manager.pbsmanager import PbsManager
from game.manager.hotkeymanager import HotkeyManager
from game.manager.entitymanager import EntityManager

from game.manager.eventmanager import EventManager
from game.manager.actionmanager import ActionManager
from game.manager.regionmanager import RegionManager

from game.manager.aimanager import AiManager
from game.manager.cameramanager import CameraManager

# Swap these to get new/old particles
from game.manager.p4 import ParticleManager

# from game.manager.particlemanager import ParticleManager


from game.manager.mapmanager import MapManager
from game.manager.savemanager import SaveManager

from game.player.inventory import Inventory

import logging


SIZE_X = 320
if SIZE_X % 16:
    SIZE_X -= SIZE_X % 16
    print(f"SIZE_X not divisible by 16, reverting to: {SIZE_X}")
SIZE_Y = int(SIZE_X / 16 * 9)
print(f"SIZE: {SIZE_X}x{SIZE_Y}, {SIZE_X/16}x{SIZE_Y/16}")


class PokeGame(mglw.WindowConfig):
    title = "Ulix Dexflow"
    fullscreen = False
    vsync = False
    resource_dir = (Path(__file__) / "../").absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        [print(x, y) for x, y in self.ctx.info.items()]
        logger = logging.getLogger("moderngl_window")
        logger.setLevel(logging.WARNING)
        self.size = (SIZE_X, SIZE_Y)

        self.resolution_render = (1920, 1280)
        self.resolution_interface_width = 1280
        self.resolution_combat_particles = (320, 180)

        # Map
        self.m_res = ResourceManager(self, self.ctx)
        self.m_res.init_noise()

        # TODO
        self.m_sav = SaveManager(self)
        self.m_map = MapManager(self)
        self.m_map.load_world_data()
        # Top level renderers
        self.r_aud = AudioRenderer(self)
        self.r_ent = EntityRenderer(self, self.ctx)
        self.r_int = InterfaceRenderer(self, self.ctx)
        self.r_wld = WorldRenderer(self, self.ctx)

        self.pan_tool = PanTool(self.size)
        # TODO
        self.r_wld.offset = (0.5, 13 / 16)

        # Top level managers
        self.m_ani = AnimationManager(self)
        self.m_ari = AiManager(self)
        self.m_act = ActionManager(self)
        self.m_cam = CameraManager(self)
        self.m_col = CollisionManager(self)
        self.m_dat = DbManager(self)
        self.m_pbs = PbsManager(self)
        self.m_ent = EntityManager(self)
        self.m_evt = EventManager(self)
        self.m_gst = GameStateManager(self)
        self.m_key = HotkeyManager(self)
        self.m_par = ParticleManager(self)

        # TODO: maybe move to savemanager
        self.inventory = Inventory(self)
        self.m_ent.load_entities()

        self.query = self.ctx.query(primitives=True)

        # Keystates
        self.from_locking = False
        self.maphack = False

        # Rendering
        self.render_prog = self.m_res.get_program("texture")
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
        self.r_wld.set_map_via_manager(self.m_sav.load("current_offset") or (0, 0))
        # Start game
        # self.m_gst.switch_state("intro")

        self.m_res.init_types()

        if self.particle is not None:
            self.m_gst.switch_state("battle")
            self.m_gst.current_state.particle_test = self.particle
        else:
            self.m_gst.switch_state("intro")
        # TODO: TEMP, start rendering
        self.render_start = False

    def render(self, time, frame_time):
        frame_time = min(2, max(0.0001, frame_time))

        # TODO: Substitute hacky render block
        if self.render_start or ((time > 0.3) and (frame_time > 0.001)):

            if not self.render_start:
                self.render_start = True
                frame_time = 0.01

            """
            Rendering pipeline:
            Game State ->
            (Battle Renderer) ->
            CPU Renderer ->
            GPU Renderer ->
            Game Renderer
            """
            # Render the scene to offscreen buffer
            self.offscreen.clear()
            self.offscreen.use()

            locking = self.m_gst.current_state.on_tick(time, frame_time)
            self.r_aud.on_tick(time, frame_time)

            # TODO
            self.ctx.disable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
            self.ctx.enable(moderngl.BLEND)
            self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
            self.ctx.blend_equation = moderngl.FUNC_ADD
            self.pan_tool.on_tick(time, frame_time)
            self.r_ent.pan(self.pan_tool.pan_value, self.pan_tool.zoom_value)
            self.r_wld.render(time, frame_time, locking=locking)

        self.r_int.update()

        # Activate the window as the render target
        self.ctx.screen.use()

        # Render offscreen diffuse layer to screen
        self.offscreen_diffuse.use(location=0)
        self.quad_fs.render(self.render_prog)

        self.m_sav.render(time, frame_time)

    def key_event(self, key, action, modifiers):
        self.m_key.key_event(key, action, modifiers)


from moderngl_window.context.base import WindowConfig, BaseWindow
from moderngl_window.timers.clock import Timer
from moderngl_window.conf import settings
from moderngl_window.utils.module_loading import import_string
from typing import List, Type


__version__ = "2.3.0"

IGNORE_DIRS = [
    "__pycache__",
    "base",
]

# Add new windows classes here to be recognized by the command line option --window
WINDOW_CLASSES = [
    "glfw",
    "headless",
    "pygame2",
    "pyglet",
    "pyqt5",
    "pyside2",
    "sdl2",
    "tk",
]

OPTIONS_TRUE = ["yes", "on", "true", "t", "y", "1"]
OPTIONS_FALSE = ["no", "off", "false", "f", "n", "0"]
OPTIONS_ALL = OPTIONS_TRUE + OPTIONS_FALSE

# Quick and dirty debug logging setup by default
# See: https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial
logger = logging.getLogger(__name__)


def run_window_custom(
    config_cls: WindowConfig, timer=None, args=None, parser=None
) -> None:
    """
    Run an WindowConfig entering a blocking main loop

    Args:
        config_cls: The WindowConfig class to render
    Keyword Args:
        timer: A custom timer instance
        args: Override sys.args
    """
    mglw.setup_basic_logging(config_cls.log_level)
    parser = parser
    config_cls.add_arguments(parser)
    values = mglw.parse_args(args=args, parser=parser)
    config_cls.argv = values
    window_cls = mglw.get_local_window_cls(values.window)

    # Calculate window size
    size = values.size or config_cls.window_size
    size = int(size[0] * values.size_mult), int(size[1] * values.size_mult)

    # Resolve cursor
    show_cursor = values.cursor
    if show_cursor is None:
        show_cursor = config_cls.cursor

    window = window_cls(
        title=config_cls.title,
        size=size,
        fullscreen=config_cls.fullscreen or values.fullscreen,
        resizable=values.resizable
        if values.resizable is not None
        else config_cls.resizable,
        gl_version=config_cls.gl_version,
        aspect_ratio=config_cls.aspect_ratio,
        vsync=values.vsync if values.vsync is not None else config_cls.vsync,
        samples=values.samples if values.samples is not None else config_cls.samples,
        cursor=show_cursor if show_cursor is not None else True,
    )
    window.print_context_info()

    config_cls.particle = values.particle

    mglw.activate_context(window=window)
    timer = timer or Timer()
    window.config = config_cls(ctx=window.ctx, wnd=window, timer=timer)

    # Swap buffers once before staring the main loop.
    # This can trigged additional resize events reporting
    # a more accurate buffer size
    window.swap_buffers()
    window.set_default_viewport()

    timer.start()

    while not window.is_closing:
        current_time, delta = timer.next_frame()

        if window.config.clear_color is not None:
            window.clear(*window.config.clear_color)

        # Always bind the window framebuffer before calling render
        window.use()

        window.render(current_time, delta)
        if not window.is_closing:
            window.swap_buffers()

    _, duration = timer.stop()
    window.destroy()
    if duration > 0:
        logger.info(
            "Duration: {0:.2f}s @ {1:.2f} FPS".format(
                duration, window.frames / duration
            )
        )


if __name__ == "__main__":
    parser = mglw.create_parser()
    parser.add_argument("--particle", help="If testing particle, particle name")
    run_window_custom(PokeGame, parser=parser)
