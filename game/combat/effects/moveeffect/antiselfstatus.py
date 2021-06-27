from .basemoveeffect import BaseMoveEffect


class Antiselfstatus(BaseMoveEffect):
    def before_move(self):
        user_effects = self.scene.get_effects_on_target(self.move.user)
        if major_statuses := [x for x in user_effects if x.type == "Majorstatus"]:
            for major_status in major_statuses:
                if major_status.name == "Burn":
                    major_status.skip = True
            self.move.power *= 2
            return True
