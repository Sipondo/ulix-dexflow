from .basemoveeffect import BaseMoveEffect
from game.combat.effects.genericeffect import GenericEffect


class Cure(BaseMoveEffect):
    def after_move(self):
        target_effects = self.scene.get_effects_on_target(self.move.target)
        for status in [x for x in target_effects if x.type == "Majorstatus"]:
            self.scene.delete_effect(status)
        self.scene.add_effect(
            GenericEffect(
                self.scene,
                f"{self.scene.board.get_actor(self.move.user).name} was cured!",
            )
        )
        return True
