import abc


class BaseEffect(abc.ABC):
    name = "None"
    type = "None"

    def __init__(self, scene):
        self.scene = scene
        self.done = False
        self.skip = False
        self.target = "Global"
        self.spd_on_faint = 0
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
        return False, False, False

    def on_send_out(self, new_target):
        return False, False, False

    def on_faint(self, target):
        return False, False, False

    def before_action(self):
        return False, False, False

    def on_action(self):
        return False, False, False

    def after_action(self):
        return False, False, False

    def before_end(self):
        return False, False, False

    def on_hit(self, move):
        return False

    def on_damage(self, damage):
        pass

    def on_status(self, target):
        return False

    def on_stat_change(self, target):
        return False

    def on_stat_request(self, target, stat):
        return None

    def on_delete(self):
        pass

    @property
    def stat_mod(self):
        # atk, def, spatk, spdef, speed, acc, eva
        return [1, 1, 1, 1, 1, 1, 1]
