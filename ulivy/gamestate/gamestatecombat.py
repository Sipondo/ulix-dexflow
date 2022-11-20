from .basegamestate import BaseGameState
from ulivy.particle.battlescene import BattleScene

from ulivy.c2.combatboard import Input


class GameStateCombat(BaseGameState):
    def on_enter(
        self, battle_type="trainer", enemy_team=None, agents=None, particle_test=False
    ):
        if len(self.game.inventory.members) < 1:
            self.game.inventory.members.append(self.game.inventory.init_random_member())

        if enemy_team is None:
            enemy_team = [self.game.inventory.init_random_member()]

        self.game.m_com.init_new_stack()
        self.game.m_com.set_team(0, self.game.inventory.members)
        self.game.m_com.set_team(1, enemy_team)
        self.game.m_com.set_required_input(Input.TURN)

        self.game.r_fbo.r_box.go_to(0.0, force=True)
        print("STARTING A FIGHT AGAINST:", enemy_team)

        self.game.r_fbo.disable_overworld()
        # Renderer setup
        self.scene = BattleScene(self.game)
        self.game.r_fbo.fbo_add_widget(self.scene)

        if len(self.game.inventory.members) < 1:
            self.game.inventory.members.append(self.game.inventory.init_random_member())

        self.battle_type = battle_type

        self.lock_state = False

    def update(self, time, frame_time):
        return True

    def on_exit(self):
        self.game.r_fbo.fbo_remove_widget(self.scene)
        del self.scene

    def event_keypress(self, key, modifiers):
        return
