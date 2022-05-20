from cmath import pi
from sympy import symbols, Eq, solve, Symbol
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import complex_parser as cp
import math


def a_residue(a, b, c, n, m):
    z_0 = complex(0, a)
    f = f"(z**{n})/((z-{b})*((z+({c}j))**4))"
    z = Symbol('z')
    f_z = parse_expr(f)
    print(f_z)
    f_z_prime = f_z.diff(z, m-1)
    f_z_prime = f_z_prime.subs([(z, z_0)])
    f_z_prime = complex(f_z_prime/math.factorial(m-1))
    return f_z_prime

def b_residue(a, b, c, n, m):
    z_0 = complex(b, 0)
    f = f"(z**{n})/(((z-{a}j)**{m})*((z+({c}j))**4))"
    z = Symbol('z')
    f_z = parse_expr(f)
    print(f_z)
    f_z_prime = f_z.diff(z, 0)
    f_z_prime = f_z_prime.subs([(z, z_0)])
    f_z_prime = complex(f_z_prime/math.factorial(0))
    return f_z_prime

def c_residue(a, b, c, n, m):
    z_0 = complex(0, -c)
    f = f"(z**{n})/(((z-{a}j)**{m})*(z-{b}))"
    z = Symbol('z')
    f_z = parse_expr(f)
    print(f_z)
    f_z_prime = f_z.diff(z, 3)
    f_z_prime = f_z_prime.subs([(z, z_0)])
    f_z_prime = complex(f_z_prime/math.factorial(3))
    return f_z_prime

def residue(a, b, c, n, m, r):
    if abs(a) > r:
        a_res = complex(0, 0)
    else:
        a_res = a_residue(a, b, c, n, m)
    
    if abs(b) > r:
        b_res = complex(0, 0)
    else:
        b_res = b_residue(a, b, c, n, m)
    
    if abs(c) > r:
        c_res = complex(0, 0)
    else:
        c_res = c_residue(a, b, c, n, m)
    
    return complex(2 * math.pi * complex('j')* (a_res + b_res + c_res))