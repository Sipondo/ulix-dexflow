from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect


class Avghp(BaseMoveEffect):
    def after_action(self):
        user_hp = self.scene.board.get_data(self.move.user).current_hp
        user_max_hp = self.scene.board.get_actor(self.move.user).stats[0]
        target_hp = self.scene.board.get_data(self.move.target).current_hp
        target_max_hp = self.scene.board.get_actor(self.move.target).stats[0]

        average = (user_hp + target_hp) // 2
        self.scene.board.set_hp(self.move.user, min(average, user_max_hp))
        self.scene.board.set_hp(self.move.target, min(average, target_max_hp))
        return True, False, False
