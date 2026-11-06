"""browser"""
import js
import zengl
from pyodide.ffi import create_proxy

from .glsl import install_glsl_header
from .event import Event

KEY_ALIASES = {
    ' ': 'space',
    'arrowleft': 'left',
    'arrowright': 'right',
    'arrowup': 'up',
    'arrowdown': 'down',
    'enter': 'return',
}

POINTER_EVENTS = {
    'pointerdown': 'pointer_down',
    'pointerup': 'pointer_up',
    'pointercancel': 'pointer_up',
    'pointermove': 'pointer_move',
}


class WebHost:
    def run(self, game):
        self.game = game
        self.events: list[Event] = []
        self.lost = False
        self.restored = False
        self.last_time = None

        # zengl.init() binds the WebGL 2 context of the <canvas id="canvas"> element, creating it if absent.
        zengl.init()
        self.canvas = js.document.getElementById('canvas')
        self.size = self._fit_canvas()
        self._init_gl()

        # Proxies are kept on self: JS holds the only other reference and Pyodide would free them.
        self._proxies = []
        for name in POINTER_EVENTS:
            self._listen(self.canvas, name, self._on_pointer)
        self._listen(js.window, 'keydown', self._on_key)
        self._listen(js.window, 'keyup', self._on_key)
        self._listen(self.canvas, 'webglcontextlost', self._on_context_lost)
        self._listen(self.canvas, 'webglcontextrestored', self._on_context_restored)

        self._frame_proxy = create_proxy(self._frame)
        js.requestAnimationFrame(self._frame_proxy)

    def _listen(self, target, name, handler):
        proxy = create_proxy(handler)
        self._proxies.append(proxy)
        target.addEventListener(name, proxy)

    def _init_gl(self):
        ctx = zengl.context()
        install_glsl_header(ctx)
        self.game.setup(ctx, self.size)

    def _fit_canvas(self):
        dpr = js.window.devicePixelRatio or 1.0
        w = max(1, round(self.canvas.clientWidth * dpr))
        h = max(1, round(self.canvas.clientHeight * dpr))
        if (self.canvas.width, self.canvas.height) != (w, h):
            self.canvas.width = w
            self.canvas.height = h
        return w, h

    def _on_pointer(self, e):
        if e.type == 'pointerdown':
            self.canvas.setPointerCapture(e.pointerId)
        elif e.type == 'pointermove' and e.pointerType != 'mouse' and not e.buttons:
            return
        dpr = js.window.devicePixelRatio or 1.0
        self.events.append(Event(POINTER_EVENTS[e.type], x=e.offsetX * dpr, y=e.offsetY * dpr, pointer=e.pointerId))

    def _on_key(self, e):
        if e.repeat:
            return
        key = e.key.lower()
        self.events.append(Event('key_down' if e.type == 'keydown' else 'key_up', key=KEY_ALIASES.get(key, key)))

    def _on_context_lost(self, e):
        e.preventDefault()
        self.lost = True

    def _on_context_restored(self, e):
        self.restored = True

    def _frame(self, timestamp):
        dt = 0.0 if self.last_time is None else (timestamp - self.last_time) / 1000.0
        self.last_time = timestamp

        if self.restored:
            self.lost = self.restored = False
            zengl.init()
            self._init_gl()

        if not self.lost:
            size = self._fit_canvas()
            if size != self.size:
                self.size = size
                self.game.resize(size)

            events, self.events = self.events, []
            for event in events:
                self.game.event(event)

            ctx = zengl.context()
            ctx.new_frame()
            self.game.update(dt)
            ctx.end_frame()

        js.requestAnimationFrame(self._frame_proxy)
