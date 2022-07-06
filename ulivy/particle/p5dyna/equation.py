from math import *
from numpy.random import rand


class Equation:
    def __init__(self, system, label, equation):
        self.system = system
        self.label = label
        self.equation = equation
        self.last_eval = None

    def reset_eval(self):
        self.last_eval = None

    def get(self, t):
        if self.last_eval is None:
            equation = self.system.p(self.equation, parse=False)
            self.last_eval = eval(equation)
        return self.last_eval
