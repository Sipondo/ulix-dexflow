from ..gamestate.gamestatebattle import GameStateBattle
from ..gamestate.gamestatecinematic import GameStateCinematic

# from ..gamestate.gamestateintro import GameStateIntro
from ..gamestate.gamestatemenubag import GameStateMenuBag

# from ..gamestate.gamestatemenucareer import GameStateMenuCareer
# from ..gamestate.gamestatemenudex import GameStateMenuDex
# from ..gamestate.gamestatemenuoptions import GameStateMenuOptions
from ..gamestate.gamestatemenumain import GameStateMenuMain

# from ..gamestate.gamestatemenusave import GameStateMenuSave
from ..gamestate.gamestateoverworld import GameStateOverworld

from ..gamestate.gamestateprompt import GameStatePrompt

# from ..gamestate.gamestatestorage import GameStateStorage
# from ..gamestate.gamestateevolve import GameStateEvolve
# from ..gamestate.gamestateshop import GameStateShop
from ..gamestate.gamestatedebug import GameStateDebug


class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.current_state = None
        self.current_state_name = None
        self.previous_state_name = None

        self.switching = False
        self.switching_to = None
        self.switching_kwargs = []

    def switch_to_previous_state(self):
        if self.previous_state_name is not None:
            self.switch_state(self.previous_state_name)

    def update(self, time, frame_time):
        if self.switching:
            if self.game.r_fad.fade_done():
                self.switching = False
                self._switch_state(
                    self.switching_to, fade=True, **self.switching_kwargs
                )
                self.switching_to = None
                self.switching_kwargs = []
            return
        if self.current_state:
            return self.current_state.update(time, frame_time)

    def event_keypress(self, request, modifiers):
        if not self.game.r_fad.fade_done():
            return
        if self.current_state:
            return self.current_state.event_keypress(request, modifiers)

    def event_unicode(self, char):
        if not self.game.r_fad.fade_done():
            return
        if self.current_state:
            return self.current_state.event_unicode(char)

    def switch_state(self, new_state, fade=False, **kwargs):
        if not fade:
            self._switch_state(new_state, fade, **kwargs)
            return
        self.switching = True
        self.switching_to = new_state
        self.switching_kwargs = kwargs
        self.game.r_fad.go_to(1.0)

    def _switch_state(self, new_state, fade, **kwargs):
        if self.current_state is not None:
            self.current_state.on_exit()
            del self.current_state

        if fade:
            self.game.r_fad.go_to(0.0)

        self.previous_state_name = self.current_state_name
        self.current_state_name = new_state

        if new_state == "overworld":
            self.current_state = GameStateOverworld(self.game)
        elif new_state == "battle":
            self.current_state = GameStateBattle(self.game)
        elif new_state == "menubag":
            self.current_state = GameStateMenuBag(self.game)
        elif new_state == "menucareer":
            self.current_state = GameStateMenuCareer(self.game)
        elif new_state == "menudex":
            self.current_state = GameStateMenuDex(self.game)
        elif new_state == "menuoptions":
            self.current_state = GameStateMenuOptions(self.game)
        elif new_state == "menumain":
            self.current_state = GameStateMenuMain(self.game)
        elif new_state == "menusave":
            self.current_state = GameStateMenuSave(self.game)
        elif new_state == "cinematic":
            self.current_state = GameStateCinematic(self.game)
        elif new_state == "storage":
            self.current_state = GameStateStorage(self.game)
        elif new_state == "intro":
            self.current_state = GameStateIntro(self.game)
        elif new_state == "evolve":
            self.current_state = GameStateEvolve(self.game)
        elif new_state == "prompt":
            self.current_state = GameStatePrompt(self.game)
        elif new_state == "shop":
            self.current_state = GameStateShop(self.game)
        elif new_state == "debug":
            self.current_state = GameStateDebug(self.game)

        print(f"GAMESTATE SWITCHED: {new_state}, {kwargs}")
        self.current_state.on_enter(**kwargs)

        self.game.r_uin.switch_ui(new_state, self.current_state)
