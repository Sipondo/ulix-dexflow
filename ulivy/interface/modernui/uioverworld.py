from ..baseui import BaseUI
from kivy.lang import Builder


class UIOverworld(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False

    def update(self, time=None, frame_time=None):
        return False

    def event_keypress(self, key, modifiers):
        if key == "alt":
            self.game.m_ent.player.set_movement_type(0)
        elif key == "shift":
            self.game.m_ent.player.set_movement_type(1)
        elif key == "ctrl" and self.game.m_map.allow_cycle:
            self.game.m_ent.player.set_movement_type(2)
        if key == "interact":
            self.game.m_act.check_interact()
        if key == "backspace":
            self.game.m_gst.switch_state("menumain")
        if key == "zoom_in":
            self.game.pan_tool.zoom_in()
        if key == "zoom_out":
            self.game.pan_tool.zoom_out()
        if key == "debug":
            self.game.m_gst.switch_state("debug")

    def event_unicode(self, char):
        pass
