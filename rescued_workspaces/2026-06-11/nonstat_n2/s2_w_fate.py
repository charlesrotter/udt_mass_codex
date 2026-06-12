"""NONSTATIONARY SECTOR N2 — script 2: THE w-FATE (fork adjudicator).

Setting (from s1, all 29 checks PASS):
  After exact elimination of the time row (a,b) [K=0, S* branch; the only
  nondegenerate branch — theorem T1 below], the reduced Lagrangian is
      L* = -(c/8) sqrt(B) [f P + D2 vT^2] / (f sqrt(f D2)) * sgn(Q),
      P  = A vr^2 - 2 q vr vh + vh^2/f,   D2 = A/f - q^2,
      Q  = f P - D2 vT^2,   R = f P + D2 vT^2,
  with q and w (A = r^2(1+w)^2, B = r^2 sin^2/(1+w)^2) pointwise algebraic.
  Stationarity (envelope theorem):
      E1 (q):  vT^2 q^3 + (f A vr^2 + vh^2 - (A/f) vT^2) q - 2 A vr vh = 0
      E2 (w):  brack := -R f D2 + 2A(f vr^2 + vT^2/f) f D2 - A R = 0
  E1 is degree 1 in A  =>  A(q) = -q (vT^2 q^2 + vh^2) / (q g - 2 vr vh),
      g := f vr^2 - vT^2/f.
  Substituting A(q) into brack gives the one-variable FATE POLYNOMIAL.
  Admissibility: A > 0, D2 > 0 (Lorentzian), Q != 0 records the branch.

This script: T1 (K!=0 branch emptiness, exact), T2 (small-vh expansion,
exact), T3 (the fate polynomial, exact factorization), N1 (exhaustive
numeric root scan over parameter space), VERDICT.
"""
import numpy as np
import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label)

def zero_cancel(e):
    return sp.cancel(sp.together(e)) == 0

f, A = sp.symbols('f A', positive=True)
q = sp.Symbol('q', real=True)
vT, vr, vh = sp.symbols('v_T v_r v_theta', real=True)

D2 = A / f - q**2
P = A * vr**2 - 2 * q * vr * vh + vh**2 / f
R = sp.expand(f * P + D2 * vT**2)
Q = sp.expand(f * P - D2 * vT**2)
g = f * vr**2 - vT**2 / f

# ===================================================================== T1
# K != 0 branch of the time-row elimination is EMPTY of nondegenerate
# stationary points. Conditions: eqK/K = 2 Del P + N D2 = 0 and the
# S-equation; show every solution forces Delta = 0 (degenerate metric).
Ssym, Ksym = sp.symbols('S K', real=True)
Nf = D2 * vT**2 - 2 * vT * Ssym - f * P - Ksym**2
Delf = f * D2 + (Ssym**2 + D2 * Ksym**2) / P
eqS = 2 * sp.diff(Nf, Ssym) * Delf - Nf * sp.diff(Delf, Ssym)
eqK_factor = 2 * Delf * P + Nf * D2
# On eqK_factor = 0: Delta = -N D2/(2P). Substitute into eqS:
eqS_sub = sp.cancel(sp.together(eqS.subs(Delf, -Nf * D2 / (2 * P))))
# eqS with Delf replaced symbolically: rebuild eqS from scratch with Del symbol
Dsym = sp.Symbol('Delta', positive=True)
eqS_form = 2 * sp.diff(Nf, Ssym) * Dsym - Nf * (2 * Ssym / P)
eqS_on_branch = sp.expand(eqS_form.subs(Dsym, -Nf * D2 / (2 * P)) * P)
fac = sp.factor(eqS_on_branch)
print("    S-equation on the K-branch factors as:", fac)
check("T1a: S-equation on the K-branch = (2/P) N (v_T D2 - S) structure",
      zero_cancel(eqS_on_branch - 2 * Nf * (vT * D2 - Ssym) / P * P))
# Case N = 0: Delta = -N D2/(2P) = 0 -> degenerate. Case S = vT D2:
N_case2 = sp.expand(Nf.subs(Ssym, vT * D2))
check("T1b: at S = vT D2, N = -(R + K^2)",
      zero_cancel(N_case2 + R + Ksym**2))
Del_case2 = sp.cancel(Delf.subs(Ssym, vT * D2))
check("T1c: at S = vT D2, Delta = D2 (R + K^2)/P",
      zero_cancel(Del_case2 - D2 * (R + Ksym**2) / P))
