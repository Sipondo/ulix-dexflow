from .baseabilityeffect import BaseAbilityEffect
from ..damageeffect import DamageEffect


class Aftermath(BaseAbilityEffect):
    name = "Aftermath"

    def on_faint(self, target):
        if self.active:
            if self.scene.current_action.target == self.holder:
                if not self.scene.get_effects_by_name("Damp"):
                    if self.scene.current_action_effect.contact:
                        actor = self.scene.board.get_actor(self.holder)
                        damage = actor.stats[0] // 4
                        self.scene.add_effect(
                            DamageEffect(
                                self.scene,
                                self.scene.current_action.user,
                                abs_dmg=damage,
                            )
                        )
