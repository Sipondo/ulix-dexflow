from .baseeffect import BaseEffect


class LevelEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.spd_on_action = 200
        self.target = target

    def on_action(self):
        self.scene.board.copy_actor(self.target)
        actor = self.scene.board.get_actor(self.target)
        actor.level += 1
        actor.current_xp = 0
        self.scene.board.set_exp(self.target, 0)
        actor.set_new_level_xp()
        self.scene.board.no_skip(f"{self.scene.board.get_actor(self.target).name} leveled up!", particle="")
        return True, False, False