branch_eq = sp.cancel(sp.together(eqK_factor.subs(Ssym, vT * D2)))
check("T1d: K-branch equation reduces to D2 (R + K^2) = 0  => Delta = 0 "
      "in every case: K!=0 BRANCH EMPTY (nondegenerate)",
      zero_cancel(branch_eq - D2 * (R + Ksym**2)))
print("    => the K=0, S=S* branch is the UNIQUE nondegenerate time-row "
      "elimination. (Theorem)")

# ===================================================================== T2
# Small-vh expansion of the w-residual ON the q-branch connected to q*:
# q = q1 eps + O(eps^3), q1 = 2 vr/g; residual of brack = 2 A h /g eps^2 ...
eps = sp.Symbol('epsilon')
h = f * vr**2 + vT**2 / f
brack = sp.expand(-R * f * D2 + 2 * A * h * f * D2 - A * R)
q1 = 2 * vr / g
brack_eps = brack.subs({vh: eps, q: q1 * eps})
ser = sp.series(sp.together(brack_eps), eps, 0, 4).removeO()
c0 = sp.simplify(ser.coeff(eps, 0)); c1 = sp.simplify(ser.coeff(eps, 1))
c2 = sp.simplify(sp.together(ser.coeff(eps, 2)))
check("T2a: brack O(1) and O(eps) vanish on the q1-branch", c0 == 0 and c1 == 0)
c2_expected = 2 * A * h / g
check("T2b: brack = +(2 A h / g) vh^2 + O(vh^4)  [h > 0 always]",
      zero_cancel(c2 - c2_expected))
print("    => near-spherical w-residual NEVER vanishes for real data;")
print("       its SIGN FLIPS across the radial sonic locus g = f vr^2 - vT^2/f = 0.")

# ===================================================================== T3
# THE FATE POLYNOMIAL: substitute A(q) into brack; factor exactly.
Aq = sp.cancel(-q * (vT**2 * q**2 + vh**2) / (q * g - 2 * vr * vh))
E1 = vT**2 * q**3 + (f * A * vr**2 + vh**2 - (A / f) * vT**2) * q - 2 * A * vr * vh
check("T3a: A(q) solves E1 exactly", zero_cancel(E1.subs(A, Aq)))
fate = sp.together(brack.subs(A, Aq))
fate_num = sp.factor(sp.numer(fate))
fate_den = sp.factor(sp.denom(fate))
print("    FATE numerator factors:")
print("      ", fate_num)
print("    FATE denominator factors:")
print("      ", fate_den)
# Also the admissibility quantities on the A(q) curve:
D2q = sp.cancel(D2.subs(A, Aq))
print("    D2 on the curve:", sp.factor(D2q))
Qq = sp.cancel(Q.subs(A, Aq))
print("    Q  on the curve:", sp.factor(Qq))

# ===================================================================== N1
# Exhaustive numeric scan: for each (f, vr, vh, vT) find ALL real roots of
# the fate polynomial in q, then test A(q) > 0 and D2 > 0 (admissible w*).
fate_poly = sp.Poly(sp.expand(fate_num), q)
coeff_funcs = [sp.lambdify((f, vr, vh, vT), cc, 'numpy')
               for cc in fate_poly.all_coeffs()]
Aq_f = sp.lambdify((q, f, vr, vh, vT), Aq, 'numpy')
D2_f = sp.lambdify((q, A, f), D2, 'numpy')
Q_f = sp.lambdify((q, A, f, vr, vh, vT), Q, 'numpy')
brackA_f = sp.lambdify((q, A, f, vr, vh, vT), brack, 'numpy')
E1_f = sp.lambdify((q, A, f, vr, vh, vT), E1, 'numpy')

rng = np.random.default_rng(20260611)

# EXACT THEOREM (from the T3 factorization, verified above):
#   fate numerator = -2 f q vh (f q vr - vh)^3      [vT ABSENT]
#   D2 on the A(q) curve = -q (f q vr - vh)^2 / denA
#   A(q=0) = 0;  q = vh/(f vr)  =>  D2 = 0.
# Hence EVERY joint root of (E1, E2) is metric-degenerate (A = 0 or D2 = 0)
# for ALL vT — shaped (vh != 0) configurations are excluded dynamically
# exactly as statically. Special slices (exact):
#   vr = 0: fate numerator = +2 f q vh^4 => q = 0; then E2 = -2 A vh^2 != 0
#   vh = 0: q = 0 solves E1 for all A; E2 identically satisfied (flat w)
#   E1 A-coefficient zero (q g = 2 vr vh): forces q = 0 & vr vh = 0 (above)
import sympy as _sp
fate_num_expected = -2 * f * q * vh * (f * q * vr - vh)**3
check("N0a: fate numerator == -2 f q vh (f q vr - vh)^3  (vT-FREE)",
      zero_cancel(sp.expand(fate_num) - sp.expand(fate_num_expected))
      or zero_cancel(sp.expand(fate_num) + sp.expand(fate_num_expected)))
