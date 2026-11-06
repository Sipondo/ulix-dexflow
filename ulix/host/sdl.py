"""desktop (Windows/macOS/Linux) and Android via python-for-android"""

import sys

import zengl

from . import _sdl2 as sdl
from .glsl import install_glsl_header
from .event import Event

IS_ANDROID = hasattr(sys, 'getandroidapilevel')


class SDLLoader:
    def load_opengl_function(self):
        return sdl.GL_GetProcAddress(name.encode()) or 0


class SDLHost:
    def __init__(self, title = 'zengl-demo', size = (960, 540), hidden = False):
        self.title = title
        self.window_size = size
        self.hidden = hidden

    def run(self, game, max_frames = None):
        sdl.check(sdl.Init(sdl.INIT_VIDEO))
        window = context = None

        # set attributes for gl versions
        try:
            if IS_ANDROID:
                sdl.GL_SetAttribute(sdl.GL_CONTEXT_PROFILE_MASK, sdl.GL_CONTEXT_PROFILE_ES)
                sdl.GL_SetAttribute(sdl.GL_CONTEXT_MAJOR_VERSION, 3)
                sdl.GL_SetAttribute(sdl.GL_CONTEXT_MINOR_VERSION, 0)
            else:
                sdl.GL_SetAttribute(sdl.GL_CONTEXT_PROFILE_MASK, sdl.GL_CONTEXT_PROFILE_CORE)
                sdl.GL_SetAttribute(sdl.GL_CONTEXT_FLAGS, sdl.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
                sdl.GL_SetAttribute(sdl.GL_CONTEXT_MAJOR_VERSION, 3)
                sdl.GL_SetAttribute(sdl.GL_CONTEXT_MINOR_VERSION, 3)
            sdl.GL_SetAttribute(sdl.GL_DOUBLEBUFFER, 1)
            sdl.GL_SetAttribute(sdl.GL_DEPTH_SIZE, 0)

            flags = sdl.WINDOW_OPENGL | sdl.WINDOW_RESIZABLE | sdl.WINDOW_ALLOW_HIGHDPI
            if self.hidden:
                flags |= sdl.WINDOW_HIDDEN
            w, h = self.window_size
            pos = sdl.WINDOWPOS_CENTERED
            window = sdl.check(sdl.CreateWindow(self.title.encode(), pos, pos, w, h, flags))
            context = sdl.check(sdl.GL_CreateContext(window))
            sdl.GL_SetSwapInterval(1)

            self._loop(window, game, max_frames)
        finally:
            game.close()
            zengl.cleanup()
            if context:
                sdl.GL_DeleteContext(context)
            if window:
                sdl.DestroyWindow(window)
            sdl.Quit()

    def _init_gl(self, window, game):
        zengl.init(SDLLoader())
        ctx = zengl.context()
        install_glsl_header(ctx)
        size = sdl.size_of(sdl.GL_GetDrawableSize, window)
        game.setup(ctx, size)
        return size

    def _loop(self, window, game, max_frames):
        size = self._init_gl(window, game)
        ctx = zengl.context()
        ev = sdl.EventBuffer()
        freq = sdl.GetPerformanceFrequency()
        last = sdl.GetPerformanceCounter()
        frames = 0

        while max_frames is None or frames < max_frames:
            while ev.poll():
                kind = ev.type
                if kind == sdl.QUIT:
                    return
                if kind == sdl.RENDER_DEVICE_RESET:
                    size = self._init_gl(window, game)
                    ctx = zengl.context()
                elif kind == sdl.WINDOWEVENT:
                    if ev.window()[0] == sdl.WINDOWEVENT_SIZE_CHANGED:
                        size = sdl.size_of(sdl.GL_GetDrawableSize, window)
                        game.resize(size)
                elif event := self._translate(ev, window, size):
                    game.event(event)

            now = sdl.GetPerformanceCounter()
            dt, last = (now - last) / freq, now

            ctx.new_frame()
            game.update(dt)
            ctx.end_frame()
            sdl.GL_SwapWindow(window)
            frames += 1

    def _translate(self, ev, window, size):
        kind = ev.type
        if kind in (sdl.KEYDOWN, sdl.KEYUP):
            repeat, sym = ev.key()
            if repeat:
                return None
            name = sdl.GetKeyName(sym).decode().lower()
            return Event('key_down' if kind == sdl.KEYDOWN else 'key_up', key=name)

        # mouse
        if kind in (sdl.MOUSEMOTION, sdl.MOUSEBUTTONDOWN, sdl.MOUSEBUTTONUP):
            if kind == sdl.MOUSEMOTION:
                which, x, y = ev.mouse_motion()
                name = 'pointer_move'
            else:
                which, button, x, y = ev.mouse_button()
                if button != 1:
                    return None
                name = 'pointer_down' if kind == sdl.MOUSEBUTTONDOWN else 'pointer_up'
            if which == sdl.TOUCH_MOUSEID:
                return None

            ww, wh = sdl.size_of(sdl.GetWindowSize, window)
            return Event(name, x=x * size[0] / ww, y=y * size[1] / wh)

        # trackpad
        if kind in (sdl.FINGERDOWN, sdl.FINGERUP, sdl.FINGERMOTION):
            touch_id, finger_id, x, y = ev.finger()

            if sdl.GetTouchDeviceType(touch_id) != sdl.TOUCH_DEVICE_DIRECT:
                return None
            name = {sdl.FINGERDOWN: 'pointer_down', sdl.FINGERUP: 'pointer_up', sdl.FINGERMOTION: 'pointer_move'}[kind]
            return Event(name, x=x * size[0], y=y * size[1], pointer=finger_id)

        return None
