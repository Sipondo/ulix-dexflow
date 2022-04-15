import importlib

UI = "modernui"

UI_CINEMATIC = importlib.import_module(f"ulivy.interface.{UI}.uicinematic").UICinematic


class UIRenderer:
    def __init__(self, game):
        self.game = game
        self.current_ui = None

    def switch_ui(self, new_ui, **kwargs):
        if self.current_ui is not None:
            self.current_ui.on_exit()
            self.game.remove_widget(self.current_ui)
            del self.current_ui

        if new_ui == "overworld":
            return None
        elif new_ui == "cinematic":
            self.current_ui = UI_CINEMATIC(self.game)
        else:
            return

        self.current_ui.on_enter(**kwargs)
        self.game.add_widget(self.current_ui)

