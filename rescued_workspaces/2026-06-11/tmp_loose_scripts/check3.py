import sympy as sp
from sympy import Ynm, symbols, exp, I, simplify
theta, phi = symbols('theta phi', real=True)
for (l,m) in [(3,2),(2,1),(4,3)]:
    Y = Ynm(l,m,theta,phi).expand(func=True)
    ratio = simplify(Y/exp(I*m*phi))
    print(f"(l,m)=({l},{m}): Y/e^(i m phi) free symbols =", ratio.free_symbols)
