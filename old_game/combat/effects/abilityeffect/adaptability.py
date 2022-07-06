from .baseabilityeffect import BaseAbilityEffect


class Adaptability(BaseAbilityEffect):
    name = "Adaptability"

    def on_hit(self, move):
        if self.active:
            if self.scene.current_action.user == self.holder:
                actor = self.scene.board.get_actor(self.holder)
                if actor.type1 == move.type or actor.type2 == move.type:
                    move.power = int(move.power * 4 / 3)
        return False
