import os.path
from kivy.resources import resource_add_path

KV_PATH = os.path.realpath(os.path.dirname(__file__))
resource_add_path(KV_PATH)

from kivy.lang import Builder

Builder.load_file("joystickdemo.kv")

from .JoystickDemo import JoystickDemo
