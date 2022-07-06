"""function
Retrieve text input from the player.

Ask a question and request text input from the player. Text inputs can be limited to a specified length and can be filtered on symbols.
The result is stored afterwards in `game.text_input`.

in:
- String: question to ask
- [Optional, 15] Numeric: max length of answer
- [Optional, "letters"] String: filter to use

"""


class Prompt:
    def __init__(self, act, src, user, obj, length=15, filter="letters"):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.obj = obj
        self.src = src
        self.user = user
        self.filter = filter
        self.length = length
        self.act.game.m_gst.switch_state(
            "prompt", length=self.length, filter=self.filter
        )

    def on_tick(self, time=None, frame_time=None):
        if self.act.game.m_gst.current_state_name == "Prompt":
            return False
        return True

    def on_read(self):
        return None
