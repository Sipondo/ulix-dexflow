from lark import Lark
from lark import Transformer


with open("game/upl/upl_grammar.lark", "r") as infile:
    parser = Lark(infile.read(), start="upl",)


def portalconnection(a, b, c):
    print(a, b, c)


class UPLToPython(Transformer):
    def statement(self, source):
        return (source[0], source[1])

    def fcall(self, s):
        return s[0](*s[1])

    def function(self, s):
        (s,) = s
        return portalconnection

    def source(self, s):
        (s,) = s
        return str(s)

    def object(self, s):
        (s,) = s
        return str(s)

    def command(self, s):
        (s,) = s
        return s

    def variable(self, s):
        (s,) = s
        self = testclass
        return eval(s)

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def number(self, n):
        (n,) = n
        return float(n)

    upl = list
    fargs = list

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False


class Test:
    def __init__(self):
        self.target_level = "L2"
        self.target_coords = (20, 35)
        self.direction = "N"


testclass = Test()

text = """
target: portalconnection(self.target_level, self.target_coords, self.direction)
"""

print(parser.parse(text).pretty())


code_parser = parser.parse(text)
UPLToPython().transform(code_parser)

