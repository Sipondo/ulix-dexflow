from ulivy.interface.baseui import BaseUI
from kivy.lang import Builder

Builder.load_file("resources/armourui/interface/uioverworld.kv")


class UIOverworld(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.show_area = 3

    def update(self, time=None, frame_time=None):
        if time is None:
            time = 0
            frame_time = 0.05
        if (
            self.game.m_map.areaname is not None
            and self.game.m_map.areaname
            and self.game.m_map.areaname != self.game.last_visited_name
        ):
            self.game.last_visited_name = self.game.m_map.areaname
            self.show_area = 0

        self.ids.AreaText.text = self.game.last_visited_name

        self.ids.AreaWindow.opacity = 0
        if self.show_area < 3:
            self.show_area += frame_time
            if self.show_area < 0.5:
                self.ids.AreaWindow.opacity = min(1, self.show_area * 2)
            elif self.show_area > 2.5:
                self.ids.AreaWindow.opacity = max(0, 6.0 - self.show_area * 2)
            else:
                self.ids.AreaWindow.opacity = 1

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
            self.game.m_gst.switch_state("status")
        if key == "zoom_in":
            self.game.pan_tool.zoom_in()
        if key == "zoom_out":
            self.game.pan_tool.zoom_out()
        if key == "debug":
            self.game.m_gst.switch_state("debug")

    def event_unicode(self, char):
        pass
