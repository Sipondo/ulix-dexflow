from ulivy.manager.pluginmanager import Plugin

class Armourui(Plugin):
    def pre_load(self, **kwargs):
        print("ARMOURUI PRE")
        pass

    def post_load(self, **kwargs):
        print("ARMOURUI POST")
        pass

    def update(self, time, frame_time):
        return self.lock

    @property
    def priority(self):
        return 0
