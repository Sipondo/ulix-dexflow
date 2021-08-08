from game.combat.effects.baseeffect import BaseEffect


class DamageEffect(BaseEffect):
    def __init__(self, scene, target, abs_dmg=0, rel_dmg=0):
        super().__init__(scene)
        self.target = target
        self.abs_damage = abs_dmg
        self.rel_damage = rel_dmg
        self.spd_before_action = 1e10
        self.spd_on_action = 1e10
        self.spd_before_end = 1e10


    def before_action(self):
        damage = self.abs_damage + int(self.scene.board.get_actor(self.target).stats[0] * self.rel_damage)
        self.scene.board.inflict_damage(self.target, damage)
        # self.scene.board.no_skip(f"{self.scene.board.get_actor(self.target).name} took {damage} damage!", particle="")
        return True, False, False

    def on_action(self):
        damage = self.abs_damage + int(self.scene.board.get_actor(self.target).stats[0] * self.rel_damage)
        self.scene.board.inflict_damage(self.target, damage)
        # self.scene.board.no_skip(f"{self.scene.board.get_actor(self.target).name} took {damage} damage!", particle="")
        return True, False, False

    def before_end(self):
        damage = self.abs_damage + int(self.scene.board.get_actor(self.target).stats[0] * self.rel_damage)
        self.scene.board.inflict_damage(self.target, damage)
        # self.scene.board.no_skip(f"{self.scene.board.get_actor(self.target).name} took {damage} damage!", particle="")
        return True, False, False
