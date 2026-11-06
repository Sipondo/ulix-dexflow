[app]
title = Ulix Dexflow
package.name = ulixdexflow
package.domain = org.ulix.dexflow
version = 0.1

source.dir = .
source.include_exts = py,ttf,txt,png,jpg,ldtkc,json,glsl
source.exclude_dirs = .venv, .git, .buildozer, bin, build, tools, web
source.exclude_patterns = ulix/host/web.py

requirements = python3,sdl2,zengl,Pillow,fonttools
orientation = landscape
fullscreen = 1

android.api = 35
android.minapi = 24
android.archs = arm64-v8a, x86_64
android.accept_sdk_license = True

p4a.bootstrap = sdl2
p4a.local_recipes = ./recipes

[buildozer]
log_level = 2
warn_on_root = 1
