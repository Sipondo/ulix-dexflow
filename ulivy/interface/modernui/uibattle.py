from ulivy.combat.effects.sendouteffect import SendOutEffect
from ulivy.combat.effects.switcheffect import SwitchEffect
from ..baseui import BaseUI
from kivy.lang import Builder
import enum
from ulivy.combat.action import ActionType, Action
from ulivy.gamestate.gamestatebattle import BattleStates

Builder.load_file("ulivy/interface/modernui/uibattle.kv")


class UIBattle(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False

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

        try:
            actors = self.gamestate.actors
            self.sel_max_action = len(actors[0].actions)
        except AttributeError:
            pass

        self.update_status(time, frame_time)
        self.update_ui()
        return False

    def event_keypress(self, key, modifiers):
        # print(key, modifiers)
        if self.gamestate.lock == False:
            if self.gamestate.state == BattleStates.TOPMENU:
                if key == "down":
                    self.sel_top = (self.sel_top + 1) % self.sel_max_top
                    self.game.r_aud.effect("select")
                elif key == "up":
                    self.sel_top = (self.sel_top - 1) % self.sel_max_top
                    self.game.r_aud.effect("select")
                # elif key == "right":
                #     self.sel_top = (self.sel_top + 1) % self.sel_max_top
                #     self.game.r_aud.effect("select")
                # elif key == "left":
                #     self.sel_top = (self.sel_top - 1) % self.sel_max_top
                #     self.game.r_aud.effect("select")
                elif key == "interact":
                    self.game.r_aud.effect("select")
                    if self.sel_top == 0:
                        self.gamestate.state = BattleStates.ACTIONMENU
                        # self.selection = self.action_choice
                    elif self.sel_top == 1:
                        self.gamestate.state = BattleStates.SWAPMENU

            elif self.gamestate.state == BattleStates.ACTIONMENU:
                if key == "down":
                    self.sel_action = (self.sel_action + 1) % self.sel_max_action
                    self.game.r_aud.effect("select")
                elif key == "up":
                    self.sel_action = (self.sel_action - 1) % self.sel_max_action
                    self.game.r_aud.effect("select")
                    print(self.gamestate.lock_state)
                    print(self.gamestate.pending_boards)
                elif key == "interact":
                    self.game.r_aud.effect("select")
                    pp_amount = int(
                        self.gamestate.actors[0].actions[self.sel_action]["pp"]
                    )
                    if pp_amount > 0:
                        self.action_choice = self.sel_action
                        self.gamestate.reg_action(
                            Action(ActionType.ATTACK, a_index=self.sel_action)
                        )

            elif self.gamestate.state == BattleStates.SWAPMENU:
                if key == "down":
                    self.sel_swap = (self.sel_swap + 1) % self.sel_max_swap
                    self.game.r_aud.effect("select")
                elif key == "up":
                    self.sel_swap = (self.sel_swap - 1) % self.sel_max_swap
                    self.game.r_aud.effect("select")
                elif key == "interact":
                    self.game.r_aud.effect("select")
                    self.sel_action = 0
                    if self.gamestate.board.teams[0][self.sel_swap][1].can_fight:
                        print(
                            "Lock state?",
                            self.gamestate.lock_state,
                            self.gamestate.combat.mgr_agent.agents[
                                0
                            ].action_handler.only_legal("SWITCH"),
                        )
                        # if self.gamestate.combat.mgr_agent.agents[
                        #     0
                        # ].action_handler.only_legal(
                        #     "SWITCH"
                        # ):  # TODO: remove this hacky solution (not UI)
                        if self.gamestate.lock_state == "user_summon":
                            self.gamestate.init_battle_us(self.sel_swap)
                            self.summoned_first = True
                        elif self.gamestate.lock_state == "user_switch":
                            sendout_act = Action(
                                ActionType.SENDOUT, a_index=self.sel_swap
                            )  # SENDOUT

                            if self.gamestate.combat.mgr_agent.agents[
                                0
                            ].action_handler.is_legal(sendout_act):
                                self.gamestate.reg_action(sendout_act)
                            else:
                                if self.gamestate.board.get_active(0) != self.sel_swap:
                                    self.gamestate.reg_action(
                                        Action(ActionType.SWITCH, a_index=self.sel_swap)
                                    )
                                    self.gamestate.reg_opponent_skip()
                                else:
                                    self.gamestate.state = BattleStates.TOPMENU
                                self.gamestate.combat.board.fainted = False

                                # switch_act = Action(
                                #     ActionType.SWITCH, a_index=self.sel_swap
                                # )  # SENDOUT
                                # self.gamestate.combat.add_effect(
                                #     SwitchEffect(
                                #         self.gamestate.combat, switch_act,
                                #     )
                                # )
                                # self.gamestate.combat.add_effect(
                                #     SendOutEffect(self.gamestate.combat, (1, 1),)
                                # )
                            # print("PENDING BOARDS:", self.gamestate.pending_boards)
                            self.gamestate.combat.mgr_agent.reset_legal(
                                0
                            )  # TODO: resolve this properly
                            self.gamestate.lock_state = False
                        else:
                            if self.gamestate.board.get_active(0) != self.sel_swap:
                                self.gamestate.reg_action(
                                    Action(ActionType.SWITCH, a_index=self.sel_swap)
                                )

            elif self.gamestate.state == BattleStates.ACTION:
                if key == "interact":
                    self.gamestate.advance_board()

            if key == "backspace" or key == "menu":
                if (
                    (not self.gamestate.lock_state)
                    and self.summoned_first
                    and self.gamestate.state
                    in (
                        BattleStates.SWAPMENU,
                        BattleStates.ACTIONMENU,
                        BattleStates.BALLMENU,
                    )
                ):
                    self.game.r_aud.effect("cancel")
                    # if self.gamestate.state == BattleStates.TOPMENU:
                    #     self.combat.deregister_action()
                    self.gamestate.state = BattleStates.TOPMENU

        self.update_ui()

    def update_ui(self):
        # print(self.gamestate.board.actives)
        # print(self.gamestate.actors)
        # for i in range(self.gamestate.combat.teams_n):
        #     print(self.gamestate.board.get_active_actor(i))
        self.highlight_top()
        self.highlight_attack()
        self.highlight_swap()

        self.ids.DialogueText.text = self.narrate

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
            f"ulivy/interface/modernui/battle/{n}bar.png"
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
            f"ulivy/interface/modernui/battle/{n}bar.png"
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
        self.ids.BattleTop.opacity = (
            1 if self.gamestate.state == BattleStates.TOPMENU else 0
        )
        s = self.sel_top
        self.ids.BattleTopAttackCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==0 else ""}.png'
        # self.ids.BattleTopThrowballCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==1 else ""}.png'
        self.ids.BattleTopSwitchCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==1 else ""}.png'
        # self.ids.BattleTopRunCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==3 else ""}.png'

    def highlight_attack(self):
        self.ids.BattleAttack.opacity = (
            1 if self.gamestate.state == BattleStates.ACTIONMENU else 0
        )
        s = self.sel_action

        self.ids.BattleAttackDCell.source = f'ulivy/interface/modernui/battle/attackcell{"_selected" if s==3 else ""}.png'

        self.ids.BattleAttackA.opacity = 0
        self.ids.BattleAttackB.opacity = 0
        self.ids.BattleAttackC.opacity = 0
        self.ids.BattleAttackD.opacity = 0

        if self.gamestate.state != BattleStates.ACTIONMENU:
            return

        actors = self.gamestate.actors
        actionlist = actors[0].actions

        if len(actionlist) < 1:
            return

        self.ids.BattleAttackA.opacity = 1
        self.ids.BattleAttackAName.text = (
            actionlist[0]["prefix"] + " " + actionlist[0]["name"]
        )[:20]
        self.ids.BattleAttackAType.source = f'ulivy/interface/modernui/battle/attack_types/attack_{actionlist[0]["type"].lower()}.png'
        self.ids.BattleAttackACharges.text = (
            str(actionlist[0]["pp"]) if int(actionlist[0]["pp"]) < 41 else "-"
        )

        stab = actionlist[0]["type"] in actors[0].types
        self.ids.BattleAttackACell.source = f'ulivy/interface/modernui/battle/attackcell{"_stab" if stab else ""}{"_selected" if s==0 else ""}.png'

        if len(actionlist) < 2:
            return

        self.ids.BattleAttackB.opacity = 1
        self.ids.BattleAttackBName.text = (
            actionlist[1]["prefix"] + " " + actionlist[1]["name"]
        )[:20]
        self.ids.BattleAttackBType.source = f'ulivy/interface/modernui/battle/attack_types/attack_{actionlist[1]["type"].lower()}.png'
        self.ids.BattleAttackBCharges.text = (
            str(actionlist[1]["pp"]) if int(actionlist[1]["pp"]) < 41 else "-"
        )

        stab = actionlist[1]["type"] in actors[0].types
        self.ids.BattleAttackBCell.source = f'ulivy/interface/modernui/battle/attackcell{"_stab" if stab else ""}{"_selected" if s==1 else ""}.png'

        if len(actionlist) < 3:
            return

        self.ids.BattleAttackC.opacity = 1
        self.ids.BattleAttackCName.text = (
            actionlist[2]["prefix"] + " " + actionlist[2]["name"]
        )[:20]
        self.ids.BattleAttackCType.source = f'ulivy/interface/modernui/battle/attack_types/attack_{actionlist[2]["type"].lower()}.png'
        self.ids.BattleAttackCCharges.text = (
            str(actionlist[2]["pp"]) if int(actionlist[2]["pp"]) < 41 else "-"
        )

        stab = actionlist[2]["type"] in actors[0].types
        self.ids.BattleAttackCCell.source = f'ulivy/interface/modernui/battle/attackcell{"_stab" if stab else ""}{"_selected" if s==2 else ""}.png'

    def highlight_swap(self):
        self.ids.BattleSwap.opacity = (
            1 if self.gamestate.state == BattleStates.SWAPMENU else 0
        )
        s = self.sel_swap
        self.ids.BattleSwapACell.source = (
            f'ulivy/interface/modernui/battle/ballcell{"_selected" if s==0 else ""}.png'
        )
        self.ids.BattleSwapBCell.source = (
            f'ulivy/interface/modernui/battle/ballcell{"_selected" if s==1 else ""}.png'
        )
        self.ids.BattleSwapCCell.source = (
            f'ulivy/interface/modernui/battle/ballcell{"_selected" if s==2 else ""}.png'
        )
        self.ids.BattleSwapDCell.source = (
            f'ulivy/interface/modernui/battle/ballcell{"_selected" if s==3 else ""}.png'
        )

        self.ids.BattleSwapA.opacity = 0
        self.ids.BattleSwapB.opacity = 0
        self.ids.BattleSwapC.opacity = 0
        self.ids.BattleSwapD.opacity = 0

        if self.gamestate.state != BattleStates.SWAPMENU:
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
        if self.gamestate.state == BattleStates.ACTION:
            return self.gamestate.board.narration

        if self.gamestate.state == BattleStates.ACTIONMENU:
            action = self.gamestate.actors[0].actions[self.sel_action]
            return (
                action.description + " " + action.suffix
                if not self.gamestate.lock_state
                else f"Forget {action['name']}?"
            )

        if self.gamestate.state == BattleStates.SWAPMENU:
            name = self.game.inventory.fighter_names[self.sel_swap]
            return f"Send out {name}."

        if self.gamestate.state == BattleStates.BALLMENU:
            # ball = self.game.inventory.get_pocket_items(3)[self.selection]
            return "Throw a ball to catch the Pokémon!"  # ball.description

        if self.gamestate.state == BattleStates.TOPMENU:
            strings = [
                "Attack the enemy!",
                "Choose a Pokemon!",
                "Throw a Poke Ball!",
                "Run away!",
            ]
            return strings[self.sel_top]
        return "ERROR: Missing String"
