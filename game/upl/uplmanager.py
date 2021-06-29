from lark import Lark
from lark import Transformer

from game.upl.upl_scripts.portal import portal

# with open("game/upl/upl_grammar.lark", "r") as infile:
#     parser = Lark(infile.read(), start="upl",)


class UPLToPython(Transformer):
    def statement(self, source):
        return (source[0], source[1])

    def fcall(self, s):
        print(s)
        return s[0](self.src, *s[1])

    def function(self, s):
        (s,) = s
        return portal

    def source(self, s):
        (s,) = s
        return str(s)

    def object(self, s):
        (s,) = s
        return s

    def command(self, s):
        (s,) = s
        return s

    def variable(self, s):
        (s,) = s
        self = self.src
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


class UplManager:
    def __init__(self, game):
        self.game = game
        with open("game/upl/upl_grammar.lark", "r") as infile:
            self.parser = Lark(infile.read(), start="upl", parser="lalr")

    def parse(self, src, script):
        transformer = UPLToPython()
        transformer.src = src
        transformer.transform(self.parser.parse(script))


# class Test:
#     def __init__(self):
#         self.target_level = "L2"
#         self.target_coords = (20, 35)
#         self.direction = "N"


# testclass = Test()

# text = """
# target: portalconnection(self.target_level, self.target_coords, self.direction)
# """

# print(parser.parse(text).pretty())


# code_parser = parser.parse(text)
# UPLToPython().transform(code_parser)

