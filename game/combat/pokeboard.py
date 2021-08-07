from .combatboard import CombatBoard
from .effects.genericeffect import GenericEffect
from .effects.fainteffect import FaintEffect
from .effects.statuseffect import *


STATUS_CLASSES = {"badpoison": BadPoison,
                  "poison": Poison,
                  "sleep": Sleep,
                  "freeze": Freeze,
                  "burn": Burn,
                  "paralysis": Paralysis}


class PokeBoard(CombatBoard):
    def __init__(self, scene):
        super().__init__(scene)
        # self.legal = pd.DataFrame(columns=["Pokemon", "Team", "Action", "Legal"])
        self.switch = []
        self.new_move = False

    def copy(self):
        newstate = PokeBoard(self.scene)
        newstate.from_board(self)
        newstate.switch = self.switch.copy()
        newstate.new_move = self.new_move
        # newstate.legal = self.legal.copy()
        return newstate

    def first_init(self, *teams):
        for i, team in enumerate(teams):
            team_formatted = []
            for j, poke in enumerate(team):
                data = {
                    "hp": poke.current_hp,
                    "exp": poke.current_xp,
                    "can_fight": True,
                    "level": poke.level,
                }
                team_formatted.append((poke, data))
                if poke.status is not None:
                    self.scene.add_effect(STATUS_CLASSES[poke.status](self.scene, None, (i, j)))
            self.teams.append(team_formatted)
            self.actives.append((0, 0))
            self.switch.append(False)

    def get_action_priority(self, action):
        prio = action.priority
        if action.user is None or action.target is None:
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
        damage = min(data["hp"], damage)
        data["hp"] -= damage
        for effect in self.scene.get_effects_on_target(target):
            effect.on_damage(damage)
        if self.get_data(target)["hp"] < 1:
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

    def set_active(self, new_active):
        self.actives[new_active[0]] = (new_active[1], self.scene.round)

    def is_active(self, target):
        return target[1] == self.actives[target[0]][0]

    def get_active(self, team):
        return self.actives[team][0]

    def get_active_round(self, team):
        return self.actives[team][1]

    def get_data(self, target):
        return self.teams[target[0]][target[1]][1]

    def set_exp(self, target, new_exp):
        self.teams[target[0]][target[1]][1]["exp"] = new_exp

    def set_level(self, target, new_level):
        self.teams[target[0]][target[1]][1]["level"] = new_level

    def set_can_fight(self, target, b):
        self.teams[target[0]][target[1]][1]["can_fight"] = b

    def has_fighter(self, team):
        for mon, data in self.teams[team]:
            if data["can_fight"]:
                return True
        return False

    def get_relative_hp(self, target):
        return self.get_data(target)["hp"] / self.teams[target[0]][target[1]][0].stats[0]

    def get_relative_xp(self, target):
        return self.get_data(target)["exp"] / self.teams[target[0]][target[1]][0].level_xp

    def sync_actor(self, target):
        actor = self.get_actor(target)
        actor.current_hp = self.get_data(target)["hp"]
        actor.current_xp = self.get_data(target)["exp"]
        actor.level = self.get_data(target)["level"]
        if mjr_status := [x for x in self.scene.get_effects_on_target(target) if x.type == "Majorstatus"]:
            actor.status = mjr_status[0].name.lower()

    @property
    def actor_1(self):
        if self.actives[0][0] == -1:
            return -1
        return self.teams[0][self.actives[0][0]]

    @property
    def actor_2(self):
        if self.actives[1][0] == -1:
            return -1
        return self.teams[1][self.actives[1][0]]
