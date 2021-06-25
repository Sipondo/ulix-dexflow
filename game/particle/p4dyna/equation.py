from math import *


class Equation:
    def __init__(self, system, label, equation):
        self.system = system
        self.label = label
        self.equation = equation

    def get(self, t):
        equation = self.system.p(self.equation, parse=False)
        return eval(equation)
