import sympy as sp
E = {-1: sp.Rational(943,1000), -2: sp.Rational(5337,1000), -3: sp.Rational(8400,1000)}
print("E(-2)/E(-1) =", float(E[-2]/E[-1]))
print("E(-3)/E(-1) =", float(E[-3]/E[-1]))
import math
for q in [3,5]:
    print("pi^%d ="%q, math.pi**q)
print("ratio*pi^3 =", float(E[-2]/E[-1])*math.pi**3)
print("ratio*pi^5 =", float(E[-3]/E[-1])*math.pi**5)
