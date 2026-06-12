"""Attack round 2:
 (a) what Einstein slot does the native H1 EL correspond to?  In GR the
     variation wrt g_tr gives the linearized (t,r) Einstein equation, NOT
     the (t,theta) weld.  Compute delta G_tr (lower) at first order and
     compare structures.
 (b) independent Lie-derivative spot check of K gauge-rigidity (ell=2).
 (c) numerical probe: with E0 < 0 (sourced collar), can the quadratic
     form go negative => REAL-omega mode exists (loophole in 'no real-omega
     modes')?  Vacuum E0=0 control included.
"""
import numpy as np
import sympy as sp

t, r, th, ph, eps = sp.symbols("t r theta phi epsilon", real=True)
c = sp.symbols("c", positive=True)
P0 = sp.Function("phi0", real=True)(r)
dp = sp.Function("dp", real=True)(t, r)
h1 = sp.Function("h1", real=True)(t, r)
kf = sp.Function("kk", real=True)(t, r)
Y = sp.Function("Y", real=True)(th)
f = sp.exp(-2 * P0)
P0p = sp.diff(P0, r)
X = [t, r, th, ph]
FAIL = []


def ck(lbl, ok):
    print(("PASS " if ok else "FAIL ") + lbl)
    if not ok:
        FAIL.append(lbl)


def o1(e):
    return sp.expand(sp.series(sp.expand(e), eps, 0, 2).removeO())


# ---------- (a) delta G_tr at first order ----------
g = sp.Matrix([
    [-f + eps * 2 * f * dp * Y, eps * h1 * Y, 0, 0],
    [eps * h1 * Y, 1 / f + eps * (2 / f) * dp * Y, 0, 0],
    [0, 0, r**2 * (1 + eps * kf * Y), 0],
    [0, 0, 0, r**2 * sp.sin(th)**2 * (1 + eps * kf * Y)]])
g0 = g.applyfunc(lambda e: sp.expand(e).coeff(eps, 0))
g1 = g.applyfunc(lambda e: sp.expand(e).coeff(eps, 1))
g0i = g0.inv()
gi = (g0i - eps * g0i * g1 * g0i).applyfunc(o1)
Gam = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
for a in range(4):
    for b in range(4):
        for d in range(b, 4):
            e = sum(gi[a, s] * (sp.diff(g[s, b], X[d]) + sp.diff(g[s, d], X[b])
                                - sp.diff(g[b, d], X[s])) for s in range(4)) / 2
            e = o1(e)
            Gam[a][b][d] = e
            Gam[a][d][b] = e
Ric = sp.zeros(4, 4)
for b in range(4):
    for d in range(b, 4):
        e = (sum(sp.diff(Gam[a][b][d], X[a]) for a in range(4))
             - sum(sp.diff(Gam[a][b][a], X[d]) for a in range(4))
             + sum(Gam[a][a][s] * Gam[s][b][d] for a in range(4) for s in range(4))
             - sum(Gam[a][d][s] * Gam[s][b][a] for a in range(4) for s in range(4)))
        Ric[b, d] = o1(e)
        Ric[d, b] = Ric[b, d]
