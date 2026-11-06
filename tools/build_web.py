"""tooling to host the game in a browser, packages the game into a zip
"""

import hashlib
import io
import json
import re
import shutil
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
WEB = TOOLS / 'web'
OUT = ROOT / 'build' / 'web'
ENTRY = 'main.py'
APP_DIRS = ['ulix', 'ulix_shaders', 'resources', 'data']
APP_FILES = ['world.ldtkc']

EXCLUDE = {Path(p) for p in ('ulix/host/_sdl2.py', 'ulix/host/sdl.py')}
EXCLUDE_SUFFIXES = {'.pdn', '.psd', '.xlsx'}

STORED_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.ogg', '.mp3', '.ttf', '.otf', '.ldtkc', '.npz', '.zip'}
STATIC = [
    'index.html',
    'manifest.json',
    'favicon.ico',
    'icon-192.png',
    'icon-512.png',
    'icon-maskable-512.png',
    'apple-touch-icon.png',
]


def app_files():
    files = [ROOT / ENTRY]
    for name in APP_FILES:
        if (ROOT / name).is_file():
            files.append(ROOT / name)
        else:
            print(f'warning: {name} is missing, the game will not find it (run compile_world.py)')
    for app_dir in APP_DIRS:
        for path in sorted((ROOT / app_dir).rglob('*')):
            rel = path.relative_to(ROOT)
            if (path.is_file() and '__pycache__' not in rel.parts and path.suffix.lower() not in EXCLUDE_SUFFIXES
                    and not EXCLUDE & {rel, *rel.parents}):
                files.append(path)
    return files


def get_lark_dir():
    # check if lark exists
    try:
        import lark
        src = Path(lark.__file__).resolve().parent
        if (src / '__init__.py').is_file():
            return src
    except Exception:
        pass

    cache_dir = ROOT / 'build' / '.cache' / 'lark'
    if (cache_dir / '__init__.py').is_file():
        return cache_dir

    print('downloading lark from PyPI...')
    api_url = 'https://pypi.org/pypi/lark/json'
    req = urllib.request.Request(api_url, headers={'User-Agent': 'build_web/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        meta = json.loads(resp.read().decode('utf-8'))

    whl_url = None
    for url_info in meta.get('urls', []):
        fn = url_info.get('filename', '')
        if fn.endswith('-none-any.whl'):
            whl_url = url_info.get('url')
            break

    if not whl_url:
        for url_info in meta.get('urls', []):
            if url_info.get('packagetype') == 'bdist_wheel':
                whl_url = url_info.get('url')
                break

    if not whl_url:
        raise RuntimeError('could not find a suitable pure-Python wheel for lark on PyPI')

    print(f'downloading {whl_url}...')
    with urllib.request.urlopen(whl_url, timeout=30) as resp:
        whl_bytes = resp.read()

    cache_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(whl_bytes)) as zf:
        for member in zf.namelist():
            if member.startswith('lark/') and not member.endswith('/'):
                rel_path = member[len('lark/'):]
                target = cache_dir / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(member))

    return cache_dir


def main():
    lark_dir = get_lark_dir()
    OUT.mkdir(parents=True, exist_ok=True)
    build = hashlib.sha256(Path(__file__).read_bytes())
    for name in STATIC:
        src = WEB / name
        if src.is_file():
            shutil.copy(src, OUT / name)
            build.update(src.read_bytes())

    with zipfile.ZipFile(OUT / 'app.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in app_files():
            rel = path.relative_to(ROOT).as_posix()
            stored = path.suffix.lower() in STORED_SUFFIXES
            zf.write(path, rel, zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED)
            build.update(rel.encode() + path.read_bytes())

        # include lark in the root of app.zip
        for p in sorted(lark_dir.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                rel = 'lark/' + p.relative_to(lark_dir).as_posix()
                zf.write(p, rel, zipfile.ZIP_DEFLATED)
                build.update(rel.encode() + p.read_bytes())

    pyodide = re.search(r'/pyodide/v([\w.]+)/', (WEB / 'index.html').read_text(encoding='utf-8')).group(1)
    worker = (WEB / 'sw.js').read_text(encoding='utf-8')
    build.update(worker.encode())
    worker = worker.replace('__BUILD__', build.hexdigest()[:12]).replace('__PYODIDE__', pyodide)
    (OUT / 'sw.js').write_text(worker, encoding='utf-8')


if __name__ == '__main__':
    main()
