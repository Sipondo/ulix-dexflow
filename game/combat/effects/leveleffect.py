from .baseeffect import BaseEffect
from .learnmoveeffect import LearnMoveEffect


class LevelEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.spd_on_action = 95
        self.target = target

    def on_action(self):
        actor = self.scene.board.get_actor(self.target)
        current_hp = self.scene.board.get_data(self.target).current_hp
        old_max_hp = self.scene.board.get_data(self.target).max_hp
        self.scene.board.get_data(self.target).level += 1
        actor.level += 1
        new_max_hp = actor.stats[0]
        self.scene.board.get_data(self.target).max_hp = new_max_hp
        self.scene.board.set_hp(self.target, current_hp + (new_max_hp - old_max_hp))
        self.scene.board.set_exp(self.target, 0)

        new_level_exp = actor.get_level_exp()
        self.scene.board.get_data(self.target).exp_to_level = new_level_exp
        self.scene.board.get_data(self.target).current_exp = 0
        actor.level_xp = new_level_exp
        for level, move_name in actor.data["learnset"]:
            if actor.level == int(level):
                self.scene.add_effect(LearnMoveEffect(self.scene, self.target, move_name))
        self.scene.board.no_skip(f"{self.scene.board.get_actor(self.target).name} leveled up!", particle="level-up")
        # TODO show stats
        return True, False, False
