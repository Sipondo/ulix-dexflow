from kivy.uix.floatlayout import FloatLayout

UI = "modernui"

from resources.armourui.interface.uicinematic import UICinematic
from resources.armourui.interface.uicombat import UICombat
from resources.basicui.interface.uidebug import UIDebug
from resources.basicui.interface.uimenubag import UIMenuBag
from resources.basicui.interface.uimenumain import UIMenuMain
from resources.armourui.interface.uimenustart import UIMenuStart
from resources.basicui.interface.uioverworld import UIOverworld
from resources.basicui.interface.uiprompt import UIPrompt
from resources.basicui.interface.uistatus import UIStatus


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
            self.current_ui = UIOverworld(self.game, gstate, size=self.size)
        elif new_ui == "cinematic":
            self.current_ui = UICinematic(self.game, gstate, size=self.size)
        elif new_ui == "debug":
            self.current_ui = UIDebug(self.game, gstate)
        elif new_ui == "prompt":
            self.current_ui = UIPrompt(self.game, gstate)
        elif new_ui == "battle":
            self.current_ui = UICombat(self.game, gstate)
        elif new_ui == "menumain":
            self.current_ui = UIMenuMain(self.game, gstate, size=self.size)
        elif new_ui == "menubag":
            self.current_ui = UIMenuBag(self.game, gstate)
        elif new_ui == "menustart":
            self.current_ui = UIMenuStart(self.game, gstate)
        elif new_ui == "status":
            self.current_ui = UIStatus(self.game, gstate)
        else:
            return

        self.current_ui.on_enter(**kwargs)
        self.add_widget(self.current_ui)
        self.current_ui.update()
