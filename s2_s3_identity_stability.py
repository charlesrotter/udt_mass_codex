#!/usr/bin/env python3
"""
s2_s3_identity_stability.py -- decompose the n_4 source into L2/L4, determine the
POTENTIAL CHARACTER at X=0 (well => S^2 demanded; hill => S^3), and resolve the
Part-2/Part-4 native-vs-Lagrange equality.  sympy-exact.  DATA-BLIND.

Builds on s2_s3_identity_derive.py.  TRIPWIRE: distinguish a DEMAND (X=0 forced) from
a PERMIT (X=0 merely allowed).  The decisive object is the X-direction POTENTIAL and
its curvature at X=0, AND whether any term sources X AWAY from 0.
"""
import sympy as sp

r, th, ps = sp.symbols('r theta psi', positive=True)
xi, kap, m = sp.symbols('xi kappa m', positive=True)
A = sp.Function('A')(r); B = sp.Function('B')(r)
ginv = sp.diag(-sp.exp(-2*A), sp.exp(-2*B), 1/r**2, 1/(r**2*sp.sin(th)**2))
sqrtg = sp.exp(A+B)*r**2*sp.sin(th)

def dot(a, b): return (a.T*b)[0, 0]
def cross3(a, b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

X = sp.Function('X')(r)
u1 = sp.sin(th)*sp.cos(m*ps); u2 = sp.sin(th)*sp.sin(m*ps); u3 = sp.cos(th)
n = sp.Matrix([sp.cos(X)*u1, sp.cos(X)*u2, sp.cos(X)*u3, sp.sin(X)])
dn = [sp.zeros(4, 1) for _ in range(4)]
for a_ in range(4):
    dn[1][a_] = sp.diff(n[a_], r); dn[2][a_] = sp.diff(n[a_], th); dn[3][a_] = sp.diff(n[a_], ps)
Gf = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Gf[mu, nu] = dot(dn[mu], dn[nu])

L2 = -(xi/2)*sum(ginv[i, i]*Gf[i, i] for i in range(4))
dn3 = [sp.Matrix(dn[mu][0:3]) for mu in range(4)]
def Snat(mu, nu): return cross3(dn3[mu], dn3[nu])
L4nat = -(kap/4)*sum(ginv[a, a]*ginv[b, b]*dot(Snat(a, b), Snat(a, b))
                     for a in range(4) for b in range(4))

def radEL(Lden):
    Lr = sp.simplify(sp.integrate(sp.integrate(sp.simplify(Lden*sqrtg),
                     (ps, 0, 2*sp.pi)), (th, 0, sp.pi)))
    Xp = sp.diff(X, r)
    return sp.simplify(sp.diff(sp.diff(Lr, Xp), r) - sp.diff(Lr, X)), Lr

print("="*78); print("L2 vs L4 decomposition of the n_4 SOURCE term"); print("="*78)
EL2, _ = radEL(L2)
EL4, _ = radEL(L4nat)
Xp = sp.diff(X, r)
src2 = sp.simplify(EL2.subs({sp.diff(X, r, 2): 0, Xp: 0}))
src4 = sp.simplify(EL4.subs({sp.diff(X, r, 2): 0, Xp: 0}))
print("\nL2 source (X'=X''=0):"); sp.pprint(src2)
print("\nL4_native source (X'=X''=0):"); sp.pprint(src4)
print("\n=> L4_native contributes to the n_4 source?  ", src4 != 0)

print("\n" + "="*78)
print("THE X-DIRECTION POTENTIAL V(X) (non-gradient part of the energy)")
print("="*78)
# energy density = -L (static). The X-direction POTENTIAL = the part with no X'.
# Build the angular-integrated energy, drop X' terms => V(X).
Lr2 = sp.simplify(sp.integrate(sp.integrate(sp.simplify(L2*sqrtg),
                  (ps, 0, 2*sp.pi)), (th, 0, sp.pi)))
Lr4 = sp.simplify(sp.integrate(sp.integrate(sp.simplify(L4nat*sqrtg),
                  (ps, 0, 2*sp.pi)), (th, 0, sp.pi)))
V = sp.simplify((-(Lr2+Lr4)).subs(Xp, 0))   # potential = -L with no gradient
print("\nV(X) (radial-gradient-free energy density) =")
sp.pprint(sp.simplify(V))
dV = sp.simplify(sp.diff(V, X))
d2V = sp.simplify(sp.diff(V, X, 2))
print("\ndV/dX =", sp.simplify(dV))
print("dV/dX at X=0  =", sp.simplify(dV.subs(X, 0)), "  (0 => X=0 is a critical point)")
print("d2V/dX2 at X=0 =", sp.simplify(d2V.subs(X, 0)))
c = sp.simplify(d2V.subs(X, 0))
print("\nsign of d2V/dX2|_{X=0}: coefficients all positive (xi,kappa,m,r>0, e^{..}>0)?")
print("  d2V/dX2|_0 =", c)
# X = pi/2 (pure 4th-axis pole) curvature:
print("\nd2V/dX2 at X=pi/2 =", sp.simplify(d2V.subs(X, sp.pi/2)))

print("\n" + "="*78)
print("VERDICT LOGIC")
print("="*78)
print("""If dV/dX|_{X=0}=0 AND d2V/dX2|_{X=0} > 0:  X=0 is a POTENTIAL MINIMUM in the
4th-component direction. Then n_4=0 (pure S^2) is the STABLE configuration the
energy DEMANDS -- not merely permits -- because any X!=0 costs energy and rolls
BACK to X=0. The only way to hold X!=0 is to IMPOSE it by a boundary condition
(the Skyrme Theta(core)=m*pi import). That is the DEMANDS-level S^2 argument.

If instead d2V/dX2|_{X=0} < 0: X=0 is a hill, n_4 would be sourced ON dynamically
=> genuine S^3. (Watch this sign; it is the whole question.)""")
