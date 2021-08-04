from game.combat.effects.baseeffect import BaseEffect
from game.combat.effects.damageeffect import DamageEffect


class Poison(BaseEffect):
    name = "Poison"
    particle = "poison"
    type = "Majorstatus"

    def __init__(self, scene, user, target):
        super().__init__(scene)
        self.apply_narration = "was inflicted by poison"
        self.target = target

    def before_end(self):
        if self.scene.board.is_active(self.target):
            self.scene.board.no_skip(
                f"{self.scene.board.get_actor(self.target)[0].name} was hurt by poison",
                particle=self.particle,
            )
            self.scene.add_effect(
                DamageEffect(self.scene, self.target, rel_dmg=0.125)
            )
        return False, False, False
