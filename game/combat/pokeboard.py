from .combatboard import CombatBoard
from .effects.genericeffect import GenericEffect
from .effects.fainteffect import FaintEffect


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
        for team in teams:
            team_formatted = []
            for poke in team:
                # TODO EV gains during battle
                data = {"hp": poke.current_hp,
                        "exp": poke.current_xp,
                        "can_fight": True}
                team_formatted.append((poke, data))
            self.teams.append(team_formatted)
            self.actives.append((0, 0))
            self.switch.append(False)

    def inflict_damage(self, target, damage):
        x, data = self.teams[target[0]][target[1]]
        damage = min(data["hp"], damage)
        data["hp"] -= damage
        for effect in self.scene.get_effects_on_target(target):
            effect.on_damage(damage)
        if self.get_hp(target) < 1:
            self.scene.add_effect(FaintEffect(self.scene, target))

    def inflict_status(self, status, user, target):
        for effect in self.scene.get_effects_on_target(target):
            if effect.on_status(target):
                return
        status_effect = status(self.scene, user, target)
        self.scene.add_effect(status_effect)
        if status_effect.apply_narration != "":
            particle = status_effect.particle if status_effect.particle != "" else "generic-status"
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

    def get_hp(self, target):
        return self.teams[target[0]][target[1]][1]["hp"]

    def get_exp(self, target):
        return self.teams[target[0]][target[1]][1]["exp"]

    def set_exp(self, target, new_exp):
        self.teams[target[0]][target[1]][1]["exp"] = new_exp

    def get_can_fight(self, target):
        return self.teams[target[0]][target[1]][1]["can_fight"]

    def set_can_fight(self, target, b):
        self.teams[target[0]][target[1]][1]["can_fight"] = b

    def has_fighter(self, team):
        for mon, data in self.teams[team]:
            if data["can_fight"]:
                return True
        return False

    def get_relative_hp(self, target):
        return (
            self.get_hp(target)
            / self.teams[target[0]][target[1]][0].stats[0]
        )

    def get_relative_xp(self, target):
        return (
            self.get_exp(target)
            / self.teams[target[0]][target[1]][0].level_xp
        )

    def sync_actor(self, target):
        actor = self.get_actor(target)
        actor.current_hp = self.get_hp(target)
        actor.current_xp = self.get_exp(target)

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
