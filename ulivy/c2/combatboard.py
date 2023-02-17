import enum
import random

from dataclasses import replace, dataclass, fields
from .combatteam import CombatTeam
from .combatfighter import CombatFighter

from ulivy.c2.action import ActionType, Action


class Input(enum.Enum):
    NONE = enum.auto()
    TURN = enum.auto()


@dataclass(frozen=True)
class CombatBoard:
    change = "No change description available."
    parent = None
    required_input = Input.NONE
    teams = (CombatTeam(), CombatTeam())
    actives = (0, 0)
    effects = ()
    action_effects = ()

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def copy(self, **changes):
        changes = {**self.__dict__, **changes}
        return replace(self, **changes)

    def set_change(self, change):
        return self.copy(
            change=change,
        )

    def set_team(self, team_id, team):
        entry = []

        for t in team:
            if isinstance(t, dict):
                entry.append(t)
            else:
                entry.append(t.to_dict())

        teams = list(self.teams)

        new_team = CombatTeam(members=tuple(CombatFighter(**x) for x in entry))
        teams[team_id] = new_team  # teams[team_id].copy(**changes)

        b = self.copy(
            teams=tuple(teams),
            change=f"Team changed: team_id {team_id} changed to {[x.name for x in new_team.members]}",
            # change=f"Team changed: team_id {team_id} swapped from \n{self.teams[team_id]} to \n{entry}",
        )
        # b.teams[team_id] = entry  # TODO: fix
        return b

    def inflict_damage(self, target, damage, lethal=True, user=None):
        # if user is not None:
        #     user_actor = self.get_actor(user)
        #     if user_actor.current_hp <= 0:
        #         return

        x = self.get_m(target)
        prev_hp = x.current_hp
        damage = min(x.current_hp, damage)

        # print("X PRE", x.__dict__)
        x = x.copy(current_hp=x.current_hp - damage)
        # print("X POST", x.__dict__)

        teams = list(self.teams)
        team = list(teams[target[0]].members)

        team[target[1]] = x
        teams[target[0]] = CombatTeam(members=tuple(team))

        b = self.copy(
            teams=tuple(teams),
            change=f"Inflicted damage: target {target} took {damage} and went from {prev_hp} to {x.current_hp} hp.",
            # change=f"Team changed: team_id {team_id} swapped from \n{self.teams[team_id]} to \n{entry}",
        )
        # x.current_hp -= damage

        # for effect in self.scene.get_effects_on_target(target):
        #     effect.on_damage(damage)
        # if data.current_hp < 1:
        #     if lethal:
        #         self.scene.add_effect(FaintEffect(self.scene, target))
        #     else:
        #         data.current_hp = 1
        return b

    def set_required_input(self, input):
        return self.copy(
            required_input=input,
            change=f"Required input changed: {self.required_input} to {input}",
        )

    def get_m(self, id):
        return self.teams[id[0]].members[id[1]]

    def get_active_m(self, team_id):
        if self.actives[team_id] < len(self.teams[team_id].members):
            return self.teams[team_id].members[self.actives[team_id]]
        return None

    def set_action(self, action: Action):
        if self.required_input == Input.TURN:
            return self.copy(
                required_input=Input.NONE,
                change=f"Required input resolved: {self.required_input} to {Input.NONE}",
            )
        else:
            raise Exception(
                f"Combatboard received unexpected input even though {self.required_input} was expected!"
            )

    def add_effect(self, effect):
        return self.copy(
            effects=tuple(list(self.effects) + [effect]),
            change=f"Added effect {effect}.",
        )

    def delete_effect(self, effect):
        effect_str = str(effect)
        effect.on_delete()
        effects = list(self.effects)
        effects.remove(effect)
        del effect

        return self.copy(
            effects=tuple(effects),
            change=f"Deleted effect {effect_str}.",
        )

    def add_action_effect(self, effect):
        return self.copy(
            action_effects=tuple(list(self.action_effects) + [effect]),
            change=f"Added action effect {effect}.",
        )

    def reset_effects_done(self):
        # TODO: these effects should be static and need to be copied
        effects = tuple((x for x in self.effects))
        for effect in effects:
            effect.done = False

        return self.copy(
            effects=effects,
            change=f"Reset all effects done.",
        )

    def reset_effects_skip(self):
        # TODO: these effects should be static and need to be copied
        effects = tuple((x for x in self.effects))
        for effect in effects:
            effect.skip = False

        return self.copy(
            effects=effects,
            change=f"Reset all effects skip.",
        )

    def pop_action_effect(self):
        action_effects = list(self.action_effects)
        effect = action_effects.pop()
        return (
            self.copy(
                action_effects=tuple(action_effects),
                change=f"Popped action effect {effect}.",
            ),
            effect,
        )

    def random_int(self, a, b):
        return random.randint(a, b)

    def random_float(self):
        return random.random()

    def random_roll(self, chance: float):
        return self.random_float() <= chance
