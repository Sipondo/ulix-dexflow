from .baseeffect import BaseEffect
from .genericeffect import GenericEffect
from .damageeffect import DamageEffect


class MainMove(BaseEffect):
    type = "Move"

    def __init__(self, scene, move):
        super().__init__(scene)
        self.move = move

        # move attributes
        self.name = move["name"]
        self.user = move.user
        self.target = move.target
        self.type = move.type
        self.chance = move.chance / 100
        self.move_cat = move.damagecat
        self.power = move.power
        self.accuracy = move.accuracy
        self.perfect_accuracy = True if move.accuracy == 0 else False

        # added effects
        self.effects = []
        # TEMP
        for func in [move.function]:
            move_effect = self.scene.effect_lib[func](self.scene, self)
            self.effects.append(move_effect)
            self.scene.effects.append(move_effect)

    def move_hit(self):
        if not self.perfect_accuracy:
            acc = 1
            # accuracy boosts
            for acc_mod in [
                x.stat_mod[5]
                for x in self.scene.get_effects_on_target(self.user)
                if x.name == "Statmod"
            ]:
                acc *= acc_mod
            for eva_mod in [
                x.stat_mod[6]
                for x in self.scene.get_effects_on_target(self.target)
                if x.name == "Statmod"
            ]:
                acc /= eva_mod
            if self.scene.board.random_roll() > ((self.accuracy / 100) * acc):
                self.scene.board.particle_miss = True
                self.scene.add_effect(GenericEffect(self.scene, "But it missed!"))
                return False
        if self.power > 0:
            print("I have power!")
            # CRITS
            crit_chance = 0.04167
            crit_total = 0
            if crit_level := [
                x.level
                for x in self.scene.get_effects_by_name("Critmod")
                if x.target == self.target
            ]:
                crit_total += crit_level
            if crit_total == 1:
                crit_chance = 0.125
            if crit_total == 2:
                crit_chance = 0.5
            if crit_total > 2:
                crit_chance = 1
            crit = self.scene.board.random_roll() < crit_chance

            # Calculate move dmg/effectiveness etc.
            return self.move_damage(crit=crit)
        return True

    def move_damage(self, crit=False):
        user_mon = self.scene.board.get_actor(self.user)
        target_mon = self.scene.board.get_actor(self.target)
        stab = 1
        if self.type in (user_mon.type_1, user_mon.type_2):
            stab = 1.5
        move_effectiveness = self.get_move_effectiveness(
            self.type, target_mon.type_1, target_mon.type_2
        )
        if move_effectiveness == 0:
            return False

        # stat modifiers
        target_effects = self.scene.get_effects_on_target(self.target)
        user_effects = self.scene.get_effects_on_target(self.user)

        atk_mod = 1
        def_mod = 1
        if self.move_cat == "Physical":
            for effect in [x for x in user_effects if x.name == "Statmod"]:
                atk_mod *= effect.stat_mod[0]
            for effect in [x for x in target_effects if x.name == "Statmod"]:
                def_mod *= effect.stat_mod[1]
        if self.move_cat == "Special":
            for effect in [x for x in user_effects if x.name == "Statmod"]:
                atk_mod *= effect.stat_mod[2]
            for effect in [x for x in target_effects if x.name == "Statmod"]:
                def_mod *= effect.stat_mod[3]

        # damage
        damage = (0.4 * user_mon.level + 2) * self.power
        damage *= (
            ((user_mon.stats[1]*atk_mod) / (target_mon.stats[2]*def_mod))
            if self.type == "Physical"
            else ((user_mon.stats[1]*atk_mod) / (target_mon.stats[2]*def_mod))
        )
        damage = damage / 50 + 2
        damage *= move_effectiveness * stab
        if crit:
            self.scene.add_effect(GenericEffect(self.scene, "Critical hit!"))
            damage *= 1.5
        damage *= 1 - (self.scene.board.random_roll() * 0.15)
        damage = int(damage)
        self.scene.add_effect(DamageEffect(self.scene, self.target, abs_dmg=damage))
        return True

    def get_move_effectiveness(self, move_type, target_type_1, target_type_2):
        # TODO get move effectiveness
        return 1

    def on_action(self):
        if self.scene.board.user != self.user:
            return False, False, False
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.user).name} used {self.name}",
            particle=self.name,
        )
        for effect in self.effects:
            if not effect.before_move():
                self.scene.board.particle = ""
                self.scene.add_effect(GenericEffect(self.scene, "But it failed"))
                return True, False, False
        if self.move_hit():
            for effect in self.effects:
                effect.after_move()
        return True, False, False

    def on_switch(self, target_old, target_new):
        if self.target == target_old:
            self.target = target_new

    def on_delete(self):
        for effect in self.effects:
            self.scene.delete_effect(effect)
