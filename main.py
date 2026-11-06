import math
import os
import struct
import zengl

from pathlib import Path
from ulix import Event
from ulix.renderer.text import DirectFontRender, FormattedText

from ulix.renderer.faderenderer import FadeRenderer
from ulix.renderer.worldrenderer import WorldRenderer

from ulix.manager.actionmanager import ActionManager
from ulix.manager.animationmanager import AnimationManager


from ulix.manager.hotkeymanager import HotkeyManager
from ulix.manager.mapmanager import MapManager
from ulix.manager.panmanager import PanManager
from ulix.manager.resourcemanager import ResourceManager
from ulix.manager.savemanager import SaveManager
from ulix.manager.gamestatemanager import GameStateManager

# from ulivy.manager.cameramanager import CameraManager
from ulix.manager.collisionmanager import CollisionManager
from ulix.manager.dbmanager import DbManager
from ulix.manager.entitymanager import EntityManager

# # from ulivy.manager.p5 import ParticleManager
# from ulivy.manager.generatormanager import GeneratorManager
# from ulivy.manager.battlemanager import BattleManager
# from ulivy.manager.mapmanager import MapManager
# from ulivy.manager.oscmanager import FPSCounter, OscManager
# from ulivy.manager.p6 import ParticleManager
# from ulivy.manager.panmanager import PanManager
from ulix.manager.pbsmanager import PbsManager
# from ulivy.manager.pluginmanager import PluginManager
# from ulivy.manager.resourcemanager import ResourceManager
# from ulivy.manager.savemanager import SaveManager
# from ulivy.manager.threadingmanager import ThreadingManager
from ulix.player.inventory import Inventory
# from ulivy.renderer.audiorenderer import AudioRenderer
# from ulivy.renderer.bufferrenderer import BufferRenderer, InterfaceBufferRenderer
# from ulivy.renderer.uirenderer import UIRenderer
# from ulivy.upl.uplmanager import UplManager


class FrameRate:
    def __init__(self, rate_window = 0.5):
        self.rate_window = rate_window
        self.frames = 0
        self.elapsed = 0.0
        self.fps = 0.0
        self.ms = 0.0

    def update(self, dt):
        self.frames += 1
        self.elapsed += dt
        if self.elapsed >= self.rate_window:
            self.fps = self.frames / self.elapsed
            self.ms = 1000.0 * self.elapsed / self.frames
            self.frames = 0
            self.elapsed = 0.0