Rsc = o1(sum(gi[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
Glow = (Ric - sp.Rational(1, 2) * Rsc * g).applyfunc(o1)
dG_tr = sp.simplify(Glow[0, 1].coeff(eps, 1))
print("delta G_tr (lower index, first order) =")
sp.pprint(sp.expand(dG_tr))
# does it contain Y'' (i.e. ell(ell+1)) content? does it contain h1 algebraically?
has_Ypp = dG_tr.has(sp.Derivative(Y, th, 2)) or dG_tr.has(sp.Derivative(Y, (th, 2)))
print("contains Y''(angular/ell-dependent) content:", has_Ypp)
print("contains h1:", dG_tr.has(h1), " contains d_r h1:",
      dG_tr.has(sp.Derivative(h1, r)))
# the GR H1-variation equation would be delta(G_tr - 8 pi G T_tr) = 0 — a
# DIFFERENT slot than the (t,theta) weld; record its structure for the report.

# ---------- (b) Lie-derivative spot check, ell = 2 ----------
T_, R_, Th_ = [sp.Function(n, real=True)(t, r) for n in ("Tg", "Rg", "Thg")]
Y2 = 3 * sp.cos(th)**2 - 1
xi_up = [T_ * Y2, R_ * Y2, Th_ * sp.diff(Y2, th), 0]
g0m = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)


def lie(mu, nu):
    return sp.expand(sum(xi_up[a] * sp.diff(g0m[mu, nu], X[a]) for a in range(4))
                     + sum(g0m[a, nu] * sp.diff(xi_up[a], X[mu]) for a in range(4))
                     + sum(g0m[mu, a] * sp.diff(xi_up[a], X[nu]) for a in range(4)))


# to remove K from g_thth AND g_phph simultaneously (keeping RW: no G-harmonic),
# need (L g)_thth = -r^2 K Y2 and (L g)_phph = -r^2 K Y2 sin^2 th.
Kc = sp.Function("Kc", real=True)(t, r)
eq1 = sp.expand(lie(2, 2) + r**2 * Kc * Y2)
eq2 = sp.expand(lie(3, 3) + r**2 * Kc * Y2 * sp.sin(th)**2)
sol = sp.solve([eq1.subs(th, sp.pi / 3), eq1.subs(th, sp.pi / 5),
                eq2.subs(th, sp.pi / 3)], [R_, Th_], dict=True)
ck("(b) ell=2: solving K-removal on the sphere block forces Theta = 0 and "
   "R = -rK/2 (unique)",
   len(sol) == 1 and sp.simplify(sol[0][Th_]) == 0
   and sp.simplify(sol[0][R_] + r * Kc / 2) == 0)
res1 = sp.simplify(eq1.subs(sol[0]))
res2 = sp.simplify(eq2.subs(sol[0]))
ck("(b) the unique solution actually removes K from BOTH sphere slots "
   "for all theta", res1 == 0 and res2 == 0)
rth = sp.simplify(lie(1, 2).subs(sol[0]).doit())
ck("(b) price: (L g)_rtheta = -e^{2phi0} (rK/2) d_th Y2 != 0 — leaves the "
   "RW/P0 class; K is NOT pure gauge at ell=2 (independent confirmation)",
   sp.simplify(rth + sp.exp(2 * P0) * (r * Kc / 2) * sp.diff(Y2, th)) == 0
   and rth != 0)

# ---------- (c) numerical probe of the no-real-omega claim ----------
# mode eq: (r^2 f^2 u')' = (om^2 r^2 + lam f + 4 r^2 f^2 E0) u, u(a)=u(b)=0.
# Rayleigh: om^2 = -min_u Q[u]/N[u],
#   Q = int r^2 f^2 u'^2 + (lam f + 4 r^2 f^2 E0) u^2,  N = int r^2 u^2.
# Vacuum E0=0 -> Q > 0 -> om^2 < 0 (script claim).  Sourced E0 < 0 -> ?
def probe(A, lamv=6.0, a=1.0, b=2.0, n=4000):
    rr = np.linspace(a, b, n)
    p0 = -A * (rr - 1.5)**2          # phi0 profile (E0<0 collar for A>0)
    p0p = -2 * A * (rr - 1.5)
    p0pp = -2 * A * np.ones_like(rr)
    fv = np.exp(-2 * p0)
    E0v = p0pp + 2 * p0p / rr - 2 * p0p**2
    # discretize SL operator: generalized eig  (-D(r2f2 D) + V) u = -om^2 r^2 u
    drr = rr[1] - rr[0]
    V = lamv * fv + 4 * rr**2 * fv**2 * E0v
    w_mid = (rr[:-1] + rr[1:]) / 2
    f_mid = np.exp(-2 * (-A * (w_mid - 1.5)**2))
    coef = w_mid**2 * f_mid**2
    m = n - 2
    K = np.zeros((m, m))
    for i in range(m):
        K[i, i] = (coef[i] + coef[i + 1]) / drr**2 + V[i + 1]
        if i + 1 < m:
            K[i, i + 1] = -coef[i + 1] / drr**2
            K[i + 1, i] = -coef[i + 1] / drr**2
    M = np.diag(rr[1:-1]**2)
    from scipy.linalg import eigh
    vals = eigh(K, M, eigvals_only=True, subset_by_index=[0, 0])
    return E0v.min(), E0v.max(), vals[0]   # om^2 = -lambda_min


try:
    from scipy.linalg import eigh  # noqa
    e0min, e0max, lmin = probe(0.0)
    print(f"(c) vacuum-like control A=0: E0 in [{e0min:.3g},{e0max:.3g}], "
          f"min gen-eig = {lmin:.4f}  => om^2 = {-lmin:.4f} (must be < 0)")
    ck("(c) control: E0=0 gives om^2 < 0 (no real-omega) — script claim "
       "confirmed numerically", lmin > 0)
    found = None
    for A in [0.5, 1.0, 1.5, 2.0, 3.0]:
        e0min, e0max, lmin = probe(A)
        print(f"(c) A={A}: E0 in [{e0min:.3g},{e0max:.3g}], min gen-eig = "
              f"{lmin:.4f} => om^2 = {-lmin:.4f}")
        if lmin < 0 and found is None:
            found = A
    ck("(c) LOOPHOLE WITNESS: a sourced collar with E0 < 0 admits a REAL-"
       "omega normal mode (om^2 > 0) under the same Dirichlet BCs — the "
       "'no real-omega' theorem requires E0 >= 0 (vacuum OK; sourced not "
       "guaranteed)", found is not None)
except ImportError:
    print("(c) scipy unavailable — skipped numeric probe")

print()
print(f"{len(FAIL)} failures" if FAIL else "ROUND-2 CHECKS COMPLETE (all pass)")
