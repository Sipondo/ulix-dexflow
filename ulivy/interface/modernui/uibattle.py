from ..baseui import BaseUI
from kivy.lang import Builder
import enum


Builder.load_file("ulivy/interface/modernui/uibattle.kv")


class BattleStates(enum.Enum):
    ACTION = enum.auto()
    TOPMENU = enum.auto()
    ACTIONMENU = enum.auto()
    SWAPMENU = enum.auto()
    BALLMENU = enum.auto()


class UIBattle(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.lock_state = False

        self.state = BattleStates.TOPMENU

        self.sel_top = 0
        self.sel_max_top = 4
        self.sel_action = 0
        self.sel_max_action = 4

        self.update_ui()

    def update(self, time=None, frame_time=None):
        return False

    def event_keypress(self, key, modifiers):
        if self.state == BattleStates.TOPMENU:
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
                    self.state = BattleStates.ACTIONMENU
                    # self.selection = self.action_choice
                elif self.sel_top == 1:
                    self.state = BattleStates.BALLMENU
                elif self.sel_top == 2:  # and self.battle_type != "trainer":
                    self.state = BattleStates.SWAPMENU
                elif self.sel_top == 3:  # and self.battle_type != "trainer":
                    pass
                    # self.reg_action(Action(ActionType.RUN))
                pass

        if self.state == BattleStates.ACTIONMENU:
            if key == "down":
                self.sel_action = (self.sel_action + 1) % self.sel_max_action
                self.game.r_aud.effect("select")
            elif key == "up":
                self.sel_action = (self.sel_action - 1) % self.sel_max_action
                self.game.r_aud.effect("select")
            elif key == "interact":
                pass

        if key == "backspace" or key == "menu":
            self.game.r_aud.effect("cancel")
            if not self.lock_state:
                self.game.r_aud.effect("cancel")
                # if self.state == BattleStates.TOPMENU:
                #     self.combat.deregister_action()
                self.state = BattleStates.TOPMENU

        self.update_ui()

    def update_ui(self):
        self.highlight_top()
        self.highlight_attack()

    def highlight_top(self):
        self.ids.BattleTop.opacity = 1 if self.state == BattleStates.TOPMENU else 0
        s = self.sel_top
        self.ids.BattleTopAttackCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==0 else ""}.png'
        self.ids.BattleTopThrowballCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==1 else ""}.png'
        self.ids.BattleTopSwitchCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==2 else ""}.png'
        self.ids.BattleTopRunCell.source = f'ulivy/interface/modernui/battle/battlecell{"_selected" if s==3 else ""}.png'

    def highlight_attack(self):
        self.ids.BattleAttack.opacity = (
            1 if self.state == BattleStates.ACTIONMENU else 0
        )
        s = self.sel_action
        self.ids.BattleAttackACell.source = f'ulivy/interface/modernui/battle/attackcell{"_selected" if s==0 else ""}.png'
        self.ids.BattleAttackBCell.source = f'ulivy/interface/modernui/battle/attackcell{"_selected" if s==1 else ""}.png'
        self.ids.BattleAttackCCell.source = f'ulivy/interface/modernui/battle/attackcell{"_selected" if s==2 else ""}.png'
        self.ids.BattleAttackDCell.source = f'ulivy/interface/modernui/battle/attackcell{"_selected" if s==3 else ""}.png'
