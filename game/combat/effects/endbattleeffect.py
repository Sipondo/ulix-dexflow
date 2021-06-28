from .baseeffect import BaseEffect


class EndBattleEffect(BaseEffect):
    def on_action(self):
        self.scene.board.no_skip("Battle ends!", particle="Battleend", battle_end=True)
        return False, False, True
