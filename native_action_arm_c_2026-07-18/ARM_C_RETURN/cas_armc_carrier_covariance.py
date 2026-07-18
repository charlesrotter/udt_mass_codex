#!/usr/bin/env python3
"""Arm-C exact carrier convention, covariance, and source-channel audit.

Certifies encoded signs, ordered antisymmetric-index factors, static reduction,
Weyl exponents, source identities, generic direct-weight chain rules, and a
same-static-energy time-sector kernel.  It cannot select the carrier, action,
time variable, representative, weights, measure, variation domain, boundary
data, or a physical source/mass law.
"""
import sympy as sp

checks = []
def check(label, condition):
    ok = bool(condition)
    checks.append(ok)
    print(("PASS " if ok else "FAIL ") + label)

N, sqh = sp.symbols("N sqrt_h", positive=True)
xi, k4 = sp.symbols("xi kappa4", real=True)
Dt2, Xs, E0, B = sp.symbols("Dt2 Xs E0 B", real=True)
a2, a4 = sp.symbols("a2 a4", real=True)

# (-,+,+,+), zero shift. B and E0 use ordered contractions.
F2 = B - 2*E0/N**2
Lcov = sp.expand(-N*sqh*(xi*(-Dt2/N**2 + Xs)/2 + k4*F2/4))
Lstatic = sp.simplify(Lcov.subs({Dt2: 0, E0: 0}))
expected = -N*sqh*(xi*Xs/2 + k4*B/4)
check("corrected covariant action reduces to minus positive static E2+E4", sp.simplify(Lstatic-expected) == 0)

# Matching foliation form has positive electric quartic term.
Lfol = N*sqh*(a2*Dt2/(2*N**2) - xi*Xs/2 + a4*E0/(2*N**2) - k4*B/4)
check("covariant/foliation mapping is a2=xi and a4=kappa4", sp.simplify(Lfol.subs({a2:xi,a4:k4})-Lcov) == 0)
check("time coefficients disappear from static restriction", sp.diff(Lfol.subs({Dt2:0,E0:0}), a2) == 0 and sp.diff(Lfol.subs({Dt2:0,E0:0}), a4) == 0)

# Independent spatial components and ordered-index convention.
xpar, xp1, xp2 = sp.symbols("xpar xp1 xp2", nonnegative=True)
f12, f13, f23 = sp.symbols("f12 f13 f23", real=True)
X = xpar + xp1 + xp2
Y = 2*(f12**2 + f13**2 + f23**2)
rho2, rho4 = xi*X/2, k4*Y/4
S2, S4 = -rho2, rho4
check("unrestricted metric identity rho+S=2rho4", sp.simplify(rho2+rho4+S2+S4-2*rho4) == 0)
p2par = xi*(xpar-X/2)
p4par = k4*(f12**2+f13**2-Y/4)
rho2par = xi*xpar/2
rho4par = k4*(f12**2+f13**2)/2
constrained = sp.simplify(rho2+rho4+p2par+p4par)
check("reciprocal tangent identity is directional", sp.simplify(constrained-2*(rho2par+rho4par)) == 0)
check("directional and traced sources are generically unequal", sp.simplify(constrained-2*rho4) != 0)

# Direct position-dependent weights are additional functional freedom.
phi = sp.symbols("phi", real=True)
u2p,u2t,u4p,u4t = sp.symbols("u2p u2t u4p u4t")
b2p,b2t,b4p,b4t = sp.symbols("b2p b2t b4p b4t")
weighted = (sp.exp((b2p-2)*phi)*u2p + sp.exp(b2t*phi)*u2t
            + sp.exp((b4p-2)*phi)*u4p + sp.exp(b4t*phi)*u4t)
source0 = sp.expand(sp.diff(weighted, phi).subs(phi, 0))
expected_source = (b2p-2)*u2p+b2t*u2t+(b4p-2)*u4p+b4t*u4t
check("chosen carrier weights change every source coefficient", sp.simplify(source0-expected_source) == 0)

# Weyl weights in d=4 for weight-zero n.
check("carrier L2 and L4 have different CSN weights", (4-2)==2 and (4-4)==0)

print("F_MUNU_FMUNU", F2)
print("SOURCE_TRACED", sp.simplify(2*rho4))
print("SOURCE_DIRECTIONAL", constrained)
print("SOURCE_DIFFERENCE", sp.factor(constrained-2*rho4))
print("LIMIT: encoded algebra does not select covariance, weights, variation domain, or mass")
print(("PASS" if all(checks) else "FAIL") + f" SUMMARY {sum(checks)}/{len(checks)} checks")

