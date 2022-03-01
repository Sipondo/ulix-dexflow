from lark import Lark
from lark import Transformer
from pathlib import Path
import re

from ulivy.upl.upl_scripts.additem import AddItem
from ulivy.upl.upl_scripts.addmember import AddMember
from ulivy.upl.upl_scripts.ask import Ask
from ulivy.upl.upl_scripts.battle import Battle
from ulivy.upl.upl_scripts.checkcollision import CheckCollision
from ulivy.upl.upl_scripts.cinematic import Cinematic
from ulivy.upl.upl_scripts.concat import Concat
from ulivy.upl.upl_scripts.countitem import CountItem
from ulivy.upl.upl_scripts.debug import Debug
from ulivy.upl.upl_scripts.encounter import Encounter
from ulivy.upl.upl_scripts.face import Face
from ulivy.upl.upl_scripts.fade import Fade
from ulivy.upl.upl_scripts.flushtiles import FlushTiles
from ulivy.upl.upl_scripts.getentities import GetEntities
from ulivy.upl.upl_scripts.gettile import GetTile
from ulivy.upl.upl_scripts.isentity import IsEntity
from ulivy.upl.upl_scripts.jump import Jump
from ulivy.upl.upl_scripts.length import Length
from ulivy.upl.upl_scripts.manhattan import Manhattan
from ulivy.upl.upl_scripts.move import Move
from ulivy.upl.upl_scripts.moveto import MoveTo
from ulivy.upl.upl_scripts.music import Music
from ulivy.upl.upl_scripts.overworld import Overworld
from ulivy.upl.upl_scripts.portal import Portal
from ulivy.upl.upl_scripts.prompt import Prompt
from ulivy.upl.upl_scripts.push import Push
from ulivy.upl.upl_scripts.random import Random
from ulivy.upl.upl_scripts.removeitem import RemoveItem
from ulivy.upl.upl_scripts.resetlocalencounters import ResetLocalEncounters
from ulivy.upl.upl_scripts.restoreparty import RestoreParty
from ulivy.upl.upl_scripts.say import Say
from ulivy.upl.upl_scripts.setlocalencounters import SetLocalEncounters
from ulivy.upl.upl_scripts.setmovement import SetMovement
from ulivy.upl.upl_scripts.settile import SetTile
from ulivy.upl.upl_scripts.shop import Shop
from ulivy.upl.upl_scripts.sound import Sound
from ulivy.upl.upl_scripts.step import Step
from ulivy.upl.upl_scripts.storage import Storage
from ulivy.upl.upl_scripts.teleport import Teleport
from ulivy.upl.upl_scripts.updatetiles import UpdateTiles
from ulivy.upl.upl_scripts.unfade import Unfade
from ulivy.upl.upl_scripts.wait import Wait


class UPLToPython(Transformer):
    def statement(self, source):
        if len(source) > 1:
            return (source[0], source[1])
        return source[0]

    def fcall(self, s):
        # print(s)
        return s[0](self.act, self.src, self.user, *s[1])

    def fcall_object(self, s):
        # print(s)
        return s[0](self.act, self.src, self.user, *s[1]).on_read()

    def assign(self, s):
        if isinstance(s[0], str) and hasattr(
            self.user, ".".join(s[0].split(".")[:-1]) or s[0]
        ):
            user = self.user
            s[0] = f"user.{s[0]}"
        elif "." in s[0] and not "self." in s[0]:
            username = str(s[0]).split(".")[0]
            INTERNAL_VARIABLE = self.parse_username(username)
            s = ".".join(["INTERNAL_VARIABLE"] + str(s[0]).split(".")[1:])
        elif INTERNAL_VARIABLE := self.parse_username(s[0]):
            s[0] = "INTERNAL_VARIABLE"
        elif "self." in s[0]:
            pass
        else:
            user = self.user
            s[0] = f"user.{s[0]}"

        self = self.src
        return exec(f"{s[0]}=s[1]")

    def function(self, s):
        (s,) = s
        self = self.src
        return eval(s)

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
        if isinstance(s, str) and hasattr(self.user, ".".join(s.split(".")[:-1]) or s):
            user = self.user
            s = f"user.{s}"
        elif "." in s and not "self." in s:
            username = str(s).split(".")[0]
            INTERNAL_VARIABLE = self.parse_username(username)
            s = ".".join(["INTERNAL_VARIABLE"] + str(s).split(".")[1:])
        elif INTERNAL_VARIABLE := self.parse_username(s):
            s = "INTERNAL_VARIABLE"
        self = self.src
        # print(s)
        # print(eval(s))
        return eval(s)

    def index(self, s):
        INTERNAL_A = s[0]
        INTERNAL_B = s[1]
        if isinstance(INTERNAL_B, float):
            INTERNAL_B = int(INTERNAL_B)
        self = self.src
        return eval(f"INTERNAL_A[INTERNAL_B]")

    def compare(self, s):
        self = self.src
        a = s[0]
        b = s[2]
        return eval(f"a {s[1]} b")
        # print("COMPARING:", " ".join([str(x) for x in s]))
        # return eval(" ".join([str(x) for x in s]))

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

    def comp_nequal(self, s):
        return "!="

    def comp_smaller(self, s):
        return "<"

    def comp_smaller_or_equal(self, s):
        return "<="

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def multiline(self, s):
        (s,) = s
        return s[3:-3]

    def list(self, items):
        return list(items)

    def tuple(self, items):
        return tuple(items)

    def say(self, s):
        (s,) = s
        return Say(self.act, self.src, self.user, s[1:-1])

    def number(self, n):
        if len(n) == 1:
            (n,) = n
            return float(n)

        return eval(f"float(n[0]) {n[1]} float(n[2])")

    def comment(self, s):
        return None

    def exit_end(self, s):
        self.act.terminate()
        return None

    def parse_username(self, name):
        ret = None
        if name == "target":
            ret = self.src.target
        elif name == "self":
            ret = self.src
        elif name == "player":
            ret = self.act.game.m_ent.player
        elif name == "switch":
            ret = self.act.game.m_sav.switches
        elif name == "set":
            ret = self.act.game.m_sav.settables
        elif name == "local":
            ret = self.act.game.m_sav.locals
        elif name == "global":
            ret = self.act.game.m_sav.globals
        elif name == "game":
            ret = self.act.game
        elif name == "col":
            ret = self.act.game.m_col
        elif name == "map":
            ret = self.act.game.m_map
        elif name[:2].lower() == "e_" and name[2:] in self.act.game.m_ent.entities:
            ret = self.act.game.m_ent.entities[name[2:]]

        if ret is None:
            return
        else:
            if hasattr(ret, "entity_is_deleted") and ret.entity_is_deleted:
                raise Exception(f"User {name} has been deleted.")
        return ret

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
        self.resource_dirs = list(Path("").glob("resources/*/"))
        self.upl_files = {}
        for directory in self.resource_dirs:
            for file in (directory / "upl").glob("**/*.upl"):
                if file.stem not in self.upl_files:
                    with open(file) as infile:
                        self.upl_files[file.stem] = infile.read()
        with open("ulivy/upl/upl_grammar.lark", "r") as infile:
            self.parser = Lark(infile.read(), start="upl")  # , parser="lalr")

    def parse(self, script):
        outscript = ""
        while outscript != script:
            outscript = script
            for k, v in self.upl_files.items():
                script = re.sub(f"<<<{k}>>>", v, script, flags=re.M,)
        return self.parser.parse(outscript)


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
