import abc
import importlib

from pathlib import Path

def contains(path, name):
    return name in [x.name for x in path.iterdir()]



class Plugin(abc.ABC):
    def __init__(self, game):
        self.game = game

    @abc.abstractmethod
    def pre_load(self, **kwargs):
        pass

    @abc.abstractmethod
    def post_load(self, **kwargs):
        pass

    @abc.abstractmethod
    def update(self, time, frame_time):
        return self.lock

    @property
    @abc.abstractmethod
    def priority(self):
        return 0



class PluginManager:
    def __init__(self, game):
        self.game = game

        plugin_names = [resource.name for resource in Path("resources").iterdir() if contains(resource, f"{resource.name}.py")]
        print("PLUGIN PATHS!", plugin_names)

        self.plugins = {}
        for plugin_name in plugin_names:
            self.plugins[plugin_name] = getattr(importlib.import_module(f"resources.{plugin_name}.{plugin_name}"), plugin_name.capitalize())(self.game)

    def pre_load(self):
        for k, v in self.plugins.items():
            v.pre_load()

    def post_load(self):
        for k, v in self.plugins.items():
            v.post_load()

    def update(self, time, frame_time):
        for k, v in self.plugins.items():
            v.update(time, frame_time)
