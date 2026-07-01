"""
INDEPENDENT verifier v2 — STATIC ENERGY with SPATIAL 3-metric measure.
E = int (energy density) sqrt(g_spatial) d^3x,
g_spatial = diag(e^{2phi}, r^2, r^2 sin^2 th), sqrt = e^{phi} r^2 sin th.
energy density (static) = (xi/2) g^{ij} d_i n.d_j n + (kappa/4) g^{ia}g^{jb}F_ij.F_ab.
Frozen ansatz n=(sinTheta sin th cos(m ph), sinTheta sin th sin(m ph), cosTheta).
Compare to doc E2_r,E4_r.   agent: blind-verifier 2026-06-14
"""
import sympy as sp, random
r, th, ph = sp.symbols('r theta phi', real=True)
xi, kap, m = sp.symbols('xi kappa m', positive=True)
phi = sp.Function('phi')(r)
Th = sp.Function('Theta')(r)
sc = [r, th, ph]                                   # spatial coords

gs = sp.diag(sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)   # spatial 3-metric
gsi = gs.inv()
sqrtgs = sp.exp(phi)*r**2*sp.sin(th)                # e^{phi} r^2 sin th

n1 = sp.sin(Th)*sp.sin(th)*sp.cos(m*ph)
n2 = sp.sin(Th)*sp.sin(th)*sp.sin(m*ph)
n3 = sp.cos(Th)
n = [n1, n2, n3]
dn = sp.Matrix(3, 3, lambda i, a: sp.diff(n[a], sc[i]))

grad2 = sum(gsi[i, j]*dn[i, a]*dn[j, a] for i in range(3) for j in range(3) for a in range(3))
E2_dens = sp.Rational(1, 2)*xi*grad2*sqrtgs

def cross(u, v):
    return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
F = {(i, j): cross([dn[i, a] for a in range(3)], [dn[j, a] for a in range(3)])
     for i in range(3) for j in range(3)}
L4core = sum(gsi[i, ii]*gsi[j, jj]*sum(F[(i, j)][a]*F[(ii, jj)][a] for a in range(3))
             for i in range(3) for j in range(3) for ii in range(3) for jj in range(3))
E4_dens = sp.Rational(1, 4)*kap*L4core*sqrtgs

def ang_int(expr):
    e = sp.expand(sp.expand_trig(expr))
    e = sp.integrate(e, (ph, 0, 2*sp.pi))
    e = sp.expand(sp.expand_trig(sp.simplify(e)))
    return sp.simplify(sum(sp.integrate(t, (th, 0, sp.pi)) for t in sp.Add.make_args(e)))

E2_r = ang_int(E2_dens); E4_r = ang_int(E4_dens)
Thp = sp.diff(Th, r)
print("E2_r =", sp.simplify(E2_r))
print("E4_r =", sp.simplify(E4_r))

S = sp.sin(Th)
E2_doc = (2*sp.pi*xi/3)*sp.exp(-phi)*(r**2*S**2*Thp**2 + 2*r**2*Thp**2 + 4*sp.exp(2*phi)*m**2*S**2)
E4_doc = (2*sp.pi*kap/3)*sp.exp(-phi)*((2*r**2*S**4 + 2*r**2*S**2)*Thp**2 + sp.exp(2*phi)*m**2*S**4)/r**2

TpS, TS, pS, rS = sp.symbols('Tp T p rr', real=True)
def prep(e):
    e = e.subs(m, 1).subs(Thp, TpS).subs(Th, TS).subs(phi, pS).subs(r, rS).subs({xi: 1, kap: 1})
    return e
def ev(e, TT, TP, pp, rr):
    return float(prep(e).subs({TS: TT, TpS: TP, pS: pp, rS: rr}).evalf())
print("\n--- numeric comparison, m=1 ---")
m2 = m4 = True
for _ in range(8):
    TT, TP = random.uniform(0.1, 3.0), random.uniform(-2, 2)
    pp, rr = random.uniform(-3, 0), random.uniform(0.5, 5)
    a, b = ev(E2_r, TT, TP, pp, rr), ev(E2_doc, TT, TP, pp, rr)
    c, d = ev(E4_r, TT, TP, pp, rr), ev(E4_doc, TT, TP, pp, rr)
    print(f"  E2 mine={a:10.5f} doc={b:10.5f} | E4 mine={c:10.5f} doc={d:10.5f}")
    if abs(a-b) > 1e-9*max(1, abs(a)): m2 = False
    if abs(c-d) > 1e-9*max(1, abs(c)): m4 = False
print("E2 match doc:", m2, " E4 match doc:", m4)
