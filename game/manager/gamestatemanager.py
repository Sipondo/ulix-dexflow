from ..gamestate.gamestatebattle import GameStateBattle
from ..gamestate.gamestatecinematic import GameStateCinematic
from ..gamestate.gamestateintro import GameStateIntro
from ..gamestate.gamestatemenubag import GameStateMenuBag
from ..gamestate.gamestatemenucareer import GameStateMenuCareer
from ..gamestate.gamestatemenuoptions import GameStateMenuOptions
from ..gamestate.gamestatemenuparty import GameStateMenuParty
from ..gamestate.gamestatemenusave import GameStateMenuSave
from ..gamestate.gamestateoverworld import GameStateOverworld


class GameStateManager:
    def __init__(self, gamegui):
        self.game = gamegui
        self.current_state = None

    def switch_state(self, new_state, **kwargs):
        self.game.r_int.new_canvas()
        if self.current_state is not None:
            self.current_state.on_exit()
            del self.current_state

        if new_state == "overworld":
            self.current_state = GameStateOverworld(self.game)
        elif new_state == "battle":
            self.current_state = GameStateBattle(self.game)
        elif new_state == "menubag":
            self.current_state = GameStateMenuBag(self.game)
        elif new_state == "menucareer":
            self.current_state = GameStateMenuCareer(self.game)
        elif new_state == "menuoptions":
            self.current_state = GameStateMenuOptions(self.game)
        elif new_state == "menuparty":
            self.current_state = GameStateMenuParty(self.game)
        elif new_state == "menusave":
            self.current_state = GameStateMenuSave(self.game)
        elif new_state == "cinematic":
            self.current_state = GameStateCinematic(self.game)
        elif new_state == "intro":
            self.current_state = GameStateIntro(self.game)

        print(f"GAMESTATE SWITCHED: {new_state}")
        self.current_state.on_enter(**kwargs)
