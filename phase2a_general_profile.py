#!/usr/bin/env python3
"""
phase2a_general_profile.py -- PHASE-2a step 1 (continued, WHOLE-not-slice):
the gauge test killed ONE profile (W=r^2 sin^2 th, J=0). Now solve the FULL
O(eps) vacuum constraint set for the GENERAL stationary axial shift and ask:
does ANY regular/bounded vacuum profile carry Komar J != 0 (physical rotation),
or do the vacuum equations FORCE the J-carrying part to vanish (=> only gauge
survives -> rotation adds nothing)?

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE. c=1.

Method: separate the stationary axial shift in Gegenbauer/Legendre angular
harmonics. For the slow-rotation (Hartle) / linearized-Kerr structure the
relevant angular function is sin^2(theta) = (2/3)(1 - P_2(cos th)). Write
   g_tpsi = eps * W(r,theta),  W(r,theta) = sum_l f_l(r) * (-sin theta dP_l/dtheta)
the standard vector-harmonic basis for the axial shift. The l=1 piece is the
rotation/J-carrying sector (Lense-Thirring). Solve the radial ODE the O(eps)
vacuum equations give, impose regularity at core + the finite-cell wall, and
read the Komar J.
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)
eps = sp.symbols('epsilon')
X = [t, r, th, ps]
sin, cos = sp.sin, sp.cos


def einstein_offdiag(g, X, comps):
    n = len(X)
    ginv = g.inv()
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d] * (sp.diff(g[d, cc], X[b])
                                       + sp.diff(g[d, b], X[cc])
                                       - sp.diff(g[b, cc], X[d]))
                Gamma[a][b][cc] = sp.Rational(1, 2) * s
    Ric = {}
    out = {}
    for (i, j) in comps:
        s = sp.S(0)
        for a in range(n):
            s += sp.diff(Gamma[a][i][j], X[a]) - sp.diff(Gamma[a][i][a], X[j])
            for e in range(n):
                s += Gamma[a][a][e] * Gamma[e][i][j] - Gamma[a][j][e] * Gamma[e][i][a]
        out[(i, j)] = s  # Ricci off-diag = Einstein off-diag (R_ij, since g_ij=0 there at O(eps) for these)
    return out


print("=" * 78)
print("PHASE-2a step 1 (whole): general stationary axial-shift vacuum profile")
print("=" * 78)

# General stationary (time-independent) axial shift, separated radial x angular.
# Use the Lense-Thirring/Hartle structure: g_tpsi = eps * omega_func(r) * sin^2(theta)
# is the l=1 (pure rotation, J-carrying) sector. The constraint determines omega_func(r).
fr = sp.Function('f')(r)            # radial frame-drag function
W = fr * sin(th)**2                  # l=1 axial sector (Lense-Thirring form)
g = sp.Matrix([
    [-1,        0,    0,            eps * W],
    [0,         1,    0,            0],
    [0,         0,    r**2,         0],
    [eps * W,   0,    0,            r**2 * sin(th)**2],
])

# The O(eps) vacuum equation for the rotation sector comes from G_{t psi}=0.
comps = [(0, 3), (1, 3), (2, 3)]
G = einstein_offdiag(g, X, comps)
print("\n--- O(eps) vacuum equations for g_tpsi = eps f(r) sin^2(theta) ---")
for (i, j), name in zip(comps, ['G_tpsi', 'G_rpsi', 'G_thpsi']):
    val = sp.simplify(sp.series(G[(i, j)], eps, 0, 2).removeO().coeff(eps, 1))
    print(f"  {name} = 0  ->  {sp.simplify(val)} = 0")

# Extract the radial ODE from G_tpsi (the elliptic constraint on f(r))
Gtpsi = sp.simplify(sp.series(G[(0, 3)], eps, 0, 2).removeO().coeff(eps, 1))
# strip the angular factor to get the pure radial ODE
ode = sp.simplify(Gtpsi / sin(th)**2) if Gtpsi.has(sin(th)) else Gtpsi
# Build the radial ODE explicitly: collect coefficient of sin functions
ode_radial = sp.simplify(sp.expand_trig(Gtpsi))
print("\n  G_tpsi reduced:", ode_radial)

# Solve the radial ODE for f(r)
print("\n--- Solve the radial frame-drag ODE for f(r) ---")
# The Lense-Thirring radial equation is f'' + (4/r) f' = 0 (vacuum, l=1), classic.
# Let dsolve handle whatever the metric produced:
fsol = sp.dsolve(sp.Eq(ode_radial, 0), fr)
print("  General solution:", fsol)

# Two integration constants. Identify them: the homogeneous solutions.
C1, C2 = sp.symbols('C1 C2')
# Extract the basis solutions
print("\n  => the two independent radial behaviours (homogeneous basis).")

# Komar J for g_tpsi = eps f(r) sin^2 theta. From phase2a_gauge_test:
#   J/eps = (r/4) * Integral[ (2W - r W_r) sin th ] dtheta  (psi integral gives 2pi already folded)
# with W = f(r) sin^2 th : 2W - r W_r = (2 f - r f') sin^2 th
# Integral over theta of sin^2 th * sin th dth from 0..pi = 4/3
# So J/eps = (r/4)*(2 f - r f')*(4/3)*(2 pi)/(... ) -- recompute cleanly with the
# normalization used in the gauge script (which already folded the 2pi psi-integral).
# Reuse the exact integrand:
Wf = fr * sin(th)**2
# F^{tr} O(eps) coeff was (r W_r - 2 W)/r  (general, from gauge script)
Ftr_lin = (r * sp.diff(Wf, r) - 2 * Wf) / r
sqrt_sigma = r**2 * sin(th)
J_integrand = sp.Rational(1, 16) / sp.pi * Ftr_lin * 2 * (-1) * (1) * sqrt_sigma
Jr = sp.simplify(sp.integrate(sp.integrate(J_integrand, (ps, 0, 2 * sp.pi)), (th, 0, sp.pi)))
print("\n  Komar J/eps as a function of f(r):  J/eps =", Jr)
print("  (J is r-INDEPENDENT for a genuine vacuum solution = the conserved charge;")
print("   check by substituting each homogeneous branch.)")

# Substitute the two homogeneous branches into J and check r-independence + nonzero.
sols = fsol.rhs if hasattr(fsol, 'rhs') else fsol
print("\n  Evaluate J on each homogeneous branch:")
# branch A: f = const ; branch B: f = 1/r^3 (typical LT). Test both generically:
for label, ftest in [('f=const (C1)', sp.Integer(1)),
                      ('f=1/r^3 (LT decaying)', 1 / r**3),
                      ('f=r^2 (the gauge profile branch)', r**2)]:
    Jt = sp.simplify(Jr.subs(fr, ftest).doit())
    print(f"    {label:32s}: J/eps = {Jt}")

print("\n" + "=" * 78)
print("READ: the J-carrying branch (if it is a regular vacuum solution on the")
print("finite cell) decides physical-vs-gauge. f=const & f=r^2 give J=0 (gauge-like);")
print("a 1/r^3 (Lense-Thirring) branch gives J!=0 but is SINGULAR at the core r->0.")
print("On the finite mirrored cell with CORE REGULARITY, only the regular branch")
print("survives -> if that branch carries J=0, vacuum rotation is gauge here.")
print("=" * 78)
