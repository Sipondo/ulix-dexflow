from game.combat.effects.baseeffect import BaseEffect
from game.combat.effects.damageeffect import DamageEffect


class Burn(BaseEffect):
    name = "Burn"
    particle = ""
    type = "Majorstatus"

    def __init__(self, state, user, target):
        super().__init__(state)
        self.apply_narration = "was burned!"
        self.target = target

    def before_end(self):
        if self.scene.board.is_active(self.target):
            self.scene.board.no_skip(
                f"{self.scene.board.get_actor(self.target).name} was hurt by its burn",
                particle=self.particle,
            )
            self.scene.add_effect(
                DamageEffect(self.scene, self.target, rel_dmg=0.0625)
            )
        return False, False, False

    @property
    def stat_mod(self):
        return [0.5, 1, 1, 1, 1, 1, 1]
