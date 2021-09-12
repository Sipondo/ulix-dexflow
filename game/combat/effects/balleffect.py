from .baseeffect import BaseEffect
from .genericeffect import GenericEffect
from .endbattleeffect import EndBattleEffect
from ..pokefighter import PokeFighter
import math


STATUS_BONUSES = {
    "Paralysis": 1.5,
    "Sleep": 2.5,
    "Freeze": 2.5,
    "Burn": 1.5,
    "Poison": 1.5,
    "BadPoison": 1.5,
}


class BallEffect(BaseEffect):
    def __init__(self, scene, move):
        super().__init__(scene)
        self.spd_on_action = 100
        self.move = move
        self.user = move.user
        self.target = move.target
        self.ball = move.action_data

    def on_action(self):
        # print("BALL:", self.ball)
        if self.scene.battle_type == "trainer":
            print("Can't catch trainer pokes")
            return True, False, False
        mjr_status = [
            x
            for x in self.scene.get_effects_on_target(self.target)
            if x.type == "Majorstatus"
        ]
        if mjr_status:
            status_bonus = STATUS_BONUSES[mjr_status[0].name]
        else:
            status_bonus = 1
        ball_bonus = 1  # TEMP
        catch_actor = self.scene.board.get_actor(self.target)
        catch_rate = catch_actor.data["rareness"]
        hp_max = catch_actor.stats[0]
        hp_curr = self.scene.board.get_data(self.target).current_hp
        mod_catch_rate = (
            ((3 * hp_max - 2 * hp_curr) * catch_rate * ball_bonus) / (3 * hp_max)
        ) * status_bonus
        shake_chance = 1 / math.pow((255 / mod_catch_rate), 0.1875)
        fail = False
        counter = 0
        while not fail:
            if self.scene.board.random_roll() < shake_chance:
                counter += 1
            else:
                fail = True
            if counter > 3:
                self.scene.game.inventory.add_member(catch_actor.series)
                self.scene.board.add_member(catch_actor)
                self.scene.board.set_can_fight(self.target, False)
                self.scene.board.no_skip("", particle="pokeball-catch")
                self.scene.add_effect(
                    GenericEffect(self.scene, f"You caught {catch_actor.name}!", particle="")
                )
                self.scene.add_effect(EndBattleEffect(self.scene))
                return True, False, False
        self.scene.board.no_skip("", particle="pokeball-miss")
        self.scene.add_effect(
            GenericEffect(self.scene, f"{catch_actor.name} broke free!", particle="")
        )
        return True, False, False
