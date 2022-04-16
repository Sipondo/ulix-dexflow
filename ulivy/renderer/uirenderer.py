import importlib

UI = "modernui"

UI_CINEMATIC = importlib.import_module(f"ulivy.interface.{UI}.uicinematic").UICinematic
UI_DEBUG = importlib.import_module(f"ulivy.interface.{UI}.uidebug").UIDebug
UI_PROMPT = importlib.import_module(f"ulivy.interface.{UI}.uiprompt").UIPrompt


class UIRenderer:
    def __init__(self, game):
        self.game = game
        self.current_ui = None

    def update(self, time, frame_time):
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
            self.game.remove_widget(self.current_ui)
            del self.current_ui
            self.current_ui = None

        if new_ui == "overworld":
            return None
        elif new_ui == "cinematic":
            self.current_ui = UI_CINEMATIC(self.game, gstate)
        elif new_ui == "debug":
            self.current_ui = UI_DEBUG(self.game, gstate)
        elif new_ui == "prompt":
            self.current_ui = UI_PROMPT(self.game, gstate)
        else:
            return

        self.current_ui.on_enter(**kwargs)
        self.game.add_widget(self.current_ui)
        self.current_ui.update()

