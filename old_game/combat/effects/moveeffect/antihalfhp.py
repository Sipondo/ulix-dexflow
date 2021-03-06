from .basemoveeffect import BaseMoveEffect


class Antihalfhp(BaseMoveEffect):
    def before_action(self):
        target_hp = self.scene.board.get_data(self.move.target).current_hp
        target_max_hp = self.scene.board.get_actor(self.move.target).stats[0]
        if target_hp <= target_max_hp//2:
            self.move.power *= 2
        return True, False, False
