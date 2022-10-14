import enum

from kivy.lang import Builder

from ulivy.interface.baseui import BaseUI
from ulivy.c2.combatboard import Input

Builder.load_file("resources/basicui/interface/uicombat.kv")


class UIStates(enum.Enum):
    NONE = enum.auto()
    TOP = enum.auto()
    MOVE = enum.auto()
    SWAP = enum.auto()
    BALL = enum.auto()


class UICombat(BaseUI):
    def on_enter(self, **kwargs):
        self.state = UIStates.NONE
        self.advancing = True

        self.sel_top = 0
        self.sel_max_top = 2
        self.sel_action = 0
        self.sel_max_action = 4
        self.sel_swap = 0
        self.sel_max_swap = len(self.game.inventory.fighter_names)

        self.hp_bar_ours = 0.0
        self.hp_bar_theirs = 0.0

        self.summoned_first = False

        self.status_ours = (0, 0)
        self.status_theirs = (0, 0)

        self.update_ui()

    def update(self, time=None, frame_time=None):
        if time is None:
            time = 0
            frame_time = 0.05

        # self.update_status(time, frame_time)
        self.update_ui_new()
        return False

    def event_keypress(self, key, modifiers):
        if key == "interact":
            self.advancing = self.game.m_com.advance()

        print(self.advancing, self.state)
        if self.advancing:
            self.update_ui_new()
            return

        if self.state == UIStates.TOP:
            if key == "down":
                self.sel_top = (self.sel_top + 1) % self.sel_max_top
                self.game.r_aud.effect("select")
            elif key == "up":
                self.sel_top = (self.sel_top - 1) % self.sel_max_top
                self.game.r_aud.effect("select")
            elif key == "interact":
                self.game.r_aud.effect("select")
                if self.sel_top == 0:
                    self.state = UIStates.MOVE
                    # self.selection = self.action_choice
                elif self.sel_top == 1:
                    self.state = UIStates.SWAP

        elif self.state == UIStates.MOVE:
            if key == "down":
                self.sel_action = (self.sel_action + 1) % self.sel_max_action
                self.game.r_aud.effect("select")
            elif key == "up":
                self.sel_action = (self.sel_action - 1) % self.sel_max_action
                self.game.r_aud.effect("select")
            elif key == "interact":
                self.game.r_aud.effect("select")
                # pp_amount = int(
                #     self.gamestate.actors[0].actions[self.sel_action]["pp"]
                # )
                # if pp_amount > 0:
                #     self.action_choice = self.sel_action
                #     self.gamestate.reg_action(
                #         Action(ActionType.ATTACK, a_index=self.sel_action)
                #     )

        if key == "backspace" or key == "menu":
            if self.state in (
                UIStates.SWAP,
                UIStates.MOVE,
                UIStates.BALL,
            ):
                self.game.r_aud.effect("cancel")
                self.state = UIStates.TOP

        self.update_ui_new()

    def update_ui_new(self):
        if self.game.m_com.b.required_input == Input.NONE:
            self.state = UIStates.NONE
        elif self.state == UIStates.NONE:
            self.state = UIStates.TOP

        self.ids.BattleStatusOursName.text = self.game.m_com.b.get_active_m(0)["name"]
        self.ids.BattleStatusTheirsName.text = self.game.m_com.b.get_active_m(1)["name"]

        self.highlight_top()
        self.highlight_attack()
        self.highlight_swap()

    def update_ui(self):
        # print(self.gamestate.board.actives)
        # print(self.gamestate.actors)
        # for i in range(self.gamestate.combat.teams_n):
        #     print(self.gamestate.board.get_active_actor(i))

        # self.ids.DialogueText.text = self.narrate
        pass

    def update_status(self, time, frame_time):
        gst = self.gamestate
        fighter = gst.board.get_actor((0, gst.board.get_active(0)))
        rel_hp = gst.board.get_relative_hp((0, gst.board.get_active(0)))

        if rel_hp < self.hp_bar_ours:
            self.hp_bar_ours = self.hp_bar_ours - (frame_time * 1.5)

        if rel_hp >= self.hp_bar_ours:
            self.hp_bar_ours = rel_hp

        rel_hp = self.hp_bar_ours

        self.ids.BattleStatusOursName.text = fighter.name
        self.ids.BattleStatusOursHP.size_hint = (float(0.9 * rel_hp), 0.15)
        n = "green" if rel_hp >= 0.5 else ("yellow" if rel_hp >= 0.2 else "red")
        self.ids.BattleStatusOursHP.source = (
            f"resources/basicui/graphics/interface/battle/{n}bar.png"
        )

        status = (fighter, rel_hp)

        if status != self.status_ours:
            self.status_ours = status

            se = [
                x.name
                for x in self.gamestate.combat.get_effects_on_target(
                    (0, gst.board.get_active(0))
                )
            ]
            self.ids.BattleStatusOursPoison.opacity = 1.0 if "Poison" in se else 0.1
            self.ids.BattleStatusOursBurn.opacity = 1.0 if "Burn" in se else 0.1
            self.ids.BattleStatusOursParalysis.opacity = (
                1.0 if "Paralysis" in se else 0.1
            )
            self.ids.BattleStatusOursFreeze.opacity = 1.0 if "Freeze" in se else 0.1

        fighter = gst.board.get_actor((1, gst.board.get_active(1)))
        rel_hp = gst.board.get_relative_hp((1, gst.board.get_active(1)))

        if rel_hp < self.hp_bar_theirs:
            self.hp_bar_theirs = self.hp_bar_theirs - (frame_time * 1.5)

        if rel_hp >= self.hp_bar_theirs:
            self.hp_bar_theirs = rel_hp

        rel_hp = self.hp_bar_theirs

        self.ids.BattleStatusTheirsName.text = fighter.name
        self.ids.BattleStatusTheirsHP.size_hint = (float(0.9 * rel_hp), 0.15)
        n = "green" if rel_hp >= 0.5 else ("yellow" if rel_hp >= 0.2 else "red")
        self.ids.BattleStatusTheirsHP.source = (
            f"resources/basicui/graphics/interface/battle/{n}bar.png"
        )

        status = (fighter, rel_hp)

        if status != self.status_theirs:
            self.status_theirs = status

            se = [
                x.name
                for x in self.gamestate.combat.get_effects_on_target(
                    (1, gst.board.get_active(1))
                )
            ]
            self.ids.BattleStatusTheirsPoison.opacity = 1.0 if "Poison" in se else 0.1
            self.ids.BattleStatusTheirsBurn.opacity = 1.0 if "Burn" in se else 0.1
            self.ids.BattleStatusTheirsParalysis.opacity = (
                1.0 if "Paralysis" in se else 0.1
            )
            self.ids.BattleStatusTheirsFreeze.opacity = 1.0 if "Freeze" in se else 0.1

    def highlight_top(self):
        self.ids.BattleTop.opacity = 1 if self.state == UIStates.TOP else 0
        s = self.sel_top
        self.ids.BattleTopAttackCell.source = f'resources/basicui/graphics/interface/battle/battlecell{"_selected" if s==0 else ""}.png'
        # self.ids.BattleTopThrowballCell.source = f'resources/basicui/graphics/interface/battle/battlecell{"_selected" if s==1 else ""}.png'
        self.ids.BattleTopSwitchCell.source = f'resources/basicui/graphics/interface/battle/battlecell{"_selected" if s==1 else ""}.png'
        # self.ids.BattleTopRunCell.source = f'resources/basicui/graphics/interface/battle/battlecell{"_selected" if s==3 else ""}.png'

    def highlight_attack(self):
        self.ids.BattleAttack.opacity = 1 if self.state == UIStates.MOVE else 0
        s = self.sel_action

        self.ids.BattleAttackDCell.source = f'resources/basicui/graphics/interface/battle/attackcell{"_selected" if s==3 else ""}.png'

        self.ids.BattleAttackA.opacity = 0
        self.ids.BattleAttackB.opacity = 0
        self.ids.BattleAttackC.opacity = 0
        self.ids.BattleAttackD.opacity = 0

        if self.state != UIStates.MOVE:
            return

        actors = self.gamestate.actors
        actionlist = actors[0].actions

        if len(actionlist) < 1:
            return

        self.ids.BattleAttackA.opacity = 1
        self.ids.BattleAttackAName.text = (
            actionlist[0]["prefix"] + " " + actionlist[0]["name"]
        )[:20]
        self.ids.BattleAttackAType.source = f'resources/basicui/graphics/interface/battle/attack_types/attack_{actionlist[0]["type"].lower()}.png'
        self.ids.BattleAttackACharges.text = (
            str(actionlist[0]["pp"]) if int(actionlist[0]["pp"]) < 41 else "-"
        )

        stab = actionlist[0]["type"] in actors[0].types
        self.ids.BattleAttackACell.source = f'resources/basicui/graphics/interface/battle/attackcell{"_stab" if stab else ""}{"_selected" if s==0 else ""}.png'

        if len(actionlist) < 2:
            return

        self.ids.BattleAttackB.opacity = 1
        self.ids.BattleAttackBName.text = (
            actionlist[1]["prefix"] + " " + actionlist[1]["name"]
        )[:20]
        self.ids.BattleAttackBType.source = f'resources/basicui/graphics/interface/battle/attack_types/attack_{actionlist[1]["type"].lower()}.png'
        self.ids.BattleAttackBCharges.text = (
            str(actionlist[1]["pp"]) if int(actionlist[1]["pp"]) < 41 else "-"
        )

        stab = actionlist[1]["type"] in actors[0].types
        self.ids.BattleAttackBCell.source = f'resources/basicui/graphics/interface/battle/attackcell{"_stab" if stab else ""}{"_selected" if s==1 else ""}.png'

        if len(actionlist) < 3:
            return

        self.ids.BattleAttackC.opacity = 1
        self.ids.BattleAttackCName.text = (
            actionlist[2]["prefix"] + " " + actionlist[2]["name"]
        )[:20]
        self.ids.BattleAttackCType.source = f'resources/basicui/graphics/interface/battle/attack_types/attack_{actionlist[2]["type"].lower()}.png'
        self.ids.BattleAttackCCharges.text = (
            str(actionlist[2]["pp"]) if int(actionlist[2]["pp"]) < 41 else "-"
        )

        stab = actionlist[2]["type"] in actors[0].types
        self.ids.BattleAttackCCell.source = f'resources/basicui/graphics/interface/battle/attackcell{"_stab" if stab else ""}{"_selected" if s==2 else ""}.png'

    def highlight_swap(self):
        self.ids.BattleSwap.opacity = 1 if self.state == UIStates.SWAP else 0
        s = self.sel_swap
        self.ids.BattleSwapACell.source = f'resources/basicui/graphics/interface/battle/ballcell{"_selected" if s==0 else ""}.png'
        self.ids.BattleSwapBCell.source = f'resources/basicui/graphics/interface/battle/ballcell{"_selected" if s==1 else ""}.png'
        self.ids.BattleSwapCCell.source = f'resources/basicui/graphics/interface/battle/ballcell{"_selected" if s==2 else ""}.png'
        self.ids.BattleSwapDCell.source = f'resources/basicui/graphics/interface/battle/ballcell{"_selected" if s==3 else ""}.png'

        self.ids.BattleSwapA.opacity = 0
        self.ids.BattleSwapB.opacity = 0
        self.ids.BattleSwapC.opacity = 0
        self.ids.BattleSwapD.opacity = 0

        if self.state != UIStates.SWAP:
            return

        swaplist = self.game.inventory.fighter_names

        if len(swaplist) < 1:
            return

        m = self.gamestate.board.teams[0][0][1]
        self.ids.BattleSwapA.opacity = 1
        self.ids.BattleSwapAName.text = (
            f"{swaplist[0]} {int(100 * m.current_hp / m.max_hp)}%"
        )

        if len(swaplist) < 2:
            return

        m = self.gamestate.board.teams[0][1][1]
        self.ids.BattleSwapB.opacity = 1
        self.ids.BattleSwapBName.text = (
            f"{swaplist[1]} {int(100 * m.current_hp / m.max_hp)}%"
        )

        if len(swaplist) < 3:
            return

        m = self.gamestate.board.teams[0][2][1]
        self.ids.BattleSwapC.opacity = 1
        self.ids.BattleSwapCName.text = (
            f"{swaplist[2]} {int(100 * m.current_hp / m.max_hp)}%"
        )

    @property
    def gamestate(self):
        return self.game.m_gst.current_state

    @property
    def narrate(self):
        if self.state == BattleStates.ACTION:
            return self.gamestate.board.narration

        if self.state == UIStates.MOVE:
            action = self.gamestate.actors[0].actions[self.sel_action]
            return (
                action.description + " " + action.suffix
                if not self.gamestate.lock_state
                else f"Forget {action['name']}?"
            )

        if self.state == UIStates.SWAP:
            name = self.game.inventory.fighter_names[self.sel_swap]
            return f"Send out {name}."

        if self.state == UIStates.BALL:
            # ball = self.game.inventory.get_pocket_items(3)[self.selection]
            return "Throw a ball to catch the Pokémon!"  # ball.description

        if self.state == UIStates.TOP:
            strings = [
                "Attack the enemy!",
                "Choose a Pokemon!",
                "Throw a Poke Ball!",
                "Run away!",
            ]
            return strings[self.sel_top]
        return "ERROR: Missing String"
