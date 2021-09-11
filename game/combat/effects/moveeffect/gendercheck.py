from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect


class Gendercheck(BaseMoveEffect):
    def before_action(self):
        user_gender = self.scene.board.get_actor(self.move.user).gender
        target_gender = self.scene.board.get_actor(self.move.target).gender
        if user_gender not in ("Male", "Female"):
            return False
        if target_gender not in ("Male", "Female"):
            return False
        if user_gender == target_gender:
            return False
        return True
