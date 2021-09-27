"""function
Fully restores the player's party.

Fully restores the player's party of all illnesses and damage.

in:
None

"""


class RestoreParty:
    def __init__(self, act, src, user):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time

    def on_tick(self, time=None, frame_time=None):
        for member in self.game.inventory.members:
            member.current_hp = member.stats[0]
            member.status = None
        return True

    def on_read(self):
        return None
