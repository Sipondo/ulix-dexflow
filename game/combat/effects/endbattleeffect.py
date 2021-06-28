from .baseeffect import BaseEffect


class EndBattleEffect(BaseEffect):
    def on_action(self):
        # TODO show battle rewards and stuff
        self.scene.board.no_skip("Battle ends!", particle="", battle_end=True)
        return False, False, True
