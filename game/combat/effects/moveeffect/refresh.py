from .basemoveeffect import BaseMoveEffect
from game.combat.effects.genericeffect import GenericEffect


class Refresh(BaseMoveEffect):
    def after_move(self):
        user_effects = self.scene.get_effects_on_target(self.move.user)
        for effect in [x for x in user_effects if x.type == "Majorstatus"]:
            self.scene.delete_effect(effect)
        self.scene.add_effect(
            GenericEffect(
                self.scene,
                f"{self.scene.board.get_actor(self.move.user).name} was cured!",
            )
        )
        return True
