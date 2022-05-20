import math
from sympy import symbols, Eq, solve
import matplotlib.pyplot as plt
import complex_parser as cp


def alpha_curve(a, b, c, r):
    if a == r or b == r or c == r:
        res = False
    else:
        res = True
    return res