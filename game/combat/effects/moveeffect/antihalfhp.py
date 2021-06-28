from .basemoveeffect import BaseMoveEffect


class Antihalfhp(BaseMoveEffect):
    def before_move(self):
        target_hp = self.scene.board.get_hp(self.move.target)
        target_max_hp = self.scene.board.get_actor(self.move.target).stats[0]
        if target_hp <= target_max_hp//2:
            self.move.power *= 2
        return True
