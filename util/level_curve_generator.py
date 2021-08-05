import numpy as np
import math
import pandas as pd
from pathlib import Path

file_path = Path("../resources/base/PBS")


def get_erratic_level_exp(n):
    if n < 50:
        return math.floor((n**3 * (100 - n)) / 50)
    if n < 68:
        return math.floor((n**3 * (150 - n)) / 100)
    if n < 98:
        return math.floor((n**3 * ((1911 - 10 * n) // 3)) / 500)
    return (n**3 * (160 - n)) // 100


def get_slow_level_exp(n):
    return math.floor((5 * n**3) / 4)


def get_medium_slow_level_exp(n):
    return math.floor(((6 * n**3) / 5)) - (15 * n**2) + (100 * n) - 140


def get_medium_fast_level_exp(n):
    return n**3


def get_fast_level_exp(n):
    return math.floor((4 * n**3) / 5)


def get_fluctuating_level_exp(n):
    if n < 15:
        return math.floor(n**3 * ((((n+1) // 3) + 24) / 50))
    if n < 36:
        return math.floor(n**3 * ((n + 14)/50))
    return math.floor(n**3 * (((n//2) + 32) / 50))


curves = np.ndarray((6, 99), dtype=np.int32)
for i, f in enumerate((get_fast_level_exp, get_medium_fast_level_exp, get_medium_slow_level_exp, get_slow_level_exp, get_fluctuating_level_exp, get_erratic_level_exp)):
    curves[i] = np.vectorize(f)(np.arange(2, 101))
exp_needed = curves.copy()
for i in range(6):
    for j in range(98, 0, -1):
        exp_needed[i][j] = curves[i][j] - curves[i][j-1]


curves = curves.T
exp_needed = exp_needed.T
panda_data = pd.DataFrame(curves, index=range(2, 101), columns=["Fast", "Medium", "Parabolic", "Slow", "Fluctuating", "Erratic"])
panda_data_exp = pd.DataFrame(exp_needed, index=range(1, 100), columns=["Fast", "Medium", "Parabolic", "Slow", "Fluctuating", "Erratic"])
panda_data.to_csv(file_path / "level_curves.csv")
panda_data_exp.to_csv(file_path / "level_exp.csv")
