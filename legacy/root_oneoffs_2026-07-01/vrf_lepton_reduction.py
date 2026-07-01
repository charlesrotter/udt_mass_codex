"""
INDEPENDENT verifier of the FROZEN reduced 1D energy functional E[Theta].
Frozen ansatz (per native_derrick_derive.py / contract):
  n = (sinTheta(r) sin th cos(m ph), sinTheta sin th sin(m ph), cosTheta(r))
metric ds^2 = -e^{-2phi}dt^2 + e^{2phi}dr^2 + r^2 dOmega^2,
L2 = -(xi/2) g^{mn} d_m n.d_n n,  L4 = -(kappa/4)(d_m n x d_n n)^2.
Re-derived from scratch with sympy; compared to doc E2_r/E4_r.
agent: blind-verifier 2026-06-14
"""
import sympy as sp

r, th, ph, t = sp.symbols('r theta phi t', real=True)
xi, kap, m = sp.symbols('xi kappa m', positive=True)
phi = sp.Function('phi')(r)
Th = sp.Function('Theta')(r)
coords = [t, r, th, ph]

g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
sqrtg = sp.sqrt(sp.simplify(-g.det()))          # = e^{phi} r^2 sin th  (spatial e^{phi} r^2 sin th)
sqrtg = sp.simplify(sqrtg)

n1 = sp.sin(Th)*sp.sin(th)*sp.cos(m*ph)
n2 = sp.sin(Th)*sp.sin(th)*sp.sin(m*ph)
n3 = sp.cos(Th)
n = [n1, n2, n3]
dn = sp.Matrix(4, 3, lambda i, a: sp.diff(n[a], coords[i]))

# static energy density from L2 (spatial gradients only)
grad2 = 0
for i in [1, 2, 3]:
    for j in [1, 2, 3]:
        for a in range(3):
            grad2 += ginv[i, j]*dn[i, a]*dn[j, a]
E2_dens = sp.Rational(1, 2)*xi*grad2*sqrtg

# L4 Skyrme energy density
def cross(u, v):
    return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
F = {(i, j): cross([dn[i, a] for a in range(3)], [dn[j, a] for a in range(3)])
     for i in [1, 2, 3] for j in [1, 2, 3]}
L4core = 0
for i in [1, 2, 3]:
    for j in [1, 2, 3]:
        for ii in [1, 2, 3]:
            for jj in [1, 2, 3]:
                dot = sum(F[(i, j)][a]*F[(ii, jj)][a] for a in range(3))
                L4core += ginv[i, ii]*ginv[j, jj]*dot
E4_dens = sp.Rational(1, 4)*kap*L4core*sqrtg

def ang_int(expr):
    e = sp.expand(sp.expand_trig(expr))
    e = sp.integrate(e, (ph, 0, 2*sp.pi))
    e = sp.expand(sp.expand_trig(sp.simplify(e)))
    tot = 0
    for term in sp.Add.make_args(e):
        tot += sp.integrate(term, (th, 0, sp.pi))
    return sp.simplify(tot)

E2_r = ang_int(E2_dens)
E4_r = ang_int(E4_dens)
Thp = sp.diff(Th, r)
print("E2_r =", sp.simplify(E2_r))
print("E4_r =", sp.simplify(E4_r))

# Compare to DOC forms (m=1):
#  E2_r_doc = (2 pi xi/3) e^{-phi} [ r^2 sin^2Th Th'^2 + 2 r^2 Th'^2 + 4 e^{2phi} m^2 sin^2Th ]
#  E4_r_doc = (2 pi kap/3) e^{-phi} [ (2 r^2 sin^4Th + 2 r^2 sin^2Th)Th'^2 + e^{2phi} m^2 sin^4Th ]/r^2
S = sp.sin(Th)
E2_doc = (2*sp.pi*xi/3)*sp.exp(-phi)*(r**2*S**2*Thp**2 + 2*r**2*Thp**2 + 4*sp.exp(2*phi)*m**2*S**2)
E4_doc = (2*sp.pi*kap/3)*sp.exp(-phi)*((2*r**2*S**4 + 2*r**2*S**2)*Thp**2 + sp.exp(2*phi)*m**2*S**4)/r**2
print("\nE2_r - E2_doc =", sp.simplify(E2_r - E2_doc))
print("E4_r - E4_doc =", sp.simplify(E4_r - E4_doc))

# ---- numeric settle: are my E2_r,E4_r equal to doc forms on a test profile? ----
import random
TpS, TS, pS, rS = sp.symbols('Tp T p rr', real=True)
rep = {Thp: TpS, Th: TS, phi: pS, r: rS, m: 1}
def prep(expr):
    e = expr.subs(m, 1)
    e = e.subs(Thp, TpS)      # Derivative(Theta,r) -> Tp
    e = e.subs(Th, TS)        # Theta(r) -> T
    e = e.subs(phi, pS)       # phi(r) -> p   (whole function expression)
    e = e.subs(r, rS)         # bare r -> rr
    e = e.subs({xi: 1, kap: 1})
    return e
P2m, P2d, P4m, P4d = prep(E2_r), prep(E2_doc), prep(E4_r), prep(E4_doc)
print("free syms P2m:", P2m.free_symbols)
def ev(expr, TT, TP, pp, rr):
    return float(expr.subs({TS: TT, TpS: TP, pS: pp, rS: rr}).evalf())
print("\n--- numeric comparison on random points, m=1 ---")
m2 = m4 = True
for _ in range(6):
    TT = random.uniform(0.1, 3.0); TP = random.uniform(-2, 2)
    pp = random.uniform(-3, 0); rr = random.uniform(0.5, 5)
    a, b = ev(P2m, TT, TP, pp, rr), ev(P2d, TT, TP, pp, rr)
    c, d = ev(P4m, TT, TP, pp, rr), ev(P4d, TT, TP, pp, rr)
    print(f"  E2 mine={a:.5f} doc={b:.5f} | E4 mine={c:.5f} doc={d:.5f}")
    if abs(a-b) > 1e-9*max(1, abs(a)): m2 = False
    if abs(c-d) > 1e-9*max(1, abs(c)): m4 = False
print("E2 match doc:", m2, " E4 match doc:", m4)
