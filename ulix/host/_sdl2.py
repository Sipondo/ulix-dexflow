import os
import struct
import sys
from ctypes import CDLL, byref, c_char_p, c_int, c_int64, c_uint32, c_void_p, create_string_buffer
from ctypes.util import find_library

INIT_VIDEO = 0x00000020

WINDOW_OPENGL = 0x00000002
WINDOW_HIDDEN = 0x00000008
WINDOW_RESIZABLE = 0x00000020
WINDOW_ALLOW_HIGHDPI = 0x00002000
WINDOWPOS_CENTERED = 0x2FFF0000

GL_DOUBLEBUFFER = 5
GL_DEPTH_SIZE = 6
GL_CONTEXT_MAJOR_VERSION = 17
GL_CONTEXT_MINOR_VERSION = 18
GL_CONTEXT_FLAGS = 20
GL_CONTEXT_PROFILE_MASK = 21
GL_CONTEXT_PROFILE_CORE = 0x1
GL_CONTEXT_PROFILE_ES = 0x4
GL_CONTEXT_FORWARD_COMPATIBLE_FLAG = 0x2

QUIT = 0x100
WINDOWEVENT = 0x200
KEYDOWN = 0x300
KEYUP = 0x301
MOUSEMOTION = 0x400
MOUSEBUTTONDOWN = 0x401
MOUSEBUTTONUP = 0x402
FINGERDOWN = 0x700
FINGERUP = 0x701
FINGERMOTION = 0x702
RENDER_DEVICE_RESET = 0x2001

WINDOWEVENT_SIZE_CHANGED = 6

TOUCH_MOUSEID = 0xFFFFFFFF
TOUCH_DEVICE_DIRECT = 1

EVENT_SIZE = 56


def _candidates():
    if path := os.environ.get('SDL2_LIBRARY'):
        yield path
    if hasattr(sys, 'getandroidapilevel'):
        yield 'libSDL2.so'
        return
    try:
        import sdl2dll

        dll_dir = sdl2dll.get_dllpath()
        yield os.path.join(dll_dir, 'SDL2.framework', 'Versions', 'A', 'SDL2')
        yield os.path.join(dll_dir, 'SDL2.dll')
        yield os.path.join(dll_dir, 'libSDL2-2.0.so.0')
        yield os.path.join(dll_dir, 'libSDL2-2.0.so')
    except ImportError:
        pass
    if found := find_library('SDL2') or find_library('SDL2-2.0'):
        yield found


def _load():
    for path in _candidates():
        try:
            return CDLL(path)
        except OSError:
            continue
    raise RuntimeError('SDL2 not found: pip install pysdl2-dll, or set SDL2_LIBRARY')


_lib = _load()


def _fn(name, restype, *argtypes):
    f = getattr(_lib, name)
    f.restype = restype
    f.argtypes = argtypes
    return f


Init = _fn('SDL_Init', c_int, c_uint32)
Quit = _fn('SDL_Quit', None)
GetError = _fn('SDL_GetError', c_char_p)
SetHint = _fn('SDL_SetHint', c_int, c_char_p, c_char_p)
GL_SetAttribute = _fn('SDL_GL_SetAttribute', c_int, c_int, c_int)
CreateWindow = _fn('SDL_CreateWindow', c_void_p, c_char_p, c_int, c_int, c_int, c_int, c_uint32)
DestroyWindow = _fn('SDL_DestroyWindow', None, c_void_p)
GetWindowSize = _fn('SDL_GetWindowSize', None, c_void_p, c_void_p, c_void_p)
GL_CreateContext = _fn('SDL_GL_CreateContext', c_void_p, c_void_p)
GL_DeleteContext = _fn('SDL_GL_DeleteContext', None, c_void_p)
GL_GetDrawableSize = _fn('SDL_GL_GetDrawableSize', None, c_void_p, c_void_p, c_void_p)
GL_SetSwapInterval = _fn('SDL_GL_SetSwapInterval', c_int, c_int)
GL_SwapWindow = _fn('SDL_GL_SwapWindow', None, c_void_p)
GL_GetProcAddress = _fn('SDL_GL_GetProcAddress', c_void_p, c_char_p)
PollEvent = _fn('SDL_PollEvent', c_int, c_void_p)
GetKeyName = _fn('SDL_GetKeyName', c_char_p, c_int)
GetTouchDeviceType = _fn('SDL_GetTouchDeviceType', c_int, c_int64)
GetPerformanceCounter = _fn('SDL_GetPerformanceCounter', c_int64)
GetPerformanceFrequency = _fn('SDL_GetPerformanceFrequency', c_int64)


def check(result):
    if result is None or result < 0:
        raise RuntimeError(GetError().decode())
    return result


def size_of(getter, window):
    w, h = c_int(), c_int()
    getter(window, byref(w), byref(h))
    return w.value, h.value


class EventBuffer:
    def __init__(self):
        self.raw = create_string_buffer(EVENT_SIZE)

    def poll(self):
        return PollEvent(self.raw) == 1

    @property
    def type(self):
        return struct.unpack_from('I', self.raw, 0)[0]

    def window(self):
        event, w, h = struct.unpack_from('B3xii', self.raw, 12)
        return event, w, h

    def key(self):
        repeat, sym = struct.unpack_from('xB2x4xi', self.raw, 12)
        return bool(repeat), sym

    def mouse_motion(self):
        which, x, y = struct.unpack_from('I4xii', self.raw, 12)
        return which, x, y

    def mouse_button(self):
        which, button, x, y = struct.unpack_from('IB3xii', self.raw, 12)
        return which, button, x, y

    def finger(self):
        touch_id, finger_id, x, y = struct.unpack_from('qqff', self.raw, 8)
        return touch_id, finger_id, x, y

