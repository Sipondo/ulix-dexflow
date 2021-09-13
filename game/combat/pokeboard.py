import dataclasses
import copy

from .combatboard import CombatBoard
from .pokefighter import PokeFighter
from .effects.genericeffect import GenericEffect
from .effects.fainteffect import FaintEffect
from .effects.statuseffect import *


STATUS_CLASSES = {
    "badpoison": BadPoison,
    "poison": Poison,
    "sleep": Sleep,
    "freeze": Freeze,
    "burn": Burn,
    "paralysis": Paralysis,
}


@dataclasses.dataclass
class PokeFighterData:
    """Represents all variable data about a Pokémon during a battle."""

    level: int
    max_hp: int
    current_hp: int
    exp_to_level: int
    current_exp: int
    can_fight: bool
    turn_sent_out: int


class PokeBoard(CombatBoard):
    def __init__(self, game, scene):
        super().__init__(game, scene)
        # self.legal = pd.DataFrame(columns=["Pokemon", "Team", "Action", "Legal"])
        self.switch = []
        self.new_move = False

    def first_init(self, *teams):
        for i, team in enumerate(teams):
            team_formatted = []
            for j, poke in enumerate(team):
                poke_fighter = self.init_fighter(poke)
                data = PokeFighterData(
                    max_hp=poke_fighter.stats[0],
                    current_hp=poke_fighter.current_hp,
                    exp_to_level=poke_fighter.level_xp,
                    current_exp=poke_fighter.current_xp,
                    can_fight=poke_fighter.current_hp > 0,
                    level=poke_fighter.level,
                    turn_sent_out=0,
                )

                team_formatted.append((poke_fighter, data))

                # status conversion
                if poke_fighter.status is not None:
                    self.scene.add_effect(
                        STATUS_CLASSES[poke_fighter.status](self.scene, None, (i, j))
                    )

                # ability load
                try:
                    ability = self.scene.ability_lib[poke_fighter.ability.lower()](self.scene, (i, j))
                except KeyError:
                    ability = self.scene.ability_lib["noability"](self.scene, (i, j))
                self.scene.add_effect(ability)

            self.teams.append(team_formatted)

            # TODO empty field, send out pokemon at start of battle
            # find first alive poke
            self.actives.append(
                next(
                    idx
                    for idx, (poke, data) in enumerate(team_formatted)
                    if data.can_fight
                )
            )
            self.switch.append(False)

    def init_fighter(self, src):
        fighter = PokeFighter(self.game, self, src)
        return fighter

    def copy(self):
        newstate = PokeBoard(self.game, self.scene)
        newstate.from_board(self)
        newstate.switch = self.switch.copy()
        newstate.new_move = self.new_move
        # newstate.legal = self.legal.copy()
        return newstate

    def from_board(self, board):
        for index, team in enumerate(board.teams):
            self.teams.append([])
            for actor, data in team:
                member = (actor, dataclasses.replace(data))
                self.teams[index].append(member)
        self.actives = board.actives.copy()
        self.action = board.action
        self.user = board.user
        self.target = board.target

    def get_action_priority(self, action):
        prio = action.priority
        if action.user is None or action.target is None:
            # running or using balls
            return 7_000_000
        user_actor = self.get_actor(action.user)
        user_speed = user_actor.stats[0]
        for speed_mod in [
            x.stat_mod[4]
            for x in self.scene.get_effects_on_target(action.user)
            if x.name == "Statmod"
        ]:
            user_speed *= speed_mod
        return 1_000_000 * prio + user_speed

    def inflict_damage(self, target, damage):
        x, data = self.teams[target[0]][target[1]]
        damage = min(data.current_hp, damage)
        data.current_hp -= damage
        for effect in self.scene.get_effects_on_target(target):
            effect.on_damage(damage)
        if data.current_hp < 1:
            self.scene.add_effect(FaintEffect(self.scene, target))

    def inflict_status(self, status, user, target):
        for effect in self.scene.get_effects_on_target(target):
            if effect.on_status(target):
                return
        status_effect = status(self.scene, user, target)
        self.scene.add_effect(status_effect)
        if status_effect.apply_narration != "":
            particle = (
                status_effect.particle
                if status_effect.particle != ""
                else "generic-status"
            )
            self.scene.add_effect(
                GenericEffect(
                    self.scene,
                    f"{self.get_actor(target).name} {status_effect.apply_narration}!",
                    particle=particle,
                )
            )

    def catch_member(self, actor):
        # TODO not fully heal new member
        self.scene.game.inventory.add_member(actor.series, l=actor.level)

    def set_active(self, new_active):
        self.actives[new_active[0]] = new_active[1]
        self.teams[new_active[0]][new_active[1]][1].turn_sent_out = self.scene.round

    def is_active(self, target):
        return target[1] == self.actives[target[0]]

    def get_actor(self, target):
        # Get actor from (action) tuple
        return self.teams[target[0]][target[1]][0]

    def get_active(self, team):
        return self.actives[team]

    def get_active_round(self, team):
        return self.get_data((team, self.actives[team])).turn_sent_out

    def get_data(self, target) -> PokeFighterData:
        return self.teams[target[0]][target[1]][1]

    def set_hp(self, target, new_hp: int):
        self.teams[target[0]][target[1]][1].hp = new_hp

    def set_exp(self, target, new_exp: int):
        self.teams[target[0]][target[1]][1].current_exp = new_exp

    def set_level(self, target, new_level: int):
        self.teams[target[0]][target[1]][1].level = new_level

    def set_can_fight(self, target, b: bool):
        self.teams[target[0]][target[1]][1].can_fight = b

    def has_fighter(self, team):
        for mon, data in self.teams[team]:
            if data.can_fight:
                return True
        return False

    def get_relative_hp(self, target):
        return self.get_data(target).current_hp / self.get_data(target).max_hp

    def get_relative_xp(self, target):
        return self.get_data(target).current_exp / self.get_data(target).exp_to_level

    def sync_actor(self, target):
        actor = self.get_actor(target)
        actor.level = self.get_data(target).level
        actor.current_hp = self.get_data(target).current_hp
        actor.current_xp = self.get_data(target).current_exp
        if mjr_status := [
            x
            for x in self.scene.get_effects_on_target(target)
            if x.type == "Majorstatus"
        ]:
            actor.status = mjr_status[0].name.lower()

    @property
    def actor_1(self):
        if self.actives[0] == -1:
            return -1
        return self.teams[0][self.actives[0]][0]

    @property
    def actor_2(self):
        if self.actives[1] == -1:
            return -1
        return self.teams[1][self.actives[1]][0]
