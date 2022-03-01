"""function
Say some lines of text.

Say some lines of text. Can be accessed conveniently by supplying a string directly as a function.
Multiline strings are supported via explicit function call but not via the shortcut.

in:
- String: dialogue to show

"""


class Say:
    def __init__(self, act, src, user, dialogue):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.dialogue = dialogue

        self.act.game.m_gst.current_state.dialogue = self.dialogue
        self.act.game.m_gst.current_state.author = (
            "" if self.user == self.act.game else self.user.name
        )
        if hasattr(self.user, "splash") and self.user.splash:
            self.act.game.m_gst.current_state.spr_talker = self.user.splash

    def on_tick(self, time=None, frame_time=None):
        if self.act.game.m_gst.current_state.dialogue is not None:
            return False
        return True

    def on_read(self):
        return None
