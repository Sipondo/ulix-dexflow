"""Serve the web build and rebuild it whenever the game changes
"""

import argparse
import functools
import sys
import threading
import time
import traceback
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_web

WATCHED = [build_web.ROOT / p for p in (build_web.ENTRY, *build_web.APP_FILES, *build_web.APP_DIRS)]
VERSION_PATH = '/__version'
RELOAD_SCRIPT = f"""<script>
  window.ENGINE_DEV = true;
  (() => {{
    let seen = null;
    setInterval(async () => {{
      try {{
        const version = await (await fetch('{VERSION_PATH}', {{ cache: 'no-store' }})).text();
        if (seen !== null && version !== seen) location.reload();
        seen = version;
      }} catch {{}}
    }}, 500);
  }})();
</script>
"""


def snapshot():
    files = {}
    for watched in WATCHED:
        paths = watched.rglob('*') if watched.is_dir() else [watched]
        for path in paths:
            if path.is_file() and '__pycache__' not in path.parts:
                files[path] = path.stat().st_mtime_ns
    return files


class Builds:
    """The build counter the page polls; `lock` keeps requests from reading a half-written app.zip."""

    def __init__(self):
        self.lock = threading.Lock()
        self.version = 0

    def rebuild(self):
        with self.lock:
            try:
                build_web.main()
                self.version += 1
                print(f'rebuilt web app (version {self.version})')
            except Exception:
                traceback.print_exc()


class DevHandler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.wasm': 'application/wasm'}

    def __init__(self, *args, builds, **kwargs):
        self.builds = builds
        super().__init__(*args, directory=str(build_web.OUT), **kwargs)

    def do_GET(self):
        if self.path == VERSION_PATH:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(str(self.builds.version).encode())
            return
        with self.builds.lock:
            super().do_GET()

    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'credentialless')
        super().end_headers()

    def copyfile(self, source, outputfile):
        if getattr(source, 'name', None) == str(build_web.OUT / 'index.html'):
            content = source.read().decode('utf-8')
            content = content.replace('<head>', '<head>' + RELOAD_SCRIPT, 1)
            outputfile.write(content.encode('utf-8'))
            return
        super().copyfile(source, outputfile)

    def log_message(self, format, *args):
        # supress spam
        if args and args[0].startswith(f'GET {VERSION_PATH}'):
            return
        super().log_message(format, *args)


def watch(builds):
    seen = snapshot()
    while True:
        time.sleep(0.25)
        current = snapshot()
        if current != seen:
            seen = current
            builds.rebuild()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()

    builds = Builds()
    builds.rebuild()
    threading.Thread(target=watch, args=(builds,), daemon=True).start()

    handler = functools.partial(DevHandler, builds=builds)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f'serving {build_web.OUT} at http://{args.host}:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
