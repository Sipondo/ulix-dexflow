"""function
Ask a multiple choice question.

Ask the player a multiple choice question. Game must be in cinematic mode for the question to load properly.
Selected answer is stored afterwards in `game.selection` (id) and `game.selection_text` (option name).

in:
- String: question
- List of strings: options

"""


class Ask:
    def __init__(self, act, src, user, obj, options):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.obj = obj
        self.src = src
        self.user = user
        self.options = options
        self.act.game.m_gst.current_state.dialogue = self.obj
        self.act.game.m_gst.current_state.author = (
            "" if self.user == self.act.game else self.user.name
        )
        self.act.game.m_gst.current_state.options = self.options
        if hasattr(self.user, "splash") and self.user.splash:
            self.act.game.m_gst.current_state.spr_talker = self.user.splash

    def on_tick(self, time=None, frame_time=None):
        if self.act.game.m_gst.current_state.dialogue is not None:
            return False
        return True

    def on_read(self):
        return None
