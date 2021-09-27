"""function
Set the game to cinematic mode.

Set the game to cinematic mode, preventing player movement. Cinematic mode is required for showing character speech.
Make sure to revert to overworld or battle mode when your cinematic finishes.

in:
No arguments

"""


class Cinematic:
    def __init__(self, act, src, user, letterbox=True):
        act.funcs.append(self)
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.letterbox = letterbox
        self.act.game.m_gst.switch_state("cinematic", letterbox=self.letterbox)

    def on_tick(self, time=None, frame_time=None):
        return True

    def on_read(self):
        return None
