"""
Step 1: orthonormal tangent frame at the hedgehog n0, verified symbolically.
e1 = dn0/dTheta (normalized), e2 = n0 x e1.
Verify |e1|=|e2|=1, e1.n0=e2.n0=0, e1.e2=0 EXACTLY.
"""
import sympy as sp

r, th, ph = sp.symbols('r theta varphi', real=True)
Th = sp.symbols('Theta', real=True)   # treat Theta as a plain symbol here

n0 = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ph),
                sp.sin(Th)*sp.sin(th)*sp.sin(ph),
                sp.cos(Th)])

def cross(a,b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

# dn0/dTheta
dn0_dTh = sp.Matrix([sp.diff(c, Th) for c in n0])
norm_dn0 = sp.simplify(sp.sqrt(dn0_dTh.dot(dn0_dTh)))
print("|dn0/dTheta| =", norm_dn0, "  (NOT 1 in general -> must normalize)")
e1 = sp.simplify(dn0_dTh / norm_dn0)
e2 = sp.simplify(cross(n0, e1))

print("|n0|^2     =", sp.simplify(n0.dot(n0)))
print("|e1|^2     =", sp.simplify(e1.dot(e1)))
print("|e2|^2     =", sp.simplify(e2.dot(e2)))
print("e1.n0      =", sp.simplify(e1.dot(n0)))
print("e2.n0      =", sp.simplify(e2.dot(n0)))
print("e1.e2      =", sp.simplify(e1.dot(e2)))
print()
print("e1 =", e1.T)
print("e2 =", e2.T)
