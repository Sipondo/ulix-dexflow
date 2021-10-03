from .baseeffect import BaseEffect
from .genericeffect import GenericEffect
from .damageeffect import DamageEffect


class MainMove(BaseEffect):
    type = "Move"

    def __init__(self, scene, action):
        super().__init__(scene)
        move = action.a_data
        print(move)
        self.move = move

        # move attributes
        self.name = move["name"]
        self.user = action.user
        self.target = action.target
        self.type = move.type
        self.chance = 1 if move.chance == 0 else move.chance / 100
        self.move_cat = move.damagecat
        self.power = move.power
        self.accuracy = move.accuracy

        self.contact = "a" in move["flags"]
        self.protectable = "b" in move["flags"]
        self.magiccoatable = "c" in move["flags"]
        self.snatchable = "d" in move["flags"]
        self.mirrormoveable = "e" in move["flags"]
        self.kingsrock = "f" in move["flags"]
        self.thaws = "g" in move["flags"]
        self.high_crit = "h" in move["flags"]
        self.biting = "i" in move["flags"]
        self.punching = "j" in move["flags"]
        self.sound = "k" in move["flags"]
        self.powder = "l" in move["flags"]
        self.pulse = "m" in move["flags"]
        self.bomb = "n" in move["flags"]
        self.dance = "o" in move["flags"]

        self.abs_acc = False
        self.perfect_accuracy = True if move.accuracy == 0 else False

        self.fail = False

        # no target (if enemy fainted)
        self.target_fainted = False

        # added effects
        for func in move.function:
            function_args = func.split(" ")
            if len(function_args) > 1:
                func, args = function_args
                move_effect = self.scene.effect_lib[func](self.scene, self, args)
            else:
                move_effect = self.scene.effect_lib[func](self.scene, self)
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
            acc = 1 if self.abs_acc else acc
            if not self.scene.board.random_roll((self.accuracy / 100) * acc):
                self.scene.board.particle_miss = True
                self.scene.add_effect(GenericEffect(self.scene, "But it missed!"))
                return False
        if self.power > 1:
            # CRITS
            crit_chance = 0.04167
            crit_total = 0
            if crit_level := [
                x.level
                for x in self.scene.get_effects_on_target(self.user)
                if x.name == "Critmod"
            ]:
                crit_total += crit_level[0]
            if crit_total == 1:
                crit_chance = 0.125
            if crit_total == 2:
                crit_chance = 0.5
            if crit_total > 2:
                crit_chance = 1
            crit = self.scene.board.random_roll(crit_chance)
            # Calculate move dmg/effectiveness etc.
            if crit:
                self.scene.on_crit_effects(self.target)
            return self.move_damage(crit=crit)
        return True

    def move_damage(self, crit=False):
        # mon stats
        user_mon = self.scene.board.get_actor(self.user)
        target_mon = self.scene.board.get_actor(self.target)

        # move type mods
        stab = 1
        if self.type in (user_mon.type1, user_mon.type2):
            stab = 1.5
        move_effectiveness = self.get_move_effectiveness(
            self.type, target_mon.type1, target_mon.type2
        )
        for effect in self.scene.get_effects_on_target(self.target):
            if effect.on_hit(self):
                return False
        if move_effectiveness == 0:
            self.scene.add_effect(
                GenericEffect(self.scene, f"It doesn't affect foe {target_mon.name}")
            )
            return False
        if move_effectiveness < 1:
            self.scene.add_effect(GenericEffect(self.scene, "It's not very effective"))
        if move_effectiveness > 1:
            self.scene.add_effect(GenericEffect(self.scene, "It's super effective"))

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

        if crit:
            if atk_mod < 1:
                atk_mod = 1
            if def_mod > 1:
                def_mod = 1

        # damage
        damage = (0.4 * user_mon.level + 2) * self.power
        damage *= (
            ((user_mon.stats[1] * atk_mod) / (target_mon.stats[2] * def_mod))
            if self.type == "Physical"
            else ((user_mon.stats[1] * atk_mod) / (target_mon.stats[2] * def_mod))
        )
        damage = damage / 50 + 2
        damage *= move_effectiveness * stab
        if crit:
            # TODO add crit damage mods
            self.scene.add_effect(GenericEffect(self.scene, "Critical hit!"))
            damage *= 1.5
        damage *= 1 - (self.scene.board.random_float() * 0.15)
        damage = int(damage)
        self.scene.add_effect(DamageEffect(self.scene, self.target, abs_dmg=damage))
        return True

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

    def on_action(self):
        if self.scene.board.user != self.user:
            return False, False, False
        self.scene.board.no_skip(
            f"{self.scene.board.get_actor(self.user).name} used {self.name}",
            particle=self.name,
            move_data=self.move,
        )
        if self.target_fainted:
            self.scene.add_effect(
                GenericEffect(self.scene, "But there was no target..")
            )
            return True, True, False
        if self.fail:
            self.scene.add_effect(GenericEffect(self.scene, "But it failed.."))
        if self.move_hit():
            return True, False, False
        return True, True, False

    def on_switch(self, target_old, target_new):
        if self.target == target_old:
            self.target = target_new
        return False, False, False

    def on_faint(self, target):
        if self.target == target:
            self.target_fainted = True
        return False, False, False
