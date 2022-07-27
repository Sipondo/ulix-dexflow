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
        self.sel_max_top = 4
        self.sel_action = 0
        self.sel_max_action = 4
        self.sel_swap = 0
        self.sel_max_swap = len(self.game.inventory.fighter_names)

        self.update_ui()

    def update(self, time=None, frame_time=None):
        self.update_status()
        self.update_ui()
        return False

    def event_keypress(self, key, modifiers):
        # print(key, modifiers)
        if self.gamestate.lock == False:
            if self.gamestate.state == BattleStates.TOPMENU:
                if key == "down":
                    self.sel_top = (self.sel_top + 2) % self.sel_max_top
                    self.game.r_aud.effect("select")
                elif key == "up":
                    self.sel_top = (self.sel_top - 2) % self.sel_max_top
                    self.game.r_aud.effect("select")
                elif key == "right":
                    self.sel_top = (self.sel_top + 1) % self.sel_max_top
                    self.game.r_aud.effect("select")
                elif key == "left":
                    self.sel_top = (self.sel_top - 1) % self.sel_max_top
                    self.game.r_aud.effect("select")
                elif key == "interact":
                    if self.sel_top == 0:
                        self.gamestate.state = BattleStates.ACTIONMENU
                        # self.selection = self.action_choice
                    elif self.sel_top == 1:
                        self.gamestate.state = BattleStates.BALLMENU
                    elif self.sel_top == 2:  # and self.battle_type != "trainer":
                        self.gamestate.state = BattleStates.SWAPMENU
                    elif self.sel_top == 3:  # and self.battle_type != "trainer":
                        pass
                        # self.reg_action(Action(ActionType.RUN))
                    pass

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
                    self.action_choice = self.sel_swap
                    self.gamestate.reg_action(
                        Action(ActionType.ATTACK, a_index=self.sel_swap)
                    )

            elif self.gamestate.state == BattleStates.SWAPMENU:
                if key == "down":
                    self.sel_swap = (self.sel_swap + 1) % self.sel_max_swap
                    self.game.r_aud.effect("select")
                elif key == "up":
                    self.sel_swap = (self.sel_swap - 1) % self.sel_max_swap
                    self.game.r_aud.effect("select")
                elif key == "interact":
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
                        if self.gamestate.lock_state == "user_switch":
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
                self.game.r_aud.effect("cancel")
                if not self.gamestate.lock_state:
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

    def update_status(self):
        gst = self.gamestate
        fighter = gst.board.get_actor((0, gst.board.get_active(0)))
        rel_hp = gst.board.get_relative_hp((0, gst.board.get_active(0)))

        self.ids.BattleStatusOursName.text = fighter.name
        self.ids.BattleStatusOursHP.size_hint = (float(0.9 * rel_hp), 0.15)

        fighter = gst.board.get_actor((1, gst.board.get_active(1)))
        rel_hp = gst.board.get_relative_hp((1, gst.board.get_active(1)))

        self.ids.BattleStatusTheirsName.text = fighter.name
        self.ids.BattleStatusTheirsHP.size_hint = (float(0.9 * rel_hp), 0.15)

    def highlight_top(self):
        self.ids.BattleTop.opacity = (
            1 if self.gamestate.state == BattleStates.TOPMENU else 0
        )
        s = self.sel_top
        self.ids.BattleTopAttackCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==0 else ""}.png'
        self.ids.BattleTopThrowballCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==1 else ""}.png'
        self.ids.BattleTopSwitchCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==2 else ""}.png'
        self.ids.BattleTopRunCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==3 else ""}.png'

    def highlight_attack(self):
        self.ids.BattleAttack.opacity = (
            1 if self.gamestate.state == BattleStates.ACTIONMENU else 0
        )
        s = self.sel_action
        self.ids.BattleAttackACell.source = f'ulivy/interface/modernui/battle/attackcell{"_selected" if s==0 else ""}.png'
        self.ids.BattleAttackBCell.source = f'ulivy/interface/modernui/battle/attackcell{"_selected" if s==1 else ""}.png'
        self.ids.BattleAttackCCell.source = f'ulivy/interface/modernui/battle/attackcell{"_selected" if s==2 else ""}.png'
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
        self.ids.BattleAttackAName.text = actionlist[0]["name"]
        self.ids.BattleAttackAType.source = f'ulivy/interface/modernui/battle/attack_types/attack_{actionlist[0]["type"].lower()}.png'
        self.ids.BattleAttackACharges.text = str(actionlist[0]["pp"])

        if len(actionlist) < 2:
            return

        self.ids.BattleAttackB.opacity = 1
        self.ids.BattleAttackBName.text = actionlist[1]["name"]
        self.ids.BattleAttackBType.source = f'ulivy/interface/modernui/battle/attack_types/attack_{actionlist[1]["type"].lower()}.png'
        self.ids.BattleAttackBCharges.text = str(actionlist[1]["pp"])

        if len(actionlist) < 3:
            return

        self.ids.BattleAttackC.opacity = 1
        self.ids.BattleAttackCName.text = actionlist[2]["name"]
        self.ids.BattleAttackCType.source = f'ulivy/interface/modernui/battle/attack_types/attack_{actionlist[2]["type"].lower()}.png'
        self.ids.BattleAttackCCharges.text = str(actionlist[2]["pp"])

        if len(actionlist) < 4:
            return

        self.ids.BattleAttackD.opacity = 1
        self.ids.BattleAttackDName.text = actionlist[3]["name"]
        self.ids.BattleAttackDType.source = f'ulivy/interface/modernui/battle/attack_types/attack_{actionlist[3]["type"].lower()}.png'
        self.ids.BattleAttackDCharges.text = str(actionlist[3]["pp"])

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

        self.ids.BattleSwapA.opacity = 1
        self.ids.BattleSwapAName.text = swaplist[0]

        if len(swaplist) < 2:
            return

        self.ids.BattleSwapB.opacity = 1
        self.ids.BattleSwapBName.text = swaplist[1]

        if len(swaplist) < 3:
            return

        self.ids.BattleSwapC.opacity = 1
        self.ids.BattleSwapCName.text = swaplist[2]

        if len(swaplist) < 4:
            return

        self.ids.BattleSwapD.opacity = 1
        self.ids.BattleSwapDName.text = swaplist[3]

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
                action.description
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
                "Throw a Poke Ball!",
                "Choose a Pokemon!",
                "Run away!",
            ]
            return strings[self.sel_top]
        return "ERROR: Missing String"
