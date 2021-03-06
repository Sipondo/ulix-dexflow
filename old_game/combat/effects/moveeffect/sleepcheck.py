from .basemoveeffect import BaseMoveEffect


class Sleepcheck(BaseMoveEffect):
    def before_action(self):
        user_effects = self.scene.get_effects_on_target(self.move.user)
        if sleep_effects := [x for x in user_effects if x.name == "Sleep"]:
            sleep_effects[0].skip = True
        return False, False, False