class UlixGame():
    # RENDER_SIZE = (160, 90)
    # RENDER_SIZE = (640, 360)
    # RENDER_SIZE = (1280, 720)
    RENDER_SIZE = (1920, 1080)

    RENDER_SIZE_PARTICLES = (320, 180)
    # RENDER_SIZE_PARTICLES = (160, 90)
    # RENDER_SIZE_PARTICLES = (32, 18)
    ctx = None
    size = (1, 1) # placeholder

    def __init__(self, **kwargs):
        self.fps = FrameRate()

    def first_setup(self):
        # Window.size = (1280, 720)
        # self.m_plu = PluginManager(self)
        # self.m_plu.pre_load()
        ############## TODO: this should go to some resource manager

        from ulix.util.fatlas import Fatlas

        self.atlas = Fatlas("resources/essentials/graphics/characteratlas.atlas", self.ctx)

        # ############

        # self.grace = 0  # Encounter CD
        # self.last_visited_name = ""  # Area names

        self.m_res = ResourceManager(self)
        self.inventory = Inventory(self)

        self.m_sav = SaveManager(self)
        self.m_map = MapManager(self, False)
        # self.m_gen = GeneratorManager(self)

        self.m_pan = PanManager(self, self.size)

        self.m_ani = AnimationManager(self)
        self.m_col = CollisionManager(self)
        self.m_ent = EntityManager(self)
        self.m_act = ActionManager(self)
        self.m_gst = GameStateManager(self)
        self.m_key = HotkeyManager(self)
        self.m_pbs = PbsManager(self)
        # self.m_upl = UplManager(self)
        self.m_dat = DbManager(self)
        # self.m_thr = ThreadingManager(self)
        # self.m_bat = BattleManager(self)

        # self.m_vis = FloatLayout()
        # with self.m_vis.canvas:
        #     opacity = 0.0
        # self.add_widget(self.m_vis)
        # self.m_par = ParticleManager(self)

        # self.m_cam = CameraManager(self)

        # self.r_aud = AudioRenderer(self)
        self.r_fad = FadeRenderer(self)

        # self.r_fbo = BufferRenderer(self)
        # self.add_widget(self.r_fbo)
        self.r_wld = WorldRenderer(self)

        # self.r_fbi = InterfaceBufferRenderer(self)
        # self.add_widget(self.r_fbi)

        # self.r_uin = UIRenderer(self)
        # self.r_fbi.fbo_add_widget(self.r_uin)

        # self.r_fbi.fbo_add_widget(self.r_fad)

        # if platform == "android":
        #     self.m_osc = OscManager(self)
        #     self.add_widget(self.m_osc)
        # else:
        #     self.m_osc = None

        # # self.add_widget(FPSCounter())

        self.maphack = False

        # # for _ in range(30):
        # #     self.inventory.add_item(self.m_pbs.get_random_item().identifier, 1)

        # # TODO: temp
        # for _ in range(6):
        #     self.inventory.add_member(self.inventory.init_random_member())

        # print(self.inventory.fighter_names)

        # self.m_plu.post_load()
        # self.m_gst.switch_state("overworld", fade=True)
        self.m_gst.switch_state("overworld", fade=False) # TODO: temp
        # self.m_map.set_level(self.m_map.current_level_id)
        self.time = 0
        # Clock.schedule_interval(self.update, 0)

    # def update(self, dt):
    #     dt = min(dt, 0.1)  # TODO: check if this is safe
    #     self.time += dt
    #     time = self.time

    #     if self.m_osc is not None:
    #         self.m_osc.update(time, dt)

    #     # self.m_gen.update(time, dt)
    #     self.m_pan.update(time, dt)
    #     self.m_thr.update(time, dt)
    #     self.r_fad.update(time, dt)
    #     lock = self.m_gst.update(time, dt)

    #     if (
    #         not self.r_fad.blocking
    #         or self.r_fad.fade_done()
    #         or self.m_gst.current_state_name == "menustart"
    #     ):
    #         self.r_uin.update(time, dt)

    #         if self.m_gst.current_state_name in ("cinematic", "overworld"):
    #             self.m_act.update(time, dt)

    #     self.r_fbo.update(time, dt)
    #     self.m_sav.render(time, dt)

    # def get_application_config(self, defaultpath="./%(appname)s.sav"):
    #     from os.path import expanduser, sep`K`

    #     from kivy.utils import platform

    #     if platform == "android":
    #         # defaultpath = "/sdcard/emulated/0/.%(appname)s.sav"
    #         defaultpath = self.app.get_application_config()
    #     elif platform == "win":
    #         defaultpath = defaultpath.replace("/", sep)

    #     return os.path.expanduser(defaultpath) % {
    #         "appname": self.app.name,
    #         "appdir": self.app.directory,
    #     }

    def setup(self, ctx, size):
        if self.ctx is None:
            self.ctx = ctx
            self.first_setup()

        # Render targets
        self.image = None
        self.output = None
        self.quads = None
        self.text = None

        self.world_image = ctx.image(self.RENDER_SIZE, 'rgba8unorm')

        # Worldrenderer
        self.r_wld.setup(ctx, self.world_image)

        # Init pan on player
        self.m_pan.set_pan(self.m_ent.player.get_pos())

        # Init screen
        self.resize(size)

    def resize(self, size):
        for obj in (self.quads, self.image, self.output):
            if obj is not None:
                self.ctx.release(obj)
        if self.text is not None:
            self.text.release()

        self.size = size
        aspect = size[0] / size[1]
        self.image = self.ctx.image(size, 'rgba8unorm', samples=4)
        self.image.clear_value = (0.06, 0.06, 0.08, 1.0)

        self.output = self.ctx.image(size, 'rgba8unorm')
        self.quads = None

        self.text = DirectFontRender(self.ctx, [self.output])

    def event(self):
        self.m_key.event(event)

    def update(self, dt):
        self.time += dt
        self.fps.update(dt)

        #     dt = min(dt, 0.1)  # TODO: check if this is safe
        #     self.time += dt
        #     time = self.time

        # if self.m_osc is not None:
        #     self.m_osc.update(self.time, dt)

        # self.m_gen.update(self.time, dt)
        self.m_pan.update(self.time, dt)
        # self.m_thr.update(self.time, dt)
        # self.r_fad.update(self.time, dt)
        lock = self.m_gst.update(self.time, dt)

        #     if (
        #         not self.r_fad.blocking
        #         or self.r_fad.fade_done()
        #         or self.m_gst.current_state_name == "menustart"
        #     ):
        #         self.r_uin.update(time, dt)

        #         if self.m_gst.current_state_name in ("cinematic", "overworld"):
        #             self.m_act.update(time, dt)

        #     self.r_fbo.update(time, dt)
        #     self.m_sav.render(time, dt)

        # run/walk until gamestates are in
        if "shift" in self.m_key.pressed_keys:
            self.m_ent.player.set_movement_type(1)
        else:
            self.m_ent.player.set_movement_type(0)
        direction = self.m_key.get_movement_direction()
        if direction and not self.m_ent.player.moving:
            self.m_ent.player.start_move(direction, self.time)

        # Animations
        self.m_ani.on_tick(self.time, dt)

        # Camera
        self.m_pan.set_pan(self.m_ent.player.get_pos()) # TODO: this should be done in pan manager, not here
        self.m_pan.update(self.time, dt)

        # Render
        self.r_wld.render(self.time, dt)

        # Scale and center world_image into window
        src_w, src_h = self.world_image.size
        dst_w, dst_h = self.output.size
        scale = min(dst_w / src_w, dst_h / src_h)
        blit_w = int(src_w * scale)
        blit_h = int(src_h * scale)
        offset_x = (dst_w - blit_w) // 2
        offset_y = (dst_h - blit_h) // 2
        self.output.clear()
        self.world_image.blit(
            self.output,
            offset=(offset_x, offset_y),
            size=(blit_w, blit_h),
            filter=False,
        )

        self.output.blit()

        # unit = min(self.size) / 720 * 2
        # margin = 24 * unit
        # self.text.render_string('zengl-demo', margin, margin + 40 * unit, scale=40 * unit)
        # rate = self.fps
        # self.text.render_string(f'{rate.fps:.0f} fps  {rate.ms:.1f} ms', margin + 260 * unit, margin + 40 * unit, scale=16 * unit, color=(0.6, 0.65, 0.75), font='silkscreen')

        # DESCRIPTION = FormattedText.from_html(
        #     """This is a description of the port progress. Right now, only text rendering is working."""
        # )

        # self.text.render_multiline(DESCRIPTION, margin, margin + 80 * unit, 420 * unit, scale=20 * unit, min_sep=7 * unit, vertical_advance=26 * unit)
        # self.text.draw()

    def close(self):
        pass


import argparse
import subprocess
import sys
from pathlib import Path
from ulix.host import run

DEVELOP_WEB = Path(__file__).resolve().parent / "tools" / "develop_web.py"


def main():
    run(UlixGame())


def cli():
    parser = argparse.ArgumentParser(
        description="Run the game on the desktop, or serve it for the browser."
    )
    parser.add_argument(
        "--develop",
        action="store_true",
        help="web development mode"
        "other arguments (--host, --port) go to tools/develop_web.py",
    )
    args, rest = parser.parse_known_args()
    if not args.develop:
        if rest:
            parser.error(f'unrecognized arguments: {" ".join(rest)}')
        main()
        return
    try:
        sys.exit(subprocess.call([sys.executable, str(DEVELOP_WEB), *rest]))
    except KeyboardInterrupt:
        pass


# The browser page imports this module and calls main() itself.
if __name__ == "__main__":
    cli()
