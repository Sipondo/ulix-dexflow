import os
import shutil
import subprocess
import traceback

from pathlib import Path
from termcolor import colored

os.system("color")

print(
    colored(
        """
ooooo     ooo ooooo        ooooo ooooooo  ooooo      
`888'     `8' `888'        `888'  `8888    d8'       
 888       8   888          888     Y888..8P         
 888       8   888          888      `8888'          
 888       8   888          888     .8PY888.         
 `88.    .8'   888       o  888    d8'  `888b        
   `YbodP'    o888ooooood8 o888o o888o  o88888o      

 +-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+
 |E|X|E|C|U|T|A|B|L|E| |B|U|I|L|D|E|R|
 +-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+
""",
        "cyan",
    )
)

print(
    colored(
        """
This program will build your game into an .exe file.
The game will be playable even if people do not have a Python installation.
Once completed the finished product can be found in the 'export' folder.
The operation will require an amount of disk space roughly similar to the size of your project.
Building your game may take a while depending on the size of the project and the speed of your computer.
""",
        "yellow",
    )
)

print(
    colored(
        """WARNING!!! THE 'export' FOLDER AND ALL ITS CONTENTS WILL BE REMOVED UPON CONTINUING
""",
        "red",
    )
)

print(colored("Please specify (y/n) whether you want to continue.", "magenta"))
while (inp := input() or "none") :
    if inp == "y":
        break
    if inp == "n":
        print("Aborting...")
        exit()
    print("Please specify (y/n) whether you want to continue.")


try:
    print(
        colored(
            """
    ====================================================================================================
    (1/8)

    Removing 'export'.
    """,
            "yellow",
        )
    )

    path_export = Path("export")

    if path_export.is_dir():
        shutil.rmtree(path_export)

    print(
        colored(
            """
    ====================================================================================================
    (2/8)

    Compiling world.ldtk.
    """,
            "yellow",
        )
    )

    subprocess.run(
        r"""python game.py --compile-world world""", shell=True, check=True,
    )

    print(
        colored(
            """
    ====================================================================================================
    (3/8)

    Creating fresh virtualenv '.exportvenv'.
    """,
            "yellow",
        )
    )

    subprocess.run(
        r"""python -m venv .exportvenv""", shell=True, check=True,
    )

    print(
        colored(
            """
    ====================================================================================================
    (4/8)

    Installing requirements.
    """,
            "yellow",
        )
    )

    subprocess.run(
        r"""call .exportvenv\Scripts\activate.bat && pip install -r requirements.txt""",
        shell=True,
        check=True,
    )

    print(
        colored(
            """
    ====================================================================================================
    (5/8)

    Building the executable.
    """,
            "yellow",
        )
    )

    subprocess.run(
        r"""call .exportvenv\Scripts\activate.bat && cxfreeze -c game.py --target-dir export --packages "moderngl,moderngl_window,pyglet,moderngl_window.context.pyglet,glcontext,moderngl_window.loaders.texture,moderngl_window.loaders.program" --base-name=WIN32GUI""",
        shell=True,
        check=True,
    )

    print(
        colored(
            """
    ====================================================================================================
    (6/8)

    Copying game files.
    """,
            "yellow",
        )
    )

    shutil.copytree(Path("game"), path_export / "game")

    print(
        colored(
            """
    ====================================================================================================
    (7/8)

    Copying resources files.
    """,
            "yellow",
        )
    )

    shutil.copytree(Path("resources"), path_export / "resources")

    print(
        colored(
            """
    ====================================================================================================
    (8/8)

    Copying world.ldtkc.
    """,
            "yellow",
        )
    )

    shutil.copy(Path("world.ldtkc"), path_export / "world.ldtkc")

except Exception as e:
    traceback.print_exc()
    print(
        colored(
            """EXPORT_GAME has cancelled due to an error.
    """,
            "red",
        )
    )

finally:
    print(
        colored(
            """
    ====================================================================================================
    Removing '.exportvenv'.
    """,
            "yellow",
        )
    )

    path_venv = Path(".exportvenv")

    if path_venv.is_dir():
        shutil.rmtree(path_venv)

    print(colored("Waiting for input to quit...", "magenta"))
    input()
