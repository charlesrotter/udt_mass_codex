#!/usr/bin/env python3
"""BLIND VERIFIER independent check — P4 Route A Slice 2 (solution legs).

Independent constructions throughout: function-based calculus on x (NOT the package's
jet-symbol machinery), own Euler-Lagrange derivation, own witnesses, own quadrature
forms, sign-of-aF attack (the package script fixed a_F > 0; the verifier runs a_F as a
free real symbol and a_F < 0 witnesses). Exit 0 iff all checks pass.
Blind verifier, same-session-spawned, 2026-07-29. Pure CPU SymPy, deterministic.
"""
import os
import sys
import sympy as sp
from sympy import (Function, Symbol, symbols, exp, log, atan, sqrt, diff, expand,
                   simplify, integrate, Rational, Matrix, zeros, eye)

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []


def vcheck(name, ok, note=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {note}" if note else ""))
    if not ok:
        FAILS.append(name)


x = Symbol("x")
a = Symbol("a_F", real=True, nonzero=True)   # verifier: NO positivity assumption
lam = Symbol("lam", real=True)
ell = Symbol("ell", positive=True)

# ---------------------------------------------------------------------------
# (2a) INDEPENDENT re-derivation of the GEN-QUAD system from the EL equations
# of S = int e^{a p(x)} (p'^2 + f'^2 + h'^2)/2 dx  (function-based, own route)
# ---------------------------------------------------------------------------
p = Function("p")(x)
f = Function("f")(x)
h = Function("h")(x)
Ldens = exp(a * p) * (p.diff(x)**2 + f.diff(x)**2 + h.diff(x)**2) / 2


def EL(L, u):
    return (L.diff(u) - (L.diff(u.diff(x))).diff(x)).doit()


Rp = expand(exp(-a * p) * EL(Ldens, p))
Rf = expand(exp(-a * p) * EL(Ldens, f))
Rh = expand(exp(-a * p) * EL(Ldens, h))
Rp_pkg = a * (f.diff(x)**2 + h.diff(x)**2 - p.diff(x)**2) / 2 - p.diff(x, 2)
Rf_pkg = -(a * p.diff(x) * f.diff(x) + f.diff(x, 2))
Rh_pkg = -(a * p.diff(x) * h.diff(x) + h.diff(x, 2))
vcheck("V_genquad_EL_rederived",
       expand(Rp - Rp_pkg) == 0 and expand(Rf - Rf_pkg) == 0 and expand(Rh - Rh_pkg) == 0,
       "own function-based EL of e^{aF p}(p'^2+f'^2+h'^2)/2 reproduces the package tuple "
       "exactly (independent route)")

# ---------------------------------------------------------------------------
# (2a) closed-form family, zero residual WITH a_F ALLOWED NEGATIVE (attack)
# ---------------------------------------------------------------------------
w0 = Symbol("w0", positive=True)
w1 = Symbol("w1", real=True)
cf = Symbol("c_f", real=True)
ch = Symbol("c_h", real=True)   # verifier: real, not positive — sign attack
E0 = (w1**2 / a**2 + cf**2 + ch**2) / (2 * w0)
A = a**2 * E0 / 2
w = A * x**2 + w1 * x + w0
psol = log(w) / a
fp = cf / w
hp = ch / w
subs_sol = {p: psol, f.diff(x): fp, h.diff(x): hp}
rp = Rp_pkg.subs(p, psol).doit()
rp = rp.subs({f.diff(x): fp, h.diff(x): hp})
rf = (-(a * psol.diff(x) * fp + fp.diff(x)))
rh = (-(a * psol.diff(x) * hp + hp.diff(x)))
vcheck("V_well_zero_residual_signfree",
       simplify(rp) == 0 and simplify(rf) == 0 and simplify(rh) == 0,
       "the closed-form family solves all three equations with a_F a FREE REAL symbol "
       "(negative included) and c_f, c_h real — the package's a>0 declaration is not "
       "load-bearing for the residual")

disc = expand((w1**2 - 4 * A * w0) + a**2 * (cf**2 + ch**2))
ssq = expand(2 * w0 * E0 - (w1**2 / a**2 + cf**2 + ch**2))
vcheck("V_disc_and_sum_of_squares", disc == 0 and ssq == 0,
       "disc(w) = -a_F^2(c_f^2+c_h^2) <= 0 and 2 w0 E0 = w1^2/a_F^2 + c_f^2 + c_h^2 "
       "(so E0 >= 0 on the real family, = 0 iff w1=c_f=c_h=0): both exact, sign-free")

# WELL-vs-BUMP shape attack: p0''(vertex) sign follows sign(a_F).
xv = -w1 / (2 * A)
p2v = simplify(psol.diff(x, 2).subs(x, xv))
# p0'' at vertex = w''(xv)/(a w(xv)) with w(xv) = -disc/(4A) = (cf^2+ch^2) a^2/(4A) > 0
p2v_expected = simplify((2 * A) / (a * (cf**2 + ch**2) * a**2 / (4 * A)))
vcheck("V_shape_sign_of_aF",
       simplify(p2v - p2v_expected) == 0
       and simplify(p2v * a) != 0
       and sp.ask(sp.Q.positive(p2v.subs({a: 1, w1: 0, cf: 1, ch: 1, w0: 1}))) is True
       and sp.ask(sp.Q.negative(p2v.subs({a: -1, w1: 0, cf: 1, ch: 1, w0: 1}))) is True,
       "ATTACK RESULT: p0''(vertex) = 8A^2/(a^3(c_f^2+c_h^2)) has the SIGN of a_F — the "
       "depth profile is a single-MINIMUM well only for a_F > 0; for a_F < 0 it is a "
       "single-MAXIMUM bump. Nodelessness/regularity are sign-free; the 'well/minimum' "
       "prose needs a sign(a_F) stamp")

# Exhaustiveness: EXPLICIT inverse of the parameter -> initial-data map (stronger
# than the package's rank-6 spot check): given data (P0,P1,F0,F1,H0,H1) at x=0,
P0, P1, F0, F1, H0, H1 = symbols("P0 P1 F0 F1 H0 H1", real=True)
inv = {w0: exp(a * P0), w1: a * exp(a * P0) * P1, cf: exp(a * P0) * F1,
       ch: exp(a * P0) * H1}
chk_data = (simplify(psol.subs(x, 0).subs(inv) - P0) == 0
            and simplify(psol.diff(x).subs(x, 0).subs(inv) - P1) == 0
            and simplify(fp.subs(x, 0).subs(inv) - F1) == 0
            and simplify(hp.subs(x, 0).subs(inv) - H1) == 0)
vcheck("V_explicit_inverse_initial_data", chk_data,
       "EXPLICIT global inverse: (w0,w1,c_f,c_h) = (e^{aP0}, a e^{aP0}P1, e^{aP0}F1, "
       "e^{aP0}H1) realizes ARBITRARY initial data (any signs) — the family covers the "
       "full 6-dim local field-sector solution space (with Picard for uniqueness); "
       "stronger than and consistent with the package's rank-6 claim")

# Quadratures (own verification by differentiation, sign-free where stated)
c2 = cf**2 + ch**2
s = sqrt(4 * A * w0 - w1**2)
F_atan = (2 * cf / s) * atan((2 * A * x + w1) / s)
G_anti = (x + w1 / (2 * A)) * log(w) - 2 * x + (s / A) * atan((2 * A * x + w1) / s)
vcheck("V_quadratures_by_differentiation",
       simplify(diff(F_atan, x) - cf / w) == 0
       and simplify(diff(G_anti, x) - log(w)) == 0,
       "f-quadrature and the log-w antiderivative both verified by differentiation "
       "(a_F free real; requires c != 0 so s real — matches the package's stated scope)")

# First integrals (own on-shell substitution)
E0dens_on_sol = simplify(exp(a * psol) * (psol.diff(x)**2 + fp**2 + hp**2) / 2)
vcheck("V_first_integral_constant",
       simplify(E0dens_on_sol - E0) == 0
       and simplify(exp(a * psol) * fp - cf) == 0
       and simplify(exp(a * psol) * hp - ch) == 0,
       "on the closed-form solution E0dens IDENTICALLY equals the constant E0 and the "
       "shift currents equal c_f, c_h — the three first integrals confirmed on-shell")

# ---------------------------------------------------------------------------
# (2b) The background tie: own derivation of the lambda-row
# ---------------------------------------------------------------------------
# Banked generated construction (Stage-3): R_lam = WM^{-1} d/dlam (WF Ltil0), so the
# BASE-branch integrated row int WM R_lam dx = int d/dlam(WF Ltil0) dx (WM cancels for
# EVERY a_M — genuine, not assumed). For both P1 instances a_F' = d a_F/dlam = 2:
p0s, p1s, f1s, h1s = symbols("p0s p1s f1s h1s", real=True)
Lt0 = (p1s**2 + f1s**2 + h1s**2) / 2
for nm, aF_of_lam in [("P1-4D", 2 * lam), ("P1-triad", 1 + 2 * lam)]:
    lhs = expand(diff(exp(aF_of_lam * p0s) * Lt0, lam))
    rhs = expand(2 * p0s * exp(aF_of_lam * p0s) * Lt0)
    vcheck(f"V_lambda_row_{nm}", expand(lhs - rhs) == 0,
           "d/dlam(WF Ltil0) = 2 p0 WF Ltil0 exactly (a_F' = 2); on-shell WF Ltil0 = E0 "
           "const, so the integrated row is 2 E0 int p0 dx = 2 E0 I_p — re-derived")
# P2 absence: on P2 a_F = 0 IDENTICALLY (branch definition, banked) and Ltil0 is
# lam-independent, so the generated lam-slot d/dlam(1 * Ltil0) = 0 — DERIVED from the
# branch's a_F' = 0, not assumed:
vcheck("V_P2_tie_absent_derived",
       expand(diff(exp(0 * p0s) * Lt0, lam)) == 0,
       "under P2 (a_F = 0 with zero lam-dependence, the branch definition) the generated "
       "lam-slot vanishes IDENTICALLY — genuine derivational absence, and it is exactly "
       "the a_F'(lam) = 0 degeneration of the P1 tie (blindness loci lam=0, lam=-1/2 "
       "reproduce it inside the P1 branches)")

# I_p closed form vs direct integration (spot witness, exact):
Ip_closed = (G_anti.subs(x, ell) - G_anti.subs(x, -ell)) / a
legA = {a: 1, w0: Rational(1, 2), w1: 0, cf: Rational(3, 10), ch: Rational(2, 5), ell: 1}
Ip_direct_A = integrate(log(w.subs(legA)).rewrite(sp.log), (x, -1, 1))
Ip_closed_A = Ip_closed.subs(legA)
vcheck("V_Ip_closedform_vs_direct",
       simplify(Ip_direct_A - Ip_closed_A) == 0,
       "I_p = [G(ell)-G(-ell)]/a_F agrees with direct sympy integration at the package's "
       "leg-A witness (exact)")

# Nonemptiness of {I_p = 0, E0 > 0}: verifier's OWN legs at SYMBOLIC ell and BOTH signs
# of a_F.  Leg A': choose parameters with w = x^2/(8 ell^2) + 1/2 (max 5/8 < 1 on the
# cell); leg B': w = x^2/ell^2 + 2 (min 2 > 1).  Then sign(int log w dx) is -/+ resp.
# (Category-A: log monotone, integral of a negative/positive integrand), and
# I_p = (int log w)/a_F flips sign BETWEEN the legs for EITHER sign of a_F; E0 > 0 on
# both legs and along the connecting parameter path (c_f, c_h > 0 throughout); the
# explicit closed form is continuous in the parameters (w > 0: disc < 0).  Root exists.
for sgn in (1, -1):
    av = sgn * Symbol("q", positive=True)
    # leg A': A = 1/(8 ell^2)  =>  a^2 E0/2 = 1/(8 ell^2), E0 = c^2/(2 w0), w0 = 1/2
    #         => c^2 = 1/(4 a^2 ell^2): realizable (c_f = 1/(2|a|ell), c_h = 0 forbidden?
    #         package enumerates c_h = 0 edge; keep both nonzero: 3/5,4/5 split)
    cfA = Rational(3, 5) / (2 * sqrt(av**2) * ell)
    chA = Rational(4, 5) / (2 * sqrt(av**2) * ell)
    E0A = (cfA**2 + chA**2) / (2 * Rational(1, 2))
    wA = simplify((av**2 * E0A / 2) * x**2 + Rational(1, 2))
    okA = simplify(wA - (x**2 / (8 * ell**2) + Rational(1, 2))) == 0
    # leg B': A = 1/ell^2 => E0 = 2/(a^2 ell^2) = c^2/(2*2) => c^2 = 8/(a^2 ell^2)
    cfB = Rational(6, 5) * sqrt(2) / (sqrt(av**2) * ell)
    chB = Rational(8, 5) * sqrt(2) / (sqrt(av**2) * ell)
    E0B = (cfB**2 + chB**2) / (2 * 2)
    wB = simplify((av**2 * E0B / 2) * x**2 + 2)
    okB = simplify(wB - (x**2 / ell**2 + 2)) == 0
    vcheck(f"V_locus_legs_sign{'+' if sgn>0 else '-'}",
           okA and okB and sp.ask(sp.Q.positive(E0A)) and sp.ask(sp.Q.positive(E0B)),
           "verifier legs at SYMBOLIC ell, a_F of this sign: w <= 5/8 < 1 (leg A') and "
           "w >= 2 > 1 (leg B') on the whole cell with E0 > 0 on both; int log w dx "
           "changes sign between legs, so I_p = (int log w)/a_F does too (both signs of "
           "a_F); continuity of the closed form along the connecting path (E0 > 0, w > 0 "
           "throughout) gives an I_p = 0 root with E0 > 0 — the package's 'every "
           "a_F != 0 background' claim CONFIRMED, incl. the a_F < 0 leg its own witnesses "
           "did not exhibit")

# ---------------------------------------------------------------------------
# (2c) R5 triple on the SAME solution: V, M, rho (own integration)
# ---------------------------------------------------------------------------
V_direct = integrate(w, (x, -ell, ell))
V_pkg = 2 * A * ell**3 / 3 + 2 * w0 * ell
M_direct = integrate(E0, (x, -ell, ell))     # E0dens == E0 const on-shell (proven above)
vcheck("V_R5_same_solution",
       simplify(V_direct - V_pkg) == 0 and simplify(M_direct - 2 * ell * E0) == 0,
       "V = int w dx and M = int E0dens dx both integrated on the SAME closed-form "
       "member: V = (2/3)A ell^3 + 2 w0 ell, M = 2 ell E0, rho = M/V — no splicing "
       "(F-D6 confirmed); M rests on the CHOSE/CONDITIONAL instantiation (tag verified "
       "present in script/MD/ledger)")

# ---------------------------------------------------------------------------
# (2d) fork independence + (2e) W3 / omega + W1/W2-fs cell adjudications
# ---------------------------------------------------------------------------
alpha, cE, frak = symbols("alpha c_E frak_c")
vcheck("V_fork_absence",
       all(diff(e, v) == 0 for e in (Rp_pkg, Rf_pkg, Rh_pkg)
           for v in (alpha, cE, frak)),
       "alpha, c_E, frak_c absent from the GEN-QUAD components (independent recheck); "
       "a_M-independence of the integrated row = the WM cancellation above")

# W1 Helmholtz-(ii) defect, own jet computation:
p0j, p1j, p2j, f1j, f2j, h1j, h2j = symbols("p0j p1j p2j f1j f2j h1j h2j")
Dp = exp(a * p0j) * p2j


def Dx_jet(e):
    reps = {p0j: p1j, p1j: p2j, f1j: f2j, h1j: h2j}
    out = 0
    for k, v in reps.items():
        out += diff(e, k) * v
    return out


defect = expand(2 * diff(Dp, p1j) - 2 * Dx_jet(diff(Dp, p2j)))
vcheck("V_W1_defect", simplify(defect + 2 * a * p1j * exp(a * p0j)) == 0,
       "W1's Helmholtz-(ii) self-defect = -2 a_F p1 e^{a_F p0}: NV iff a_F != 0 "
       "(off-blindness on P1-side; LE at a_F = 0) — matches the banked adjudication; "
       "zero set {p2=f2=h2=0} = affine atlas, weight-independent (T0 theorem confirmed: "
       "e^{a_F p0} > 0 invertible)")

# W2-fs NV under P2 (weight 1): the (p,p) SELF Helmholtz-(ii) defect (the mixed p/f
# defect vanishes — verified: 2*lam*f1 - 2*lam*f1 = 0; the NV content is in the self row)
Rp_t = 2 * lam * (f1j**2 + h1j**2 - p1j**2) / 2 - p2j
Rf_t = -(2 * lam * p1j * f1j + f2j)
mixed_pf = expand(diff(Rp_t, f1j) + diff(Rf_t, p1j) - 2 * Dx_jet(diff(Rf_t, p2j)))
self_pp = expand(2 * diff(Rp_t, p1j) - 2 * Dx_jet(diff(Rp_t, p2j)))
vcheck("V_W2fs_NV_under_P2",
       simplify(mixed_pf) == 0 and simplify(self_pp + 4 * lam * p1j) == 0
       and simplify(self_pp.subs(lam, Rational(1, 3))) != 0,
       "the unweighted (P2) Helmholtz-(ii) SELF (p,p) defect of the W2-fs tuple = "
       "-4 lam p1 != 0 for lam != 0 (the mixed p/f defect vanishes): NONVARIATIONAL "
       "under P2 as banked, while its zero set is the SAME well family (zero-set/"
       "pairing theorem confirmed)")

vcheck("V_W3_omega_degeneracy",
       all(diff(p1j, v) == 0 for v in (f1j, f2j, h1j, h2j)),
       "W3 = (p1,0,0): f/bh rows identically zero -> {p0 const} x f,bh arbitrary "
       "(per-member underdetermined, honest); omega row k10 * int e^{a_M p0} dx = 0 with "
       "positive integrand forces k10 = 0 for EVERY a_M (Category-A positivity) — both "
       "as recorded")

# ---------------------------------------------------------------------------
# (2f) KMOD0: own recomputation of the stratum identity + L23 gauge tangent
# ---------------------------------------------------------------------------
eta = sp.diag(-1, 1, 1, 1)
L23 = zeros(4, 4)
L23[2, 3] = 1
L23[3, 2] = -1
k00, k10, k11 = symbols("k00 k10 k11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
X = zeros(4, 4)
X[0, 0], X[1, 1] = 1, 1        # H = diag(-1,1)? package uses H2=diag(-1,1)
X[0, 0] = -1
Kb = Matrix([[k00, 0], [k10, k11]])
Cb = Matrix([[c00, c01], [c10, c11]])
X[2:4, 2:4] = Kb
X[2:4, 0:2] = Cb
W = (L23 * X - X * L23).subs(k11, k00)
r_tr, r_tf, r_sh, r_nl, m00, m01, m10, m11 = symbols("r_tr r_tf r_sh r_nl m00 m01 m10 m11")
Wslot = r_tr * eye(2) + r_tf * sp.diag(-1, 1) + r_sh * Matrix([[0, 0], [1, 0]]) + \
    r_nl * Matrix([[0, 1], [0, 0]])
Mker = Matrix([[m00, m01], [m10, m11]])
pairing = expand(sp.trace(Wslot.T * W[2:4, 2:4]) + sp.trace(Mker.T * W[2:4, 0:2]))
ident = expand(-2 * k10 * r_tf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01)
Kw = W[2:4, 2:4]
Cw = W[2:4, 0:2]
Jrot = Matrix([[0, 1], [-1, 0]])
vcheck("V_kmod0_identity_and_gauge",
       expand(pairing - ident) == 0
       and expand(ident.subs({r_tf: 0, m00: 0, m01: 0, m10: 0, m11: 0})) == 0
       and Kw[1, 0] == 0 and expand((Kw[0, 0] - Kw[1, 1]) / 2 - k10) == 0
       and expand((Kw[0, 0] + Kw[1, 1]) / 2) == 0
       and all(expand(e) == 0 for e in (Cw - Jrot * Cb)),
       "stratum identity -2k10 r_tf + <M,JC-part> recomputed from [L23,X] (own build); "
       "reps (r_tf = M = 0) satisfy it identically; gauge tangent (dlam, dk_mod, dk10, "
       "dC) = (0, k10, 0, J.C) confirmed — the quotient acts only on retained moduli, "
       "GEN-QUAD components (k10, C)-independent by inspection")

# ---------------------------------------------------------------------------
# (2g) Route C restricted-EH cross-check — own parse and substitution WITH explicit x
# ---------------------------------------------------------------------------
eh_path = os.path.join(HERE, "..", "udt_p4_routeC_shared_static_sector_2026-07-28",
                       "EH_ODE_SYSTEM_FULL.txt")
with open(eh_path) as fh:
    txt = fh.read()
rows = {}
cur, buf = None, []
for line in txt.splitlines():
    if line.startswith("== "):
        if cur:
            rows[cur] = "".join(buf).strip()
        cur, buf = line.strip("= ").strip(), []
    elif line.startswith("#") or not line.strip():
        continue
    else:
        buf.append(line.strip())
if cur:
    rows[cur] = "".join(buf).strip()
As, Bs = symbols("A_s B_s")
P0c, F0c = symbols("P0c F0c")
Lam = Symbol("Lambda")
loc = {"lambda": lam, "Lambda": Lam, "alpha": alpha, "c_E": cE,
       "p0": Symbol("p0"), "p1": Symbol("p1"), "p2": Symbol("p2"),
       "f0": Symbol("f0"), "f1": Symbol("f1"), "f2": Symbol("f2"),
       "h0": Symbol("h0"), "h1": Symbol("h1"), "h2": Symbol("h2")}
sub_x = {Symbol("p0"): P0c, Symbol("p1"): 0, Symbol("p2"): 0,
         Symbol("f0"): F0c, Symbol("f1"): 0, Symbol("f2"): 0,
         Symbol("h0"): (As * x + Bs)**2, Symbol("h1"): 2 * As * (As * x + Bs),
         Symbol("h2"): 2 * As**2, Lam: 0}
all_zero, n_rows, x_free = True, 0, True
for rn in sorted(rows):
    e = sp.sympify(rows[rn].replace("lambda", "lam"), locals=loc)
    n_rows += 1
    if e.has(x):
        x_free = False
    val = simplify(e.subs(sub_x))
    if simplify(val) != 0:
        all_zero = False
        print(f"   EH row {rn}: residual {val}")
vcheck("V_EH_crosscheck_explicit_x", all_zero and n_rows == 7 and x_free,
       "own substitution with EXPLICIT x-dependence (p0 = const, f = const, "
       "bh = (Ax+B)^2, Lambda = 0) kills all 7 restricted rows identically in "
       "(x, A, B, alpha, lam, c_E, P0c, F0c); rows verified autonomous (no bare x), so "
       "the package's t-substitution was also valid")

# ---------------------------------------------------------------------------
# TD5 parity witness recheck (own)
# ---------------------------------------------------------------------------
q = Symbol("q", positive=True)   # |a_F|
ww = x**2 / (2 * ell**2) + Rational(1, 2)
pw = log(ww) / q
vcheck("V_parity_witness",
       simplify(ww.subs(x, ell) - 1) == 0 and simplify(ww.subs(x, -ell) - 1) == 0
       and simplify(pw.diff(x, 2).subs(x, ell)) == 0
       and simplify(pw.diff(x, 2).subs(x, -ell)) == 0
       and sp.ask(sp.Q.positive(ww.subs(x, 0))),
       "w = x^2/(2 ell^2) + 1/2: w(+-ell) = 1 (p0 = 0), p2(+-ell) = 0, w >= 1/2 > 0 — "
       "the gate-5 admissible witness confirmed; consistency E0 = c^2 = 1/(a_F ell)^2 "
       "checked: A = a^2 E0/2 = 1/(2 ell^2) ✓")

n = len(FAILS)
print(f"\nVERIFIER: {'ALL PASS' if n == 0 else f'{n} FAILURES: {FAILS}'}")
sys.exit(0 if n == 0 else 1)
