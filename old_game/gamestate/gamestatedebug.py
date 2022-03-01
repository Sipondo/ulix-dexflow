from .basegamestate import BaseGameState


class GameStateDebug(BaseGameState):
    def on_enter(self):
        self.input = ""
        self.block_input = True

        self.initialised = False
        pass

    def on_tick(self, time, frame_time):
        self.time = time

        if not self.initialised:
            self.initialised = True
            self.input = ""

        self.game.m_ent.render()
        return False

    def on_exit(self):
        pass

    def on_render(self, time, frame_time):
        self.game.r_int.draw_text(
            """Go where? [map x y]\nOr run an UPL command.""",
            (0.3, 0.2),
            to=(0.7, 0.31),
        )
        self.game.r_int.draw_rectangle(
            (0.28, 0.34), to=(0.72, 0.46), col="black",
        )
        self.game.r_int.draw_text(
            self.input, (0.3, 0.36), to=(0.7, 0.44), col="black",
        )

    def event_unicode(self, char):
        self.input += char

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            if len(self.input):
                self.input = self.input[:-1]
        if key == "enter":
            print("Debug:", self.input)
            try:
                self.game.debug_input = self.input.split(" ")
                mapstring = self.game.m_map.convert_mapstring_to_key(
                    self.game.debug_input[0]
                )
                y, x = self.game.m_map.get_level_size(mapstring)
                if len(self.game.debug_input) == 1:
                    self.game.debug_input.append(y // 2)
                if len(self.game.debug_input) == 2:
                    self.game.debug_input.append(x // 2)
                self.game.m_gst.switch_to_previous_state()
                self.game.m_act.create_prefab_action("debug_teleport", self.game)
            except Exception as e:
                self.game.debug_input = ""
                try:
                    upl = self.game.m_upl.parser.parse(self.input)
                    self.game.m_gst.switch_to_previous_state()
                    self.game.m_act.create_action(upl, self.game)
                except Exception as e:
                    try:
                        upl = self.game.m_upl.parser.parse(f"game: {self.input}")
                        self.game.m_gst.switch_to_previous_state()
                        self.game.m_act.create_action(upl, self.game)
                    except Exception as e:
                        print("\n\n>>>DEBUG COMMAND INVALID<<<", self.input, "\n" * 2)
                        self.game.m_gst.switch_to_previous_state()

