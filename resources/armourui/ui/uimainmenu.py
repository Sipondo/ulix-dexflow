from kivy.lang import Builder

from ulivy.interface.baseui import BaseUI

Builder.load_file("resources/armourui/ui/uimainmenu.kv")

class UIMainMenu(BaseUI):
    def on_enter(self, **kwargs):
        self.block_input = False
        self.show_area = 3

        self.options = ["dex", "mon", "bag", "card", "save", "map", "camp", "gift", "vs", "options"]
        self.selection = 0

    def update(self, time=None, frame_time=None):
        # if time is None:
        #     time = 0
        #     frame_time = 0.05
        # if (
        #     self.game.m_map.areaname is not None
        #     and self.game.m_map.areaname
        #     and self.game.m_map.areaname != self.game.last_visited_name
        # ):
        #     self.game.last_visited_name = self.game.m_map.areaname
        #     self.show_area = 0

        # self.ids.AreaText.text = self.game.last_visited_name

        self.ids.AreaWindow.opacity = 1
        # if self.show_area < 3:
        #     self.show_area += frame_time
        #     if self.show_area < 0.5:
        #         self.ids.AreaWindow.opacity = min(1, self.show_area * 2)
        #     elif self.show_area > 2.5:
        #         self.ids.AreaWindow.opacity = max(0, 6.0 - self.show_area * 2)
        #     else:
        #         self.ids.AreaWindow.opacity = 1

        self.highlight_options()

        return False

    def highlight_options(self):
        """Highlight menu options.
        We significantly reduce boilerplate by making the filenames
        and elementnames correspond to the options list.
        This allows us to get the element attribute in a for loop.
        """        
        for option in self.options:
            element = getattr(self.ids, f"Option{option.capitalize()}")
            if option == self.options[self.selection]:
                element.source = f"resources/armourui/graphics/interface/main_menu/{option}_sel.png"
                self.ids.Arrow.pos_hint = {'center_x': element.pos_hint['center_x']  - 0.055, 'center_y': element.pos_hint['center_y']}
            else:    
                element.source = f"resources/armourui/graphics/interface/main_menu/{option}.png"


    def event_keypress(self, key, modifiers):
        if key == "down":
            self.selection = (self.selection - (len(self.options)//2)) % len(self.options)
        elif key == "up":
            self.selection = (self.selection + (len(self.options)//2)) % len(self.options)
        elif key == "left":
            self.selection = (self.selection - 1) % len(self.options)
        elif key == "right":
            self.selection = (self.selection + 1) % len(self.options)
        elif key == "backspace":
            self.game.r_uin.close_ui(self)
        # if key == "alt":
        #     self.game.m_ent.player.set_movement_type(0)
        # elif key == "shift":
        #     self.game.m_ent.player.set_movement_type(1)
        # elif key == "ctrl" and self.game.m_map.allow_cycle:
        #     self.game.m_ent.player.set_movement_type(2)
        # if key == "interact":
        #     self.game.m_act.check_interact()
        # if key == "backspace":
        #     self.game.m_gst.switch_state("status")
        # if key == "zoom_in":
        #     self.game.pan_tool.zoom_in()
        # if key == "zoom_out":
        #     self.game.pan_tool.zoom_out()
        # if key == "debug":
        #     self.game.m_gst.switch_state("debug")

    def event_unicode(self, char):
        pass
