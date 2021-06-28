from game.combat.effects.baseeffect import BaseEffect


class ChargeEffect(BaseEffect):
    def __init__(self, scene, target):
        super().__init__(scene)
        self.target = target
        self.count = 1

    def on_switch(self, target_old, target_new):
        return self.target == target_old, False, False

    def on_faint(self, target):
        return self.target == target, False, False

    def on_end_turn(self):
        if self.count == 0:
            return True
        self.count -= 1

    @property
    def stat_mod(self):
        if self.scene.board.action[0].type == "Electric":
            return [2, 1, 2, 1, 1, 1, 1]
        return [1, 1, 1, 1, 1, 1, 1]
