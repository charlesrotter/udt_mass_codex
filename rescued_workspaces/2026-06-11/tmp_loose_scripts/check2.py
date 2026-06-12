import sympy as sp
from sympy import Ynm, symbols, Abs, exp, I

theta, phi = symbols('theta phi', real=True)
# General: Y_l^m = N * P_l^m(cos theta) * e^{i m phi}, so |Y|^2 = N^2 P^2, phi drops out.
# Demonstrate the phi factor explicitly:
l,m = 3,2
Y = Ynm(l,m,theta,phi)
# factor out exp(I m phi)
ratio = sp.simplify(Y / sp.exp(I*m*phi))
print("Y_3^2 / e^{i m phi} (phi-free?):", "phi" in str(ratio.free_symbols) and "still has phi" or ratio)
print("free symbols:", ratio.free_symbols)

# Part 3 arithmetic
for lG,name in [(0,'electron'),(1,'muon'),(2,'proton')]:
    print(f"{name}: l_G={lG} -> 2 l_G+1 = {2*lG+1}")
