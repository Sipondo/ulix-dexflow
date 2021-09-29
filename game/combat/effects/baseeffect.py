import abc


class BaseEffect(abc.ABC):
    name = "None"
    type = "None"

    def __init__(self, scene):
        self.scene = scene
        self.done = False
        self.skip = False
        self.target = "Global"
        self.spd_before_start = 0
        self.spd_before_action = 0
        self.spd_on_action = 0
        self.spd_after_action = 0
        self.spd_before_end = 0
        self.spd_switch_phase = 0
        self.spd_on_switch = 0
        self.spd_on_send_out = 0
        self.spd_on_faint = 0
        self.spd_on_crit = 0
        self.spd_grounded = 0
        self.priority = 0

    # def after_select(self):
    #     return False, False, False

    def on_switch(self, target_old, target_new):
        """All effects that happen before an actor is returned."""
        return False, False, False

    def on_send_out(self, new_target):
        """All effects that happen after a new actor is sent out."""
        return False, False, False

    def on_faint(self, target):
        """All effects that happen after an actor faints"""
        return False, False, False

    def before_start(self):
        """All effects that happen in a turn before the actions start.
        Mainly used for changing move priority"""
        return False, False, False

    def before_action(self):
        """All effects that happen before an action occurs.
        This includes checks for whether the action can be performed"""
        return False, False, False

    def on_action(self):
        """All effects that happen during or directly influence the action"""
        return False, False, False

    def after_action(self):
        """All effects that happen before an action occurs.
        This includes checks for whether the action can be performed"""
        return False, False, False

    def before_end(self):
        """All effects that happen before a turn ends."""
        return False, False, False

    def switch_phase(self):
        """All effects that happen during the switch phase in between turns"""
        return False, False, False

    def on_hit(self, move):
        """All effects that happen when an actor gets hit by an action"""
        return False

    def on_damage(self, damage):
        """All effects that happen when an actor takes damage"""
        pass

    def on_status(self, target):
        """All effects that happen when an actor gets inflicted with a status"""
        return False

    def on_stat_change(self, target):
        """All effects that happen before an actor gets a stat changed"""
        return False

    def on_stat_request(self, target, stat):
        """All effects that happen when a stat of an actor is requested.
        Usage is mostly when the target has a stat switched with another actor."""
        return None

    def on_delete(self):
        """Effects that happen when the effect gets deleted."""
        pass

    def on_crit(self, target):
        """Effects that happen when the target is crit."""
        return False, False, False

    def grounded(self, target):
        """Effects that influence whether the target is grounded"""
        return None

    @property
    def stat_mod(self):
        """All effects that change a stat modifier"""
        # atk, def, spatk, spdef, speed, acc, eva
        return [1, 1, 1, 1, 1, 1, 1]
