from .baseabilityeffect import BaseAbilityEffect
from ..genericeffect import GenericEffect


class Anticipation(BaseAbilityEffect):
    name = "Anticipation"

    def on_activate(self):
        actor = self.scene.board.get_actor(self.holder)
        enemy_team = (self.holder + 1) % 2
        enemy_actor = self.scene.board.get_actor((enemy_team, self.scene.board.get_active(enemy_team)))
        for action in enemy_actor.actions:
            if self.get_move_effectiveness(action.type, actor.type1, actor.type2) > 1:
                self.scene.add_effect(GenericEffect(self.scene, f"{actor.name} shuddered in anticipation!"))

    def get_move_effectiveness(self, move_type, target_type1, target_type2):
        type_1_eff = self.scene.game.m_pbs.get_type_effectiveness(
            move_type, target_type1
        )
        if target_type2.lower() != "nan":
            type_2_eff = self.scene.game.m_pbs.get_type_effectiveness(
                move_type, target_type2
            )
        else:
            type_2_eff = 1
        return type_1_eff * type_2_eff
