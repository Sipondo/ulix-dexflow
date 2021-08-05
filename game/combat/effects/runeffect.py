from .baseeffect import BaseEffect
from .genericeffect import GenericEffect
from .endbattleeffect import EndBattleEffect
from .runcountereffect import RunCounterEffect


class RunEffect(BaseEffect):
    def __init__(self, scene, action):
        super().__init__(scene)
        if effects := self.scene.get_effects_by_name("Runcounter"):
            self.counter = effects[0].counter
        else:
            self.counter = 1
        self.user = action.user
        self.target = action.target

    def on_action(self):
        user_actor = self.scene.board.get_actor(self.user)
        target_actor = self.scene.board.get_actor(self.target)
        user_speed = user_actor.stats[5]
        for speed_mod in [mod_effect.stat_mod[4] for mod_effect in self.scene.get_effects_on_target(self.user)]:
            user_speed *= speed_mod
        target_speed = target_actor.stats[5]
        for speed_mod in [mod_effect.stat_mod[4] for mod_effect in self.scene.get_effects_on_target(self.target)]:
            target_speed *= speed_mod
        attempt_n = self.counter
        escape_chance = user_speed * 32 // ((target_speed // 4) % 256) + 30 * attempt_n
        if self.scene.board.random_roll() < escape_chance:
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.scene.board.get_actor(self.user).name} ran away!",
                )
            )
            self.scene.add_effect(EndBattleEffect(self.scene))
            return True, False, True
        if effects := self.scene.get_effects_by_name("Runcounter"):
            effects[0].counter += 1
        else:
            self.scene.add_effect(RunCounterEffect(self.scene, self.counter))
        self.scene.add_effect(
            GenericEffect(
                self.scene,
                f"{self.scene.board.get_actor(self.user).name} couldn't escape!",
            )
        )
        return True, False, False
