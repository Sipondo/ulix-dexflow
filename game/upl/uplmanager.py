from lark import Lark
from lark import Transformer

from game.upl.upl_scripts.cinematic import Cinematic
from game.upl.upl_scripts.debug import Debug
from game.upl.upl_scripts.jump import Jump
from game.upl.upl_scripts.say import Say
from game.upl.upl_scripts.move import Move
from game.upl.upl_scripts.overworld import Overworld
from game.upl.upl_scripts.portal import Portal
from game.upl.upl_scripts.setmovement import SetMovement
from game.upl.upl_scripts.wait import Wait


class UPLToPython(Transformer):
    def statement(self, source):
        if len(source) > 1:
            return (source[0], source[1])
        return source[0]

    def fcall(self, s):
        # print(s)
        return s[0](self.act, self.src, self.user, *s[1])

    def assign(self, s):
        # print("assign")
        # print(s)
        return exec(f"self.user.{s[0]}={s[1]}")

    def function(self, s):
        (s,) = s
        self = self.src
        ev = eval(s)
        return ev

    def user(self, s):
        (s,) = s
        username = str(s)
        # print("\n\nSWITCHING TO SOURCE:", username, "\n\n")
        self.user = self.parse_username(username)
        # print("Parsed User")
        return self.user  # username

    def object(self, s):
        (s,) = s
        return s

    def command(self, s):
        (s,) = s
        return s

    def assign_variable(self, s):
        (s,) = s
        return str(s)

    def variable(self, s):
        (s,) = s
        if "." in s and not "self." in s:
            username = str(s).split(".")[0]
            INTERNAL_VARIABLE = self.parse_username(username)
            s = ".".join(["INTERNAL_VARIABLE"] + str(s).split(".")[1:])
        self = self.src
        return eval(s)

    def compare(self, s):
        self = self.src
        return eval(" ".join([str(x) for x in s]))

    def bool(self, s):
        self = self.src
        return eval(" ".join([str(x) for x in s]))

    def bool_not(self, s):
        self = self.src
        return not eval(" ".join([str(x) for x in s]))

    def logic_and(self, s):
        return "and"

    def logic_or(self, s):
        return "or"

    def comp_greater_or_equal(self, s):
        return ">="

    def comp_greater(self, s):
        return ">"

    def comp_equal(self, s):
        return "=="

    def comp_smaller(self, s):
        return "<"

    def comp_smaller_or_equal(self, s):
        return "<="

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def say(self, s):
        (s,) = s
        return Say(self.act, self.src, self.user, s[1:-1])

    def number(self, n):
        (n,) = n
        return float(n)

    def comment(self, s):
        return None

    def exit_end(self, s):
        self.act.terminate()
        return None

    def parse_username(self, name):
        if name == "target":
            return self.src.target
        elif name == "player":
            return self.act.game.m_ent.player
        elif name == "switch":
            return self.act.game.m_sav.switches
        elif name == "set":
            return self.act.game.m_sav.settables
        elif name == "game":
            return self.act.game
        elif name[:2].lower() == "e_" and name[2:] in self.act.game.m_ent.entities:
            return self.act.game.m_ent.entities[name[2:]]

    upl = list
    fargs = list

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False


class UplManager:
    def __init__(self, game):
        self.game = game
        self.parser = UplParser()

    def parse(self, act, src, script):
        transformer = UPLToPython()
        transformer.act = act
        transformer.src = src
        # parse = self.parser.parse(script)
        parse = script
        # print("PARSE:", parse)
        # print(parse.data)
        # print("PARSE_LINES:", "\n\n\n".join([str(x) for x in parse.children]))
        # print(parse.pretty())
        return transformer.transform(parse)


class UplParser:
    def __init__(self):
        with open("game/upl/upl_grammar.lark", "r") as infile:
            self.parser = Lark(infile.read(), start="upl")  # , parser="lalr")

    def parse(self, script):
        return self.parser.parse(script)


# parser = UplParser()
# print(
#     parser.parse(
#         """
# !target: "Hey!"
# if((player.x + 3) > 3){
#     player: "Het kan zijn dat dit niet uitgevoerd wordt."
#     player: x = target.game_position[0] + 1
#     !group{
#         player: "Dit is gegroepeerd."
#     }
#     repeat(10){
#         player: "Dit doe ik 10 keer!"
#         break
#     }
# }else{
#     exit
# }
# player: Move(3,5)
# """
#     ).pretty()
# )
