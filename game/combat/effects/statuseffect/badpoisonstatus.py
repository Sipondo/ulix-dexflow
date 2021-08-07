from game.combat.effects.baseeffect import BaseEffect
from game.combat.effects.damageeffect import DamageEffect


class BadPoison(BaseEffect):
    name = "BadPoison"
    particle = "genericstatus"
    type = "Majorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "got badly poisoned"
        self.target = target
        self.count = 1

    def before_end(self):
        if self.scene.board.is_active(self.target):
            self.scene.board.no_skip(
                f"{self.scene.board.board.get_actor(self.target).name} was hurt by poison",
                particle=self.particle,
            )
            self.scene.add_effect(
                DamageEffect(self.scene, self.target, rel_dmg=0.0625*self.count)
            )
            self.count += 1
        return False, False, False

    def on_switch(self, old_target, new_target):
        if self.target == old_target:
            self.count = 1
        return False, False, False

    def on_faint(self, target):
        return self.target == target, False, False
