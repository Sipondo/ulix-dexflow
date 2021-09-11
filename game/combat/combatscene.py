from .pokefighter import PokeFighter
from .pokeboard import PokeBoard
from .effects.mainmoveeffect import MainMove
from .effects.runeffect import RunEffect
from .effects.switcheffect import SwitchEffect
from .effects.balleffect import BallEffect
from .effects.sendouteffect import SendOutEffect
from .effects.forgetmoveeffect import ForgetMoveEffect

import types
import importlib
from pathlib import Path

EFFECTS_PATH = Path("game/combat/effects/")


class CombatScene:
    def __init__(self, game, team_1, team_2, battle_type="trainer"):

        self.game = game
        self.board_history = [PokeBoard(self)]
        self.effects = []
        t1 = self.init_team(team_1)
        t2 = self.init_team(team_2)
        self.init_board(t1, t2)
        self.teams = [t1, t2]
        self.board_graveyard = []
        self.battle_type = battle_type
        self.round = 0
        self.end = False

        self.effect_lib = {}
        self.ability_lib = {}

        self.action_effects = []
        self.current_action = None
        self.current_action_effect = None

        self.init_move_effects()
        self.init_abilities()

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

    def init_board(self, team_1, team_2):
        self.board.first_init(team_1, team_2)

    def init_team(self, team):
        return [self.init_fighter(x) for x in team]

    def init_fighter(self, src):
        fighter = PokeFighter(self.game, self, src)

        return fighter

    def run_scene(self, action_descriptions=None, next_round=True):
        self.end = False
        if next_round:
            self.round += 1
        if action_descriptions:
            actions = self.format_actions(action_descriptions)

            # Spawn all action effects
            actions.sort(key=lambda x: self.board.get_action_priority(x))
            for action in actions:
                move_effect = self.spawn_action_effect(action)
                self.action_effects.append((action, move_effect))
        # print("Actions:", actions)

        # After select
        # for effect in sorted(self.effects, key=lambda x: -x.spd_after_select):
        #     self.run_effect(effect, effect.after_select)
        # self.reset_effects_done()

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
                self.run_effect(effects[0], effects[0].after_action)
        self.board.reset_action()

        # Before end
        if not self.end:
            while effects := [
                x
                for x in sorted(self.effects, key=lambda x: -x.spd_before_end)
                if not x.done and not x.skip
            ]:
                self.run_effect(effects[0], effects[0].before_end)

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

    def on_send_out_effects(self, target):
        for effect in [
            x for x in sorted(self.effects, key=lambda x: -x.spd_on_send_out)
        ]:
            delete = self.run_effect(effect, effect.on_send_out, target)
            if delete:
                self.delete_effect(effect)

    def on_faint_effects(self, target):
        for effect in [x for x in sorted(self.effects, key=lambda x: -x.spd_on_faint)]:
            delete = self.run_effect(effect, effect.on_faint, target)
            if delete:
                self.delete_effect(effect)

    def get_effects(self):
        return self.effects

    def get_global_effects(self):
        return [x for x in self.effects if x.target == "Global"]

    def get_effects_on_target(self, target):
        return [x for x in self.effects if x.target == target]

    def get_effects_by_name(self, effect_name):
        return [x for x in self.effects if x.name == effect_name]

    def get_effects_by_type(self, effect_type):
        return [x for x in self.effects if x.type == effect_type]

    def delete_effect(self, effect):
        effect.on_delete()
        self.effects.remove(effect)
        del effect

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
