import os, sys, shutil
from cx_Freeze import setup, Executable
from pathlib import Path


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


# Dependencies are automatically detected, but it might need fine tuning.
additional_modules = []

build_exe_options = {
    "includes": additional_modules,
    "packages": [
        "moderngl",
        "moderngl_window",
        "pyglet",
        "moderngl_window.context.pyglet",
        "glcontext",
        "moderngl_window.loaders.texture",
        "moderngl_window.loaders.program",
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Catchbase",
    version="1.0",
    description="Play your fangame",
    options={"build_exe": build_exe_options},
    executables=[Executable(script="game.py", base=base)],
)

for x in Path("build").glob("*"):
    p = x
    break

copytree("resources", str(p / "resources"))

