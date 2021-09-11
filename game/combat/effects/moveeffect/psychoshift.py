from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from game.combat.effects.genericeffect import GenericEffect


class Psychoshift(BaseMoveEffect):
    def after_action(self):
        target_effects = self.scene.get_effects_on_target(self.move.user)
        user_effects = self.scene.get_effects_on_target(self.move.user)
        if [x for x in target_effects if x.type == "Majorstatus"]:
            self.scene.add_effect(GenericEffect(self.scene, "But it failed"))
            return True, False, False
        if effects := [x for x in user_effects if x.type == "Majorstatus"]:
            effects[0].target = self.move.target
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.scene.board.get_actor(self.move.user).name} passed on its status problem!",
                )
            )
            return True, False, False
        self.scene.add_effect(GenericEffect(self.scene, "Nothing happened."))
        return True, False, False
