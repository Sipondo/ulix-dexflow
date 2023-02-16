import importlib

from kivy.resources import resource_find

from ulivy.c2.combatboard import CombatBoard
from ulivy.c2.action import ActionType, Action


class CombatManager:
    def __init__(self, game):
        self.game = game
        # load moves and ability effects
        self.effect_lib = {}
        self.ability_lib = {}

        self.init_move_effects()
        self.init_abilities()

        self.board_pointer = 0

        self.actions = []

    def init_move_effects(self):
        with open(resource_find("ulivy/combat/move.txt"), "r") as file:
            effects = file.read().split()

        for x in effects:
            if "basemoveeffect" in x or "init" in x:
                continue
            lib = importlib.import_module(
                f".{x}", package="ulivy.combat.effects.moveeffect"
            )
            self.effect_lib[x] = getattr(lib, x.capitalize())

    def init_abilities(self):
        with open(resource_find("ulivy/combat/ability.txt"), "r") as file:
            effects = file.read().split()

        for x in effects:
            if "baseabilityeffect" in x or "init" in x:
                continue
            lib = importlib.import_module(
                f".{x}", package="ulivy.combat.effects.abilityeffect"
            )
            self.ability_lib[x] = getattr(lib, x.capitalize())

    def init_new_stack(self):
        self.boards = [CombatBoard()]

    def advance(self):
        if self.board_pointer == len(self.boards) - 1:
            return False
        self.board_pointer += 1
        print(f"Advancing ({self.board_pointer}): {self.b.change}")

        # TEMP
        # if self.board.get_active_actor(i) != self.actors[i]:
        for i in range(2):
            if self.b.get_active_m(i) is None:
                self.game.m_gst.current_state.scene.set_fighter_image(
                    None, i
                )  # empty spriteset for if poke is fainted
            else:
                sprite = self.game.m_res.prepare_battle_animset(
                    f"{str(self.b.get_active_m(i).id).zfill(3)}"
                )
                self.game.m_gst.current_state.scene.set_fighter_image(sprite, i)

        # END TEMP

        if self.board_pointer == len(self.boards) - 1:
            return False
        return True

    def set_team(self, team_id, team):
        self.boards.append(self.board_head.set_team(team_id, team))

    def set_required_input(self, input):
        self.boards.append(self.board_head.set_required_input(input))

    def set_action(self, action):
        self.boards.append(self.board_head.set_action(action))
        # TODO TEMP

        self.actions.append(action)

        self.prepare_scene(self.actions)

    def prepare_scene(self, actions):
        # self.end = False
        # if self.battle_state == CombatState.BEFORE_START:
        #     self.round += 1
        print(actions)
        if actions is not None:
            for action in actions:
                if action.a_type == ActionType.ATTACK:
                    # TODO remove
                    # action.a_data["priority"] = 0
                    # END TODO

                    action.priority = 0
                    # action.priority = action.a_data.priority
            # Spawn all action effects
            # actions.sort(key=lambda x: self.b.get_action_priority(x))
            actions.sort(key=lambda x: x.priority)
            for action in actions:
                move_effect = self.spawn_action_effect(action)
                if move_effect:
                    self.action_effects.append((action, move_effect))
        return self.combat_state_methods[self.battle_state]()

    @property
    def b(self):
        return self.board_current

    @property
    def board_current(self):
        return self.boards[self.board_pointer]

    @property
    def board_head(self):
        return self.boards[-1]
