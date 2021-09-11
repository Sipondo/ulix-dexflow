from .basemoveeffect import BaseMoveEffect
from game.combat.effects.genericeffect import GenericEffect


class Fullrefresh(BaseMoveEffect):
    def after_action(self):
        for i in range(self.scene.board.get_team_size(self.move.user[0])):
            user = (self.move.user[0], i)
            user_effects = self.scene.get_effects_on_target(user)
            for effect in [x for x in user_effects if x.type == "Majorstatus"]:
                self.scene.delete_effect(effect)
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.scene.board.get_actor(self.move.user).name} was cured!",
                )
            )
        return True, False, False