print("    sign convention: fate_num =", sp.factor(fate_num))
check("N0b: D2 on curve = -q (f q vr - vh)^2/denA  (root q=vh/(f vr) is degenerate)",
      zero_cancel(sp.factor(D2q) - (-q * (f * q * vr - vh)**2 /
                                    (f**2 * q * vr**2 - 2 * f * vr * vh - q * vT**2))))
check("N0c: A(0) = 0  (root q=0 is degenerate)", sp.simplify(Aq.subs(q, 0)) == 0)
# vr = 0 slice exact:
fate_vr0 = sp.factor(sp.simplify(fate_num.subs(vr, 0)))
brack_q0_vr0 = sp.expand(brack.subs({q: 0, vr: 0}))
check("N0d: vr=0 slice: fate => q=0, then brack = -2 A vh^2 (+ vT-free) != 0",
      zero_cancel(fate_vr0 - 2 * f * q * vh**4) and
      zero_cancel(brack_q0_vr0 + 2 * A * vh**2))
# vh = 0 slice exact (moving spherical: w flat):
check("N0e: vh=0: E1 => q=0 (all A); brack(q=0, vh=0) == 0 identically",
      zero_cancel(brack.subs({q: 0, vh: 0})))

# NUMERIC CROSS-CHECK: every real root of the fate polynomial coincides
# with one of the two exact (degenerate) roots; no stray admissible root.
fate_poly = sp.Poly(sp.expand(fate_num), q)
coeff_funcs = [sp.lambdify((f, vr, vh, vT), cc, 'numpy')
               for cc in fate_poly.all_coeffs()]
n_root = 0
n_classified = 0
for _ in range(60000):
    fv = float(np.exp(rng.uniform(np.log(0.01), np.log(100.0))))
    vrv = float(rng.normal() * 10**rng.uniform(-1, 1))
    vhv = float(rng.normal() * 10**rng.uniform(-1, 1))
    vTv = float(rng.normal() * 10**rng.uniform(-1, 1))
    if abs(vrv) < 1e-8 or abs(vhv) < 1e-8:
        continue
    coeffs = np.array([cf(fv, vrv, vhv, vTv) for cf in coeff_funcs], float)
    nzi = np.nonzero(np.abs(coeffs) > 1e-300)[0]
    if len(nzi) == 0 or len(coeffs[nzi[0]:]) < 2:
        continue
    for rt in np.roots(coeffs[nzi[0]:]):
        # triple-root splitting under roundoff scales as eps_mach^(1/3)
        # ~ 6e-6 relative; use 1e-3 relative classification tolerance and
        # accept the near-real splittings of the exact triple root.
        qtrip = vhv / (fv * vrv)
        scale = max(1.0, abs(rt.real), abs(qtrip))
        if abs(rt.imag) > 1e-3 * scale:
            continue
        qv = rt.real
        n_root += 1
        d0 = abs(qv)
        d1 = abs(qv - qtrip)
        if min(d0, d1) <= 1e-3 * scale:
            n_classified += 1
print(f"    numeric: {n_root} real fate-roots, {n_classified} classified as "
      "one of the two exact degenerate roots")
check("N1: every numeric real fate-root is one of the two exact degenerate "
      "roots (q=0 [A=0] or q=vh/(f vr) [D2=0]) — NO admissible w* exists",
      n_root > 1000 and n_classified == n_root)

print()
print("VERDICT (THE w-FATE): the w-equation remains UNSATISFIABLE off-")
print("spherical for ALL time dependence — the fate polynomial is vT-FREE.")
print("Motion does NOT source shape. P1's static theorem extends verbatim")
print("to the full nonstationary even sector: solution set =")
print("  { f(T,r) spherical-gradient, q = 0, b = 0, a = a*(f,f_T,f_r),")
print("    w arbitrary flat direction }  U  degenerate-metric corners.")
print("Fork branch (i) [nonstationary matter rescues shape] is REFUTED")
print("mechanically in this class; a native w-stiffness sector (fork (ii))")
print("is FORCED for shaped matter. The w-force never vanishes off-")
print("spherical; its direction flips across the radial sonic locus")
print("g = f vr^2 - vT^2/f = 0  (subsonic: toward degeneracy, as static).")

print()
print("PASS:", len(PASS), " FAIL:", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
    raise SystemExit(1)
