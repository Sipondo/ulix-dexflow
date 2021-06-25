from lark import Lark


with open("game/upl/test_grammar.lark", "r") as infile:
    json_parser = Lark(infile.read(), start="value",)


# text = '{"key": ["item0", "item1", 3.14, true]}'

text = """
red: "I am a dude."
red: move(5, 5, 3, "hey")
"""
print(json_parser.parse(text).pretty())


# from lark import Transformer

# class TreeToJson(Transformer):
#     def string(self, s):
#         (s,) = s
#         return s[1:-1]
#     def number(self, n):
#         (n,) = n
#         return float(n)

#     list = list
#     pair = tuple
#     dict = dict

#     null = lambda self, _: None
#     true = lambda self, _: True
#     false = lambda self, _: False


# tree = json_parser.parse(text)
# TreeToJson().transform(tree)

