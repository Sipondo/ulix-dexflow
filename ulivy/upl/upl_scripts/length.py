"""fobject
Returns the length of the parameter.

Returns the Python length of the parameter. The length of lists and tuples equals their amount of elements. The length of strings equals their amount of characters.
in:
- List, tuple or string: parameter to measure the length of

out:
- Numeric: length of the parameter

"""


class Length:
    def __init__(self, act, src, user, s):
        self.init_time = act.current_time
        self.act = act
        self.src = src
        self.user = user
        self.game = act.game

        self.init_time = act.current_time
        self.s = s

    def on_read(self):
        return len(self.s)
