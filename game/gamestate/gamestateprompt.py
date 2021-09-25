from .basegamestate import BaseGameState


class GameStatePrompt(BaseGameState):
    def on_enter(self, length=15, filter="all"):
        self.input = ""
        self.filter = filter
        self.block_input = True
        self.length = length

        self.initialised = False

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
        self.game.r_int.draw_rectangle(
            (0.28, 0.34), to=(0.72, 0.46), col="black",
        )
        self.game.r_int.draw_text(
            self.input, (0.3, 0.36), to=(0.7, 0.44), col="black",
        )

    def event_unicode(self, char):
        if len(self.input) >= self.length:
            return
        if self.filter == "letters":
            if not char.isalpha():
                return
        self.input += char

    def event_keypress(self, key, modifiers):
        if key == "backspace":
            if len(self.input):
                self.input = self.input[:-1]
        if key == "enter":
            print("Input:", self.input)
            self.game.text_input = self.input
            self.game.m_gst.switch_to_previous_state()

