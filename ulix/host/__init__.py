import sys

from .event import Event, EventKind
from .glsl import GLSL_DESKTOP, GLSL_ES, install_glsl_header


def run(game): 
    if sys.platform == 'emscripten':
        from .web import WebHost as Host
    else:
        from .sdl import SDLHost as Host
    Host().run(game)


__all__ = ['Event', 'EventKind', 'GLSL_DESKTOP', 'GLSL_ES', 'install_glsl_header', 'run']
