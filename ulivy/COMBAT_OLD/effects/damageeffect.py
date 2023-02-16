from ulivy.combat.effects.baseeffect import BaseEffect


class DamageEffect(BaseEffect):
    def __init__(self, scene, target, abs_dmg=0, rel_dmg=0, lethal=True, user=None):
        super().__init__(scene)
        self.target = target
        self.abs_damage = abs_dmg
        self.rel_damage = rel_dmg
        self.spd_before_action = 1e10
        self.spd_on_action = 1e10
        self.spd_before_end = 1e10
        self.lethal = lethal
        self.user = user

    def before_start(self):
        damage = self.abs_damage + int(
            self.scene.board.get_actor(self.target).stats[0] * self.rel_damage
        )
        self.scene.board.inflict_damage(self.target, damage, self.lethal, self.user)
        return True, False, False

    def before_action(self):
        damage = self.abs_damage + int(
            self.scene.board.get_actor(self.target).stats[0] * self.rel_damage
        )
        self.scene.board.inflict_damage(self.target, damage, self.lethal, self.user)
        return True, False, False

    def on_action(self):
        damage = self.abs_damage + int(
            self.scene.board.get_actor(self.target).stats[0] * self.rel_damage
        )
        self.scene.board.inflict_damage(self.target, damage, self.lethal, self.user)
        return True, False, False

    def after_action(self):
        damage = self.abs_damage + int(
            self.scene.board.get_actor(self.target).stats[0] * self.rel_damage
        )
        self.scene.board.inflict_damage(self.target, damage, self.lethal, self.user)
        return True, False, False

    def before_end(self):
        damage = self.abs_damage + int(
            self.scene.board.get_actor(self.target).stats[0] * self.rel_damage
        )
        self.scene.board.inflict_damage(self.target, damage, self.lethal, self.user)
        return True, False, False
