from kivy.uix.floatlayout import FloatLayout
import ulivy.interface.baseui

UI = "modernui"

class UIRenderer(FloatLayout):
    def __init__(self, game, **kwargs):
        self.game = game
        self.ui_stack = []
        super(UIRenderer, self).__init__(**kwargs)
        self.size_hint_x = None
        self.size_hint_y = None
        self.size = self.game.RENDER_SIZE

        self.ui_dictionary = {}

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
        
    def register_ui(self, name, ui):
        self.ui_dictionary[name] = ui

    def switch_ui(self, new_ui, gstate, replace=False, **kwargs):
        if replace:
            for ui in self.ui_stack[::-1]:
                if ui.on_exit():
                    self.remove_widget(ui)
                    del ui

            self.ui_stack = []

        try:
            self.ui_stack.append(self.ui_dictionary[new_ui](self.game))
        except KeyError:
            raise KeyError(f"UI '{new_ui}' was requested but has not been registered.")

        self.current_ui.on_enter(**kwargs)
        self.add_widget(self.current_ui)
        self.current_ui.update()

    def close_ui(self, ui):
        if ui.on_exit():
            self.remove_widget(ui)
            self.ui_stack.remove(ui)
            del ui

    @property
    def current_ui(self):
        if self.ui_stack:
            return self.ui_stack[-1]
        return None
