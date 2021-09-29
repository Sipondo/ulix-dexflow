from .pokeboard import PokeBoard
from .effects.mainmoveeffect import MainMove
from .effects.runeffect import RunEffect
from .effects.switcheffect import SwitchEffect
from .effects.balleffect import BallEffect
from .effects.sendouteffect import SendOutEffect
from .effects.forgetmoveeffect import ForgetMoveEffect
from .effects.moveeffect.basemoveeffect import BaseMoveEffect
from .effects.abilityeffect.baseabilityeffect import BaseAbilityEffect

import types
import importlib
from pathlib import Path
from enum import IntEnum

EFFECTS_PATH = Path("game/combat/effects/")


class CombatState(IntEnum):
    IDLE = 0
    BEFORE_START = 1
    ACTION = 2
    BEFORE_END = 3
    SWITCH_IDLE = 4
    SWITCH = 5


class CombatScene:
    def __init__(self, game, team_1, team_2, battle_type="trainer"):

        self.game = game

        # load moves and ability effects
        self.effect_lib = {}
        self.ability_lib = {}

        self.init_move_effects()
        self.init_abilities()

        # prepare first board
        self.board_history = [PokeBoard(self.game, self)]
        self.effects = []
        self.board.first_init(team_1, team_2)
        self.board_graveyard = []
        self.battle_type = battle_type
        self.round = 0
        self.end = False

        self.battle_state = CombatState.SWITCH_IDLE
        self.combat_state_methods = {
            CombatState.IDLE: self.prepare_scene,
            CombatState.BEFORE_START: self.run_start,
            CombatState.ACTION: self.run_actions,
            CombatState.BEFORE_END: self.run_end,
            CombatState.SWITCH_IDLE: self.prepare_scene,
            CombatState.SWITCH: self.run_switches,
        }

        self.action_effects = []
        self.current_action = None
        self.current_action_effect = None

    def init_move_effects(self):
        for x in (EFFECTS_PATH / "moveeffect").glob("*.py"):
            if "basemoveeffect" in x.stem or "init" in x.stem:
                continue
            lib = importlib.import_module(
                f".{x.stem}", package="game.combat.effects.moveeffect"
            )
            self.effect_lib[x.stem] = getattr(lib, x.stem.capitalize())

    def init_abilities(self):
        for x in (EFFECTS_PATH / "abilityeffect").glob("*.py"):
            if "baseabilityeffect" in x.stem or "init" in x.stem:
                continue
            lib = importlib.import_module(
                f".{x.stem}", package="game.combat.effects.abilityeffect"
            )
            self.ability_lib[x.stem] = getattr(lib, x.stem.capitalize())

    def prepare_scene(self, action_descriptions=None):
        self.end = False
        if self.battle_state == CombatState.IDLE:
            self.round += 1
        if action_descriptions is not None:
            actions = self.format_actions(action_descriptions)

            # Spawn all action effects
            actions.sort(key=lambda x: self.board.get_action_priority(x))
            for action in actions:
                move_effect = self.spawn_action_effect(action)
                self.action_effects.append((action, move_effect))
        return self.next_state()

    def next_state(self):
        self.reset_effects_done()
        self.battle_state = CombatState((self.battle_state + 1) % len(CombatState))
        if self.battle_state == CombatState.SWITCH_IDLE:
            if any(self.board.switch):
                return self.end_actions()
        if self.battle_state == CombatState.IDLE:
            return self.end_actions()
        return self.combat_state_methods[self.battle_state]()

    def run_start(self):
        print("BEFORE START")
        while effects := [
            x
            for x in sorted(self.effects, key=lambda x: -x.spd_before_start)
            if not x.done and not x.skip
        ]:
            self.run_effect(effects[0], effects[0].before_start)

        self.reset_effects_done()
        if self.end:
            return self.end_actions()
        return self.next_state()

    def run_actions(self):
        print("BEFORE ACTIONS")
        while self.action_effects and not self.end:
            self.current_action, self.current_action_effect = self.action_effects.pop()
            self.board.action = self.current_action
            # dit is alleen om in de state de huidige 'actor' aan te geven
            self.board.set_direction(self.current_action_effect)

            # TODO skip is scary. It might introduce bugs where effects are supposed to happen but don't. Should rework

            skip = False

            # Before action
            while effects := [
                x
                for x in sorted(self.effects, key=lambda x: -x.spd_before_action)
                if not x.done and not x.skip
            ]:
                if issubclass(type(effects[0]), BaseMoveEffect):
                    if effects[0].move.user != self.current_action.user:
                        effects[0].done = True
                        continue
                skip = self.run_effect(effects[0], effects[0].before_action)

            self.reset_effects_done()

            # On action
            if skip:
                continue

            while effects := [
                x
                for x in sorted(self.effects, key=lambda x: -x.spd_on_action)
                if not x.done and not x.skip
            ]:
                if issubclass(type(effects[0]), BaseMoveEffect):
                    if effects[0].move.user != self.current_action.user:
                        effects[0].done = True
                        continue
                skip = self.run_effect(effects[0], effects[0].on_action)

            self.reset_effects_done()

            # After action
            if skip:
                continue
            while effects := [
                x
                for x in sorted(self.effects, key=lambda x: -x.spd_after_action)
                if not x.done and not x.skip
            ]:
                if issubclass(type(effects[0]), BaseMoveEffect):
                    if effects[0].move.user != self.current_action.user:
                        effects[0].done = True
                        continue
                self.run_effect(effects[0], effects[0].after_action)
        self.board.reset_action()

        if self.end:
            return self.end_actions()
        return self.next_state()

    def run_end(self):
        print("BEFORE END")
        while effects := [
            x
            for x in sorted(self.effects, key=lambda x: -x.spd_before_end)
            if not x.done and not x.skip
        ]:
            self.run_effect(effects[0], effects[0].before_end)

        if self.end:
            return self.end_actions()
        return self.next_state()

    def run_switches(self):
        print("BEFORE SWITCHES")
        while effects := [
            x
            for x in sorted(self.effects, key=lambda x: -x.spd_switch_phase)
            if not x.done and not x.skip
        ]:
            self.run_effect(effects[0], effects[0].switch_phase)

        if self.end:
            return self.end_actions()
        return self.next_state()

    def end_actions(self):
        self.reset_effects_done()
        self.reset_effects_skip()
        self.board_graveyard.extend(self.board_history)
        board_history = self.board_history

        self.new_board()
        self.board_history = [self.board]
        return board_history

    def reset_effects_done(self):
        for effect in self.effects:
            effect.done = False

    def reset_effects_skip(self):
        for effect in self.effects:
            effect.skip = False

    def run_effect(self, effect, f, *args):
        effect.done = True
        self.new_board()
        if args:
            delete, skip, end = f(*args)
        else:
            delete, skip, end = f()
        if delete:
            self.delete_effect(effect)
        if end:
            self.end = True
        return skip

    def add_effect(self, effect):
        self.effects.append(effect)

    def remove_action_effects(self, target):
        for (move_effect, action) in self.action_effects:
            if move_effect.user == target:
                self.action_effects.remove((move_effect, action))

    def spawn_action_effect(self, action):
        effect = None
        if action.action_name == "attack":
            effect = MainMove(self, action)
        elif action.action_name == "flee":
            effect = RunEffect(self, action)
        elif action.action_name == "swap":
            effect = SwitchEffect(self, action)
        elif action.action_name == "catch":
            effect = BallEffect(self, action)
        elif action.action_name == "sendout":
            effect = SendOutEffect(self, action.action_data)
        elif action.action_name == "forget_move":
            effect = ForgetMoveEffect(self, action)
        self.effects.append(effect)
        return effect

    def on_switch_effects(self, old, new):
        for effect in [x for x in sorted(self.effects, key=lambda x: -x.spd_on_switch)]:
            delete = self.run_effect(effect, effect.on_switch, old, new)
            if delete:
                self.delete_effect(effect)
        self.reset_effects_done()

    def on_send_out_effects(self, target):
        for effect in [
            x for x in sorted(self.effects, key=lambda x: -x.spd_on_send_out)
        ]:
            delete = self.run_effect(effect, effect.on_send_out, target)
            if delete:
                self.delete_effect(effect)
        self.reset_effects_done()

    def on_faint_effects(self, target):
        for effect in [x for x in sorted(self.effects, key=lambda x: -x.spd_on_faint)]:
            delete = self.run_effect(effect, effect.on_faint, target)
            if delete:
                self.delete_effect(effect)
        self.reset_effects_done()

    def on_crit_effects(self, target):
        for effect in [x for x in sorted(self.effects, key=lambda x: -x.spd_on_crit)]:
            delete = self.run_effect(effect, effect.on_crit, target)
            if delete:
                self.delete_effect(effect)
        self.reset_effects_done()

    def is_grounded(self, target):
        actor = self.board.get_actor(target)
        grounded = not(actor.type1 == "FLYING" or actor.type2 == "FLYING")
        for effect in [x for x in sorted(self.effects, key=lambda x: -x.spd_grounded)]:
            g = self.run_effect(effect, effect.grounded, target)
            if g is not None:
                grounded = g
        return grounded

    def get_action_effect(self, target):
        for action, effect in self.action_effects:
            if action.user == target:
                return action, effect
        return None, None

    def get_effects(self):
        return self.effects

    def get_global_effects(self):
        return [x for x in self.effects if x.target == "Global"]

    def get_effects_on_target(self, target, exclusive=False):
        if exclusive:
            return [
                x for x in self.effects if x.target == target
            ]  # only the target itself
        return [
            x for x in self.effects if x.target == target or x.target == target[0]
        ]  # target team or target itself

    def get_target_abilities(self, target):
        return [
            x
            for x in self.effects
            if x.target == target and issubclass(type(x), BaseAbilityEffect)
        ]

    def get_effects_by_name(self, effect_name):
        return [x for x in self.effects if x.name == effect_name]

    def get_effects_by_type(self, effect_type):
        return [x for x in self.effects if x.type == effect_type]

    def delete_effect(self, effect):
        effect.on_delete()
        self.effects.remove(effect)
        del effect

    def get_actor(self, team):
        return self.board.get_actor(self.board.get_active(team))

    def new_board(self):
        new_board = self.board.copy()
        self.board_history.append(new_board)

    def format_actions(self, action_descriptions):
        actions = []
        for (name, action), user, target in action_descriptions:
            if name == "attack":
                action = action.copy()
                action.action_name = name
                action["user"] = user
                action["target"] = target
                actions.append(action)
            else:
                # FLEE, CATCH, SWITCH, SEND OUT, FORGET MOVE
                action_data = action
                action = types.SimpleNamespace()
                action.action_data = action_data
                action.action_name = name
                action.user = user
                action.target = target
                action.priority = 6
                actions.append(action)
        return actions

    @property
    def board(self):
        return self.board_history[-1]
