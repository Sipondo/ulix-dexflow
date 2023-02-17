import importlib
import typing

from enum import IntEnum

from kivy.resources import resource_find

from ulivy.c2.combatboard import CombatBoard
from ulivy.c2.action import ActionType, Action

from ulivy.combat.effects.mainmoveeffect import MainMove
from ulivy.combat.effects.runeffect import RunEffect
from ulivy.combat.effects.switcheffect import SwitchEffect
from ulivy.combat.effects.balleffect import BallEffect
from ulivy.combat.effects.sendouteffect import SendOutEffect
from ulivy.combat.effects.forgetmoveeffect import ForgetMoveEffect
from ulivy.combat.effects.moveeffect.basemoveeffect import BaseMoveEffect
from ulivy.combat.effects.abilityeffect.baseabilityeffect import BaseAbilityEffect


class CombatState(IntEnum):
    BEFORE_START = 0
    ACTION = 1
    BEFORE_END = 2
    SWITCH = 3


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
        self.action_type_effects = {
            ActionType.ATTACK: MainMove,
            ActionType.CATCH: BallEffect,
            ActionType.RUN: RunEffect,
            ActionType.SWITCH: SwitchEffect,
            ActionType.SENDOUT: SendOutEffect,
            ActionType.FORGET_MOVE: ForgetMoveEffect,
            ActionType.NOTHING: None,
        }

        # self.action_effects = []
        # self.effects = []

        self.battle_state = CombatState.BEFORE_START  # ACTION
        self.combat_state_methods = {
            CombatState.BEFORE_START: self.run_start,
            CombatState.ACTION: self.run_actions,
            CombatState.BEFORE_END: self.run_end,
            CombatState.SWITCH: self.run_switches,
        }

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

    def set_change(self, change):
        self.boards.append(self.h.set_change(change))

    def set_team(self, team_id, team):
        self.boards.append(self.h.set_team(team_id, team))

    def inflict_damage(self, target, damage, lethal=True, user=None):
        self.boards.append(self.h.inflict_damage(target, damage, lethal, user))

    def set_required_input(self, input):
        self.boards.append(self.h.set_required_input(input))

    def set_action(self, action):
        self.boards.append(self.h.set_action(action))

        # TODO TEMP
        self.actions = []

        self.actions.append(action)

        self.prepare_scene(self.actions)
        # END TODO

    def add_effect(self, effect):
        self.boards.append(self.h.add_effect(effect))

    def add_action_effect(self, effect):
        self.boards.append(self.h.add_action_effect(effect))

    def pop_action_effect(self):
        board, effect = self.h.pop_action_effect()
        self.boards.append(board)
        return effect

    def prepare_scene(self, actions):
        # # TODO: remove
        # self.effects = []
        # self.action_effects = []
        # # end TODO

        self.end = False
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
                    # self.action_effects.append((action, move_effect))
                    self.add_action_effect((action, move_effect))
        return self.combat_state_methods[self.battle_state]()

    def remove_action_effects(self, target):
        for (move_effect, action) in self.action_effects:
            if move_effect.user == target:
                self.action_effects.remove((move_effect, action))

    def spawn_action_effect(self, action):
        effect = self.action_type_effects[action.a_type]
        if effect:
            effect = effect(self, action)
            # self.effects.append(effect)
            self.add_effect(effect)
        return effect

    def run_start(self) -> typing.List[CombatBoard]:
        print("BEFORE START")
        while effects := [
            x
            for x in sorted(self.h.effects, key=lambda x: -x.spd_before_start)
            if not x.done and not x.skip
        ]:
            self.run_effect(effects[0], effects[0].before_start)

        self.reset_effects_done()
        if self.end:
            return self.end_actions()
        return self.next_state()

    def run_actions(self) -> typing.List[CombatBoard]:
        print("BEFORE ACTIONS")
        while self.h.action_effects and not self.end:
            (
                self.current_action,
                self.current_action_effect,
            ) = self.pop_action_effect()
            # self.board.action = self.current_action
            # dit is alleen om in de state de huidige 'actor' aan te geven
            # self.board.set_direction(self.current_action_effect)

            # TODO skip is scary. It might introduce bugs where effects are supposed to happen but don't. Should rework

            skip = False

            # Before action
            while effects := [
                x
                for x in sorted(self.h.effects, key=lambda x: -x.spd_before_action)
                if not x.done and not x.skip
            ]:
                if issubclass(type(effects[0]), BaseMoveEffect):
                    if effects[0].move.user != self.current_action.user:
                        effects[0].done = True
                        continue
                skip = self.run_effect(effects[0], effects[0].before_action)
                if skip:
                    break

            self.reset_effects_done()

            # On action
            if skip:
                continue

            while effects := [
                x
                for x in sorted(self.h.effects, key=lambda x: -x.spd_on_action)
                if not x.done and not x.skip
            ]:
                if issubclass(type(effects[0]), BaseMoveEffect):
                    if effects[0].move.user != self.current_action.user:
                        effects[0].done = True
                        continue
                skip = self.run_effect(effects[0], effects[0].on_action)
                if skip:
                    break

            self.reset_effects_done()

            # After action
            if skip:
                continue
            while effects := [
                x
                for x in sorted(self.h.effects, key=lambda x: -x.spd_after_action)
                if not x.done and not x.skip
            ]:
                if issubclass(type(effects[0]), BaseMoveEffect):
                    if effects[0].move.user != self.current_action.user:
                        effects[0].done = True
                        continue
                self.run_effect(effects[0], effects[0].after_action)
                if skip:
                    break
        # self.board.reset_action()

        if self.end:
            return self.end_actions()
        return self.next_state()

    def run_end(self) -> typing.List[CombatBoard]:
        print("BEFORE END")
        while effects := [
            x
            for x in sorted(self.h.effects, key=lambda x: -x.spd_before_end)
            if not x.done and not x.skip
        ]:
            self.run_effect(effects[0], effects[0].before_end)

        if self.end:
            return self.end_actions()
        return self.next_state()

    def run_switches(self) -> typing.List[CombatBoard]:
        print("BEFORE SWITCHES")
        while effects := [
            x
            for x in sorted(self.h.effects, key=lambda x: -x.spd_switch_phase)
            if not x.done and not x.skip
        ]:
            self.run_effect(effects[0], effects[0].switch_phase)

        if self.end:
            return self.end_actions()
        return self.next_state()

    def run_effect(self, effect, f, *args):
        print("EFFECT", effect)
        effect.done = True
        # self.new_board()
        if args:
            delete, skip, end = f(*args)
        else:
            delete, skip, end = f()
        if delete:
            self.delete_effect(effect)
        if end:
            self.end = True
        return skip

    def next_state(self) -> typing.List[CombatBoard]:
        self.reset_effects_done()
        self.battle_state = CombatState((self.battle_state + 1) % len(CombatState))
        # TODO: re-enable
        # if self.battle_state == CombatState.SWITCH:
        #     if self.board.fainted:
        #         return self.end_actions()
        if self.battle_state == CombatState.BEFORE_START:
            return self.end_actions()
        return self.combat_state_methods[self.battle_state]()

    def end_actions(self) -> typing.List[CombatBoard]:
        self.reset_effects_done()
        self.reset_effects_skip()
        # self.mgr_agent.start_agents()
        # self.board_graveyard.extend(self.board_history)
        # board_history = self.board_history

        # self.new_board()
        # self.board_history = [self.board]
        return self.b  # board_history

    def reset_effects_done(self):
        self.boards.append(self.h.reset_effects_done())
        # for effect in self.effects:
        #     effect.done = False

    def reset_effects_skip(self):
        self.boards.append(self.h.reset_effects_skip())
        # for effect in self.effects:
        #     effect.skip = False

    def get_effects_on_target(self, target, exclusive=False):
        if exclusive:
            # only the target itself
            return [x for x in self.h.effects if x.target == target]
        # target team or target itself
        return [
            x for x in self.h.effects if x.target == target or x.target == target[0]
        ]

    # def add_effect(self, effect):
    #     self.effects.append(effect)

    def delete_effect(self, effect):
        self.boards.append(self.h.delete_effect(effect))
        # effect.on_delete()
        # self.effects.remove(effect)
        # del effect

    @property
    def h(self):
        return self.boards[-1]

    @property
    def b(self):
        return self.board_current

    @property
    def board_current(self):
        return self.boards[self.board_pointer]
