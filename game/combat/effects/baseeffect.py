import abc


class BaseEffect(abc.ABC):
    name = "None"
    type = "None"

    def __init__(self, scene):
        self.scene = scene
        self.done = False
        self.target = "Global"
        self.spd_after_select = 0
        self.spd_before_action = 0
        self.spd_on_action = 0
        self.spd_after_action = 0
        self.spd_before_end = 0
        self.spd_on_switch = 0
        self.spd_on_send_out = 0
        self.priority = 0

    def after_select(self):
        return False, False, False

    def on_switch(self, target_old, target_new):
        return False

    def on_end_turn(self):
        return False, False, False

    def before_action(self):
        return False, False, False

    def on_action(self):
        return False, False, False

    def after_action(self):
        return False, False, False

    def before_end(self):
        return False, False, False

    def on_hit(self):
        return False, False, False

    def on_status(self, target):
        return True

    def on_delete(self):
        pass

    @property
    def stat_mod(self):
        # atk, def, spatk, spdef, speed, acc, eva
        return [1, 1, 1, 1, 1, 1, 1]
