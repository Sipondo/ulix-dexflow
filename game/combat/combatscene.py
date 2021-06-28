from .pokefighter import PokeFighter
from .pokeboard import PokeBoard
from .effects.mainmoveeffect import MainMove
from .effects.runeffect import RunEffect
from .effects.switcheffect import SwitchEffect
from .effects.balleffect import BallEffect

import types
import importlib
from pathlib import Path

EFFECTS_PATH = Path("game/combat/effects/moveeffect/")


class CombatScene:
    def __init__(self, game, team_1, team_2):
        self.game = game
        t1 = self.init_team(team_1)
        t2 = self.init_team(team_2)
        self.board_history = [PokeBoard(self)]
        self.board_graveyard = []
        self.init_board(t1, t2)

        self.round = 0

        self.effects = []
        self.effect_lib = {}

        self.init_effects()

    def init_effects(self):
        for x in EFFECTS_PATH.glob("*.py"):
            if "basemoveeffect" in x.stem or "init" in x.stem:
                continue
            lib = importlib.import_module(
                f".{x.stem}", package="game.combat.effects.moveeffect"
            )
            self.effect_lib[x.stem] = getattr(lib, x.stem.capitalize())

    def init_board(self, team_1, team_2):
        self.board.first_init(team_1, team_2)

    def init_team(self, team):
        return [self.init_fighter(x) for x in team]

    def init_fighter(self, src):
        return PokeFighter(self.game, src)

    def run_scene(self, action_descriptions):
        self.round += 1
        actions = self.format_actions(action_descriptions)
        # print("Actions:", actions)

        # After select
        # for effect in sorted(self.effects, key=lambda x: -x.spd_after_select):
        #     self.run_effect(effect, effect.after_select)
        # self.reset_effects_done()

        # Spawn all action effects
        actions.sort(key=lambda x: self.board.get_action_priority(x))
        action_effects = []
        for action in actions:
            move_effect = self.spawn_action_effect(action)
            action_effects.append((action, move_effect))
        while action_effects:
            self.board.action, move_effect = action_effects.pop()
            # TODO: dit is alleen om in de state de huidige 'actor' aan te geven
            self.board.set_direction(move_effect)

            # skip = False

            # Before action
            # for effect in sorted(self.effects, key=lambda x: -x.spd_before_action):
            #     skip = self.run_effect(effect, effect.before_action)
            #     if skip:
            #         break
            #
            # self.reset_effects_done()
            # if skip:
            #     continue

            # On action
            while effects := [
                x
                for x in sorted(self.effects, key=lambda x: -x.spd_on_action)
                if not x.done and not x.skip
            ]:
                skip = self.run_effect(effects[0], effects[0].on_action)
                if skip:
                    for effect in self.get_effects_on_target(move_effect.user):
                        effect.done = True
                    self.delete_effect(move_effect)
                    break
            # while effects := [
            #     x
            #     for x in sorted(self.board.get_effects_on_target(move_effect.user), key=lambda x: -x.spd_on_action)
            #     if not x.done
            # ]:
            #     skip = self.run_effect(effects[0], effects[0].on_action)

            self.reset_effects_done()

            # if skip:
            #     continue
            # # After action
            # for effect in sorted(self.effects, key=lambda x: -x.spd_after_action):
            #     skip = self.run_effect(effect, effect.after_action)
            #     if skip:
            #         continue
        self.board.reset_action()
        # Before end
        # for effect in sorted(self.effects, key=lambda x: -x.spd_before_end):
        #     self.run_effect(effect, effect.before_end)

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
            effect.skip = True

    def run_effect(self, effect, f, *args):
        effect.done = True
        self.new_board()
        if args:
            delete, skip, end = f(*args)
        else:
            delete, skip, end = f()
        if delete:
            self.delete_effect(effect)
        if skip:
            return True
        return False

    def add_effect(self, effect):
        self.effects.append(effect)

    def spawn_action_effect(self, action):
        effect = None
        if action.action_name == "attack":
            effect = MainMove(self, action)
        elif action.action_name == "flee":
            effect = RunEffect(self)
        elif action.action_name == "swap":
            effect = SwitchEffect(self, action)
        elif action.action_name == "ball":
            effect = BallEffect(self, action)
        self.effects.append(effect)
        return effect

    def on_switch_effects(self, old, new):
        for effect in [x for x in sorted(self.effects, key=lambda x: -x.spd_on_switch)]:
            delete = self.run_effect(effect, effect.on_switch, old, new)
            if delete:
                self.delete_effect(effect)

    def on_send_out_effects(self, target):
        for effect in [x for x in sorted(self.effects, key=lambda x: -x.spd_on_send_out)]:
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
        new_board.skip = True
        self.board_history.append(new_board)

    def format_actions(self, action_descriptions):
        actions = []
        for (name, action), user, target in action_descriptions:
            # action.id
            # action.identifier
            # action.name
            # action.function
            # action.power
            # action.type
            # action.damagecat
            # action.accuracy
            # action.pp
            # action.chance
            # action.target
            # action.priority
            # action.flags
            # action.description
            # action.user
            # action.target
            if name == "swap":
                action = types.SimpleNamespace()
                action.action_name = "swap"
                action.user = user
                action.target = target
                action.priority = 6
                actions.append(action)
            if name == "flee":
                # TODO fix a RunAction object
                action = types.SimpleNamespace()
                action.action_name = "flee"
                action.user = None
                action.target = None
                action.priority = 6
                actions.append(action)
            if name == "attack":
                action = action.copy()
                action.action_name = name
                action["user"] = user
                action["target"] = target
                actions.append(action)
        return actions

    @property
    def board(self):
        return self.board_history[-1]
