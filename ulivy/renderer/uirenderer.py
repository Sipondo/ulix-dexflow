import importlib
from kivy.uix.floatlayout import FloatLayout

UI = "modernui"

UI_OVERWORLD = importlib.import_module(f"ulivy.interface.{UI}.uioverworld").UIOverworld
UI_CINEMATIC = importlib.import_module(f"ulivy.interface.{UI}.uicinematic").UICinematic
UI_DEBUG = importlib.import_module(f"ulivy.interface.{UI}.uidebug").UIDebug
UI_PROMPT = importlib.import_module(f"ulivy.interface.{UI}.uiprompt").UIPrompt
UI_BATTLE = importlib.import_module(f"ulivy.interface.{UI}.uibattle").UIBattle
UI_MENU_MAIN = importlib.import_module(f"ulivy.interface.{UI}.uimenumain").UIMenuMain
UI_MENU_BAG = importlib.import_module(f"ulivy.interface.{UI}.uimenubag").UIMenuBag


class UIRenderer(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        self.current_ui = None
        super(UIRenderer, self).__init__(**kwargs)
        self.size_hint_x = None
        self.size_hint_y = None
        self.size = self.game.RENDER_SIZE

    def update(self, time, frame_time):
        self.size = self.game.RENDER_SIZE
        if self.current_ui:
            return self.current_ui.update(time, frame_time)

    def event_keypress(self, request, modifiers):
        if self.current_ui:
            return self.current_ui.event_keypress(request, modifiers)

    def event_unicode(self, char):
        if self.current_ui:
            return self.current_ui.event_unicode(char)

    def switch_ui(self, new_ui, gstate, **kwargs):
        if self.current_ui is not None:
            self.current_ui.on_exit()
            self.remove_widget(self.current_ui)
            del self.current_ui
            self.current_ui = None

        if new_ui == "overworld":
            self.current_ui = UI_OVERWORLD(self.game, gstate, size=self.size)
        elif new_ui == "cinematic":
            self.current_ui = UI_CINEMATIC(self.game, gstate, size=self.size)
        elif new_ui == "debug":
            self.current_ui = UI_DEBUG(self.game, gstate)
        elif new_ui == "prompt":
            self.current_ui = UI_PROMPT(self.game, gstate)
        elif new_ui == "battle":
            self.current_ui = UI_BATTLE(self.game, gstate)
        elif new_ui == "menumain":
            self.current_ui = UI_MENU_MAIN(self.game, gstate, size=self.size)
        elif new_ui == "menubag":
            self.current_ui = UI_MENU_BAG(self.game, gstate)
        else:
            return

        self.current_ui.on_enter(**kwargs)
        self.add_widget(self.current_ui)
        self.current_ui.update()

