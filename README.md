[![License](https://img.shields.io/badge/License-CC_BY_NC_SA_4.0-blue.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0)
[![Python Version](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![LDTK](https://img.shields.io/badge/awesomified_by-ldtk-orange.svg)](https://ldtk.io/)
[![Moderngl](https://img.shields.io/badge/powered_by-moderngl-red.svg)](https://github.com/moderngl/moderngl)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Support Server](https://img.shields.io/discord/762339140272128070.svg?label=Discord&logo=Discord&colorB=7289da&style=for-the-badge)](https://discord.gg/4EkvwQf2UT)

# Ulix: Dexflow
Dexflow is a framework for building (fan)games inspired by the Pokémon series of games.
As with any Ulix framework, Dexflow expands Ulix' functionality with features usually found in these kinds of games.
The framework falls under the Creative Commons BY-NC-SA 4.0 license. Any used assets and libraries fall under their own respective licenses.

# Documentation

Dexflow is currently in unlabelled alpha and is undergoing heavy changes. When creating your own work using the framework we heavily recommend keeping to certain types of additions:

- Create your own awesome world.
- Place people in your world and give them behaviours.
- Add new battlers for players to discover and find.
- Fine-tune encounters for the perfect game balance.
- Create cinematics with dialogue and events.
- Make your own 3D animations for your battler's attacks.

In general, you should definitely join our [Discord](https://discord.gg/4EkvwQf2UT) for any questions and, perhaps more importantly, suggestions! The framework is incredibly fresh and your feedback will have a definite impact on the final product!

We offer very little documentation as of now. If you want an introduction, need help, or have any questions, you should hit us up on Discord! We regularly introduce new people to the framework, so please do not hesitate to ask. :-)

If you have any suggestion or issue, please post on Discord and/or make an issue on [Github](https://github.com/Sipondo/ulix-dexflow/issues).

# Basic Usage
You can either clone the repo directly or patch the repo on an existing Ulix folder.
Python version 3.8 is heavily recommended as it ensures compatibility with the [Ulix Particle Forge](https://github.com/Sipondo/ulix-particle-forge).

Please install any dependencies by running `setup.bat`.

Before your first time playing the game, and after making any changes to the world, you will need to compile the LDTK world file.

Run `compile_world.bat` to generate the compressed world file, after which your game can be played via `game.bat`.

# Building your world

Editing the world is done via the editor program [LDTK](https://ldtk.io/). We heavily advise you to use the `world.ldtk` file supplied with this repo (in the [world](https://github.com/Sipondo/ulix-dexflow/tree/main/world) folder) as a base for your own world as it has been correctly configured for use.
