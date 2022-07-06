from game.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect


class Gendercheck(BaseMoveEffect):
    def before_action(self):
        user_gender = self.scene.board.get_actor(self.move.user).gender
        target_gender = self.scene.board.get_actor(self.move.target).gender
        if user_gender in ("Male", "Female"):
            if target_gender in ("Male", "Female"):
                if user_gender != target_gender:
                    return True, False, False
        self.move.fail = True
        return True, False, False
