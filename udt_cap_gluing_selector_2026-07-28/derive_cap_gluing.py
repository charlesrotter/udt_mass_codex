#!/usr/bin/env python3
"""
Cap gluing of the plane-selector certificate — gate (c).

Contract: udt_cap_gluing_selector_2026-07-28/PREREGISTRATION.md (T-c1..T-c4,
falsifiers F-c1..F-c3, maximum conclusion).

Parents (only imports permitted):
  P-OWN = udt_higher_isometry_plane_ownership_audit_2026-07-28/EXACT_DERIVATION.md
          (family §1, Gram G3 §2, witness §6, two-free-lines/cap-lattice §7,
           FREE_CIRCLE_CLASSES.tsv)
  P-SEL = udt_alpha_plane_selector_theorem_2026-07-28/EXACT_DERIVATION.md
          (certificate quantities det G_KY = -c_E^2(b u + f^2),
           off-term (D_KY)[1,0] = -alpha c_E df u^2/(b u + f^2),
           tr D_KY = X(b u + f^2)/(b u + f^2); conventions §0)

Fully symbolic (sympy) + exact rational numeric profile families. Deterministic:
no RNG, no environment input. Every check is a zero-residual sympy test
(simplify/cancel == 0, or an exact limit equality). Any failure is recorded
verbatim; exit code 0 iff every check passes.

STRUCTURE
  A. T-c1 lattice algebra: which primitive circle can close; f_cap = -x/y;
     V-closing impossible; registered cap cycles = (V±Y)/2; g(w,w) identity
     from the parent Gram G3; H = w/y at the cap moment value.
  B. T-c1/T-c2 cap series model (load-bearing): even-jet regularity model
     u = u0+u2 rho^2+..., f = f_cap+f2 rho^2+..., b = b2 rho^2+... with
     rho = transverse geodesic distance; unit closing rate fixes b2 = 1/y^2;
     forced limits chi -> 0, df -> 0 at rate O(sqrt(b)); certificate limits.
     Negative control: an odd term in f breaks smoothness of the rotation-
     invariant extension (machine form of "evenness is forced").
  C. T-c3: exceptional-stratum feedback — S = b u + f^2 -> f_cap^2 at a
     regular cap; S == c constant  =>  c = f_cap^2 = 1 (registered), both caps,
     both possible closing cap cycles; stratum rate lock f2 = -b2 u0/(2 f_cap).
  D. Witness control (P-OWN §6, symbolic eps and alpha): all limits confirmed.
  E. Non-witness numeric cap-regular families:
     NW1 generic (alpha = 7/10, off-stratum), NW2 exceptional-stratum complete
     member (c = 1 instance), NW3 failure controls (c = 6/5 and c = 4/5 cannot
     close the caps).
  F. T-c4 records: full-response trace tr D3 = db/b diverges at caps; all
     certificate legs continuous.

Series truncation note: every limit computed below depends only on the finite
jet orders displayed (2-jet or 4-jet); truncation at O(rho^4) is exact for
those limits, not an approximation of a stated result.
"""

import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))

RESULT = {
    "package": "udt_cap_gluing_selector_2026-07-28",
    "script": "derive_cap_gluing.py",
    "date": "2026-07-28",
    "deterministic": True,
    "sympy_version": sp.__version__,
    "checks": [],
    "verdicts": {},
}


def check(name, cond, detail=""):
    ok = bool(cond)
    RESULT["checks"].append({"name": name, "pass": ok, "detail": str(detail)})
    print("[{}] {}{}".format("PASS" if ok else "FAIL", name,
                             "  :: " + str(detail) if detail != "" else ""))
    return ok


def lim0(expr, var):
    return sp.limit(sp.cancel(sp.together(expr)), var, 0, '+')


print("=" * 78)
print("Cap gluing of the plane-selector certificate — gate (c)")
print("sympy", sp.__version__)
print("=" * 78)

# ---------------------------------------------------------------------------
# Shared symbols
# ---------------------------------------------------------------------------
u, b = sp.symbols('u b', positive=True)
f, alpha = sp.symbols('f alpha', real=True)
c_E = sp.Symbol('c_E', real=True, nonzero=True)
x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True, nonzero=True)
Q = 1 / u - alpha ** 2 * u

# ===========================================================================
# A. T-c1 — lattice algebra of the closing circle
# ===========================================================================
print("\n--- A. T-c1 lattice algebra ---")

# A.1 Parent Gram G3 (P-OWN §2) and the closing-circle norm identity.
G3 = sp.Matrix([
    [-c_E ** 2 * u, -c_E * alpha * u, -c_E * alpha * u * f],
    [-c_E * alpha * u, Q, Q * f],
    [-c_E * alpha * u * f, Q * f, Q * f ** 2 + b],
])
check("A_G3_det_parent", sp.simplify(G3.det() + b * c_E ** 2) == 0,
      "det G3 = -b c_E^2 (P-OWN §2) reproduced")

wvec = sp.Matrix([0, x, y])           # w = x V + y Y (spatial circle)
gww = sp.expand((wvec.T * G3 * wvec)[0, 0])
gww_closed = Q * (x + y * f) ** 2 + y ** 2 * b
check("Tc1_gww_formula", sp.simplify(gww - gww_closed) == 0,
      "g(w,w) = Q (x+y f)^2 + y^2 b for w = x V + y Y")

# Cross terms of the closing circle with K and with the surviving cycle
# w' = xp V + yp Y: both are controlled by (x + y f) and b.
xp, yp = sp.symbols('xp yp', real=True)
wpvec = sp.Matrix([0, xp, yp])
gwK = sp.expand((sp.Matrix([1, 0, 0]).T * G3 * wvec)[0, 0])
check("Tc1_cross_K_formula", sp.simplify(gwK + c_E * alpha * u * (x + y * f)) == 0,
      "g(w,K) = -c_E alpha u (x + y f)  ->  0 exactly when A(w) = x + y f -> 0")
gwwp = sp.expand((wpvec.T * G3 * wvec)[0, 0])
check("Tc1_cross_orbit_formula",
      sp.simplify(gwwp - (Q * (x + y * f) * (xp + yp * f) + y * yp * b)) == 0,
      "g(w,w') = Q (x+y f)(x'+y' f) + y y' b  ->  0 when A(w) -> 0 and b -> 0")

# A.2 The moment of the closing circle vanishes at the cap core:
# the closing generator w vanishes on the core (fixed-point set of its flow —
# a Killing field vanishes at fixed points of its flow, trivially), and A is a
# smooth registered one-form, so A(w) = x + y f -> A(0) = 0.  Hence:
fcap_sol = sp.solve(sp.Eq(x + y * f, 0), f)
check("Tc1_fcap_formula", len(fcap_sol) == 1 and sp.simplify(fcap_sol[0] + x / y) == 0,
      "A(w) -> 0 with y != 0  =>  f -> f_cap = -x/y at the cap")

# A.3 V can never be the closing circle: w = ±V means (x,y) = (±1,0)
# (primitivity of V), and then A(w) = ±1 is a nonzero CONSTANT — it cannot
# tend to 0.  Derived from A(V)=1 (registered) + smoothness of A alone.
ok_V = all(sp.simplify((sx * 1 + 0 * f) - sx) == 0 and sx != 0 for sx in (1, -1))
check("Tc1_V_never_closes", ok_V,
      "w = ±V gives A(w) = ±1, constant and nonzero: V-closing is impossible")

# A.4 Registered completion (P-OWN §7): cap cycles (v-, v+) unimodular,
# {V, Y} = the two free lines v- ± v+ (up to overall signs).  Solve for the
# cap-cycle coordinates in the (V, Y) basis for every sign labeling.
fcap_values = set()
all_half = True
opposite_at_two_caps = True
for s1 in (1, -1):
    for s2 in (1, -1):
        # V = s1 (v- + v+),  Y = s2 (v- - v+)  in the standard lattice basis
        V_ = sp.Matrix([s1, s1])
        Y_ = sp.Matrix([s2, -s2])
        M = sp.Matrix.hstack(V_, Y_)           # columns: V, Y
        caps = []
        for wlat in (sp.Matrix([1, 0]), sp.Matrix([0, 1])):   # v-, v+
            xy = M.solve(wlat)                 # w = x V + y Y
            xx, yy = xy[0], xy[1]
            all_half &= (abs(xx) == sp.Rational(1, 2) and abs(yy) == sp.Rational(1, 2))
            fc = -xx / yy
            caps.append(fc)
            fcap_values.add(fc)
        opposite_at_two_caps &= (caps[0] == -caps[1])
check("Tc1_cap_cycle_coords", all_half,
      "every cap cycle has |x| = |y| = 1/2 in the free-line basis (V, Y)")
check("Tc1_fcap_registered", fcap_values == {sp.Integer(1), sp.Integer(-1)},
      "registered completions: f_cap = ±1 exactly")
check("Tc1_fcap_opposite", opposite_at_two_caps,
      "the two caps carry OPPOSITE f_cap values (+1 at one, -1 at the other)")

# A.5 Hypothetical (non-registered) closing of the second line Y itself:
# (x,y) = (0, ±1) gives f_cap = 0.  Excluded in the registered completion
# because Y is a FREE line (P-OWN §7); recorded for scope honesty.
fc_Y = -sp.Integer(0) / 1
check("Tc1_Y_closing_record", fc_Y == 0,
      "IF the second circle itself closed (non-registered), f_cap would be 0")

# A.6 H = Y - f V becomes w/y exactly at the cap moment value f = -x/y:
Hcoef = sp.Matrix([0, -f, 1])                       # H = Y - f V in (K,V,Y)
diffH = sp.simplify((Hcoef - wvec / y).subs(f, -x / y))
check("Tc1_H_is_w_over_y", diffH == sp.zeros(3, 1),
      "at f = f_cap: H = w/y, hence b = g(H,H) = g(w,w)/y^2 -> 0 at the cap")

# ===========================================================================
# B. T-c1/T-c2 — cap series model (load-bearing regularity jets)
# ===========================================================================
print("\n--- B. cap series model ---")

rho = sp.Symbol('rho', positive=True)
u0 = sp.Symbol('u0', positive=True)
u2, u4, f2, f4, b4 = sp.symbols('u2 u4 f2 f4 b4', real=True)
b2 = sp.Symbol('b2', positive=True)

fcap = -x / y
f_s = fcap + f2 * rho ** 2 + f4 * rho ** 4
u_s = u0 + u2 * rho ** 2 + u4 * rho ** 4
b_s = b2 * rho ** 2 + b4 * rho ** 4
Q_s = 1 / u_s - alpha ** 2 * u_s

# B.1 closing-circle norm and the unit-rate (no-cone) condition
gww_s = Q_s * (x + y * f_s) ** 2 + y ** 2 * b_s
check("Tc1_gww_leading", sp.simplify(lim0(gww_s / rho ** 2, rho) - y ** 2 * b2) == 0,
      "g(w,w) = y^2 b2 rho^2 + O(rho^4): the Q-term enters only at O(rho^4)")
b2_forced = sp.solve(sp.Eq(y ** 2 * b2, 1), b2)[0]
check("Tc1_b_rate", sp.simplify(b2_forced - 1 / y ** 2) == 0,
      "unit closing rate (2pi period, no cone) forces b2 = 1/y^2 "
      "(registered |y| = 1/2  =>  b = 4 rho^2 (1+O(rho^2)))")
check("Tc1_b_gww_ratio",
      sp.simplify(lim0(y ** 2 * b_s / gww_s, rho) - 1) == 0,
      "y^2 b / g(w,w) -> 1: b -> 0 exactly as fast as the closing norm")

# B.2 forced limits of chi, df, db at a regular cap (evenness of u, f, b)
chi_s = -sp.diff(u_s, rho) / (2 * u_s)
df_s = sp.diff(f_s, rho)
db_s = sp.diff(b_s, rho)
check("Tc1_chi_zero", lim0(chi_s, rho) == 0, "chi -> 0 at every regular cap (u even)")
check("Tc1_chi_rate", sp.simplify(lim0(chi_s / rho, rho) + u2 / u0) == 0,
      "chi = -(u2/u0) rho + O(rho^3)")
check("Tc2_df_zero", lim0(df_s, rho) == 0, "df -> 0 at every regular cap (f even)")
check("Tc1_db_zero", lim0(db_s, rho) == 0, "db -> 0 at every regular cap (b even)")
check("Tc1_df_rate_general",
      sp.simplify(lim0(df_s ** 2 / b_s, rho) - 4 * f2 ** 2 / b2) == 0,
      "df^2/b -> 4 f2^2/b2: df -> 0 at rate O(sqrt(b))")
check("Tc1_df_rate_unit",
      sp.simplify(lim0((df_s ** 2 / b_s).subs(b2, 1 / y ** 2), rho)
                  - 4 * f2 ** 2 * y ** 2) == 0,
      "with the unit rate: df^2/b -> 4 f2^2 y^2 (= f2^2 registered)")

# B.3 negative control: an odd jet in an invariant scalar breaks smoothness.
# A torus-invariant function near the cap core is a rotation-invariant
# function on the transverse disc; if F(x1,x2) = f_c + f1 r with r = |(x1,x2)|
# and f1 != 0, dF/dx1 jumps by 2 f1 across the core: not C^1.
x1, x2, f1, fc0 = sp.symbols('x1 x2 f1 fc0', real=True)
F_odd = fc0 + f1 * sp.sqrt(x1 ** 2 + x2 ** 2)
dF = sp.diff(F_odd, x1).subs(x2, 0)
jump = sp.limit(dF, x1, 0, '+') - sp.limit(dF, x1, 0, '-')
check("Tc2_evenness_negative_control", sp.simplify(jump - 2 * f1) == 0,
      "odd r-term => dF/dx1 jumps by 2 f1 at the core: smooth iff f1 = 0 "
      "(machine form of: invariant scalars are even in rho; df(0)=0 FORCED)")

# B.4 certificate quantities at the cap (P-SEL formulas, INDEPENDENTLY
# recomputed here from the Gram matrix before taking limits — F-c3 guard)
S_s = b_s * u_s + f_s ** 2
G_KY = sp.Matrix([[-c_E ** 2 * u_s, -alpha * c_E * u_s * f_s],
                  [-alpha * c_E * u_s * f_s, Q_s * f_s ** 2 + b_s]])
detG = sp.simplify(G_KY.det())
check("Tc2_det_recompute", sp.simplify(detG + c_E ** 2 * S_s) == 0,
      "det G_KY = -c_E^2 (b u + f^2) recomputed from the Gram matrix")
Gp = sp.diff(G_KY, rho)
Ginv = sp.Matrix([[G_KY[1, 1], -G_KY[0, 1]], [-G_KY[1, 0], G_KY[0, 0]]]) / detG
D_KY = Ginv * Gp
off_formula = -alpha * c_E * df_s * u_s ** 2 / S_s
check("Tc2_off_recompute", sp.simplify(sp.cancel(D_KY[1, 0] - off_formula)) == 0,
      "(D_KY)[1,0] = -alpha c_E df u^2/(b u + f^2) recomputed independently")
tr_formula = sp.diff(S_s, rho) / S_s
check("Tc2_trace_recompute", sp.simplify(sp.cancel(D_KY[0, 0] + D_KY[1, 1] - tr_formula)) == 0,
      "tr D_KY = X(b u + f^2)/(b u + f^2) recomputed independently")

# limits (general x, y first, then registered |x| = |y| = 1/2)
check("Tc2_detGKY_limit_general",
      sp.simplify(lim0(detG, rho) + c_E ** 2 * x ** 2 / y ** 2) == 0,
      "det G_KY -> -c_E^2 f_cap^2 = -c_E^2 x^2/y^2 at a regular cap")
check("Tc2_detGKY_limit_registered",
      sp.simplify(lim0(detG.subs([(x, sp.Rational(1, 2)), (y, -sp.Rational(1, 2))]), rho)
                  + c_E ** 2) == 0,
      "registered f_cap^2 = 1: det G_KY -> -c_E^2 = det G_KV exactly")
check("Tc2_off_limit", lim0(off_formula, rho) == 0,
      "off-term -> 0 at every regular cap (df -> 0, S -> f_cap^2 != 0)")
check("Tc2_off_rate",
      sp.simplify(lim0(off_formula / rho, rho)
                  + alpha * c_E * 2 * f2 * u0 ** 2 * y ** 2 / x ** 2) == 0,
      "off-term = -2 alpha c_E f2 u0^2 (y^2/x^2) rho + O(rho^3): O(rho) = O(sqrt(b))")
check("Tc2_trace_limit", lim0(tr_formula, rho) == 0,
      "tr D_KY -> 0 at every regular cap")
D_lim = sp.Matrix(2, 2, lambda i, j: lim0(D_KY[i, j], rho))
check("Tc2_DKY_limit", D_lim == sp.zeros(2, 2),
      "the whole restricted response D_KY -> 0 entrywise")
D_KV = sp.Matrix([[-2 * chi_s, -4 * alpha * chi_s / c_E], [0, 2 * chi_s]])
D_KV_lim = sp.Matrix(2, 2, lambda i, j: lim0(D_KV[i, j], rho))
check("Tc2_DKV_limit", D_KV_lim == sp.zeros(2, 2),
      "D_KV -> 0 as well (chi -> 0 forced): rate pair (-2chi, +2chi) -> (0, 0)")

# ===========================================================================
# C. T-c3 — exceptional-stratum feedback
# ===========================================================================
print("\n--- C. T-c3 exceptional stratum ---")

check("Tc3_S_limit_general", sp.simplify(lim0(S_s, rho) - x ** 2 / y ** 2) == 0,
      "S = b u + f^2 -> f_cap^2 = x^2/y^2 at a regular cap")

# S == c on the principal region + continuity up to the cap => c = f_cap^2.
# Series form: impose b = (c - f^2)/u (the stratum's b) and demand closing
# (b -> 0 at the cap):
c = sp.Symbol('c', real=True)
b_stratum_cap = (c - fcap ** 2) / u0            # limit of (c - f^2)/u at the cap
c_forced = sp.solve(sp.Eq(b_stratum_cap, 0), c)
check("Tc3_c_forced_series", len(c_forced) == 1 and
      sp.simplify(c_forced[0] - x ** 2 / y ** 2) == 0,
      "S == c with a regular cap forces c = f_cap^2 exactly")

# Registered completion: both caps, both possible closing cap cycles.
all_c1 = True
for (xx, yy) in [(sp.Rational(1, 2), sp.Rational(1, 2)),
                 (sp.Rational(1, 2), -sp.Rational(1, 2)),
                 (-sp.Rational(1, 2), sp.Rational(1, 2)),
                 (-sp.Rational(1, 2), -sp.Rational(1, 2))]:
    all_c1 &= (sp.simplify(xx ** 2 / yy ** 2) == 1)
check("Tc3_both_caps_both_lines", all_c1,
      "all four registered (x, y) sign cases give c = 1; the two caps agree")

# Hypothetical non-registered Y-closing record: c would be 0 (and span(K,Y)
# would degenerate at that cap) — outside the free-line candidate set.
check("Tc3_general_record", sp.simplify((sp.Integer(0)) ** 2 / 1 ** 2) == 0,
      "record: a completion closing the second circle itself would force c = 0")

# Stratum rate lock: on S == c, the O(rho^2) coefficient must also vanish:
S_coeff2 = sp.expand(S_s).coeff(rho, 2)
f2_lock = sp.solve(sp.Eq(S_coeff2, 0), f2)[0]
check("Tc3_stratum_rate_lock",
      sp.simplify(f2_lock + b2 * u0 / (2 * fcap)) == 0,
      "S == c forces f2 = -b2 u0/(2 f_cap) (with b2 = 1/y^2: f2 = -u0/(2 y^2 f_cap))")
check("Tc3_rate_lock_witness_value",
      sp.simplify(f2_lock.subs([(b2, 4), (u0, 1), (x, sp.Rational(1, 2)),
                                (y, -sp.Rational(1, 2))]) + 2) == 0,
      "witness numbers (u0=1, b2=4, f_cap=+1): f2 = -2, matching f = cos 2 eta")

# ===========================================================================
# D. Witness control (P-OWN §6; eps and alpha symbolic)
# ===========================================================================
print("\n--- D. witness control ---")

eta = sp.Symbol('eta', positive=True)
delta = sp.Symbol('delta', positive=True)
eps = sp.Symbol('eps', positive=True)

f_w = sp.cos(2 * eta)
u_w = 1 + eps * (1 - f_w ** 2)
b_w = (1 - f_w ** 2) / u_w
S_w = sp.simplify(b_w * u_w + f_w ** 2)
check("W_on_stratum", sp.simplify(S_w - 1) == 0,
      "witness: b u + f^2 = 1 exactly (P-SEL [W_on_stratum] reproduced)")

check("W_fcap_eta0", sp.limit(f_w, eta, 0, '+') == 1, "f -> +1 at eta = 0")
check("W_fcap_etapi2", sp.limit(f_w.subs(eta, sp.pi / 2 - delta), delta, 0, '+') == -1,
      "f -> -1 at eta = pi/2")

# closing circles: eta=0 closes w = (V-Y)/2 = d_xi2; eta=pi/2 closes (V+Y)/2.
# transverse metric coefficient v = 1/u (P-OWN §6: full spatial = u^-1 round),
# so rho^2 ~ v(cap) eta^2 and the unit-rate condition reads gww/eta^2 -> v(cap).
Q_w = 1 / u_w - alpha ** 2 * u_w
gww_0 = Q_w * ((1 - f_w) / 2) ** 2 + sp.Rational(1, 4) * b_w
check("W_unit_rate_eta0",
      sp.simplify(sp.limit(sp.cancel(gww_0 / eta ** 2), eta, 0, '+')
                  - (1 / u_w).subs(eta, 0)) == 0,
      "g(w,w)/eta^2 -> v(0) = 1: unit closing rate at eta = 0 (any eps, any alpha)")
gww_p = (Q_w * ((1 + f_w) / 2) ** 2 + sp.Rational(1, 4) * b_w).subs(eta, sp.pi / 2 - delta)
check("W_unit_rate_etapi2",
      sp.simplify(sp.limit(sp.cancel(gww_p / delta ** 2), delta, 0, '+') - 1) == 0,
      "g(w,w)/delta^2 -> v(pi/2) = 1: unit closing rate at eta = pi/2")

df_w = sp.diff(f_w, eta)
chi_w = -sp.diff(u_w, eta) / (2 * u_w)
S_wfull = b_w * u_w + f_w ** 2
off_w = -alpha * c_E * df_w * u_w ** 2 / S_wfull
tr_w = sp.diff(S_wfull, eta) / S_wfull
for nm, expr, val in [
    ("W_chi_eta0", chi_w, 0),
    ("W_df_eta0", df_w, 0),
    ("W_off_eta0", off_w, 0),
    ("W_trace_eta0", tr_w, 0),
]:
    check(nm, sp.simplify(sp.limit(sp.cancel(expr), eta, 0, '+') - val) == 0,
          "-> {} at eta = 0".format(val))
for nm, expr, val in [
    ("W_chi_etapi2", chi_w, 0),
    ("W_df_etapi2", df_w, 0),
    ("W_off_etapi2", off_w, 0),
]:
    check(nm, sp.simplify(sp.limit(sp.cancel(expr.subs(eta, sp.pi / 2 - delta)),
                                   delta, 0, '+') - val) == 0,
          "-> {} at eta = pi/2".format(val))
check("W_det_const", sp.simplify(-c_E ** 2 * S_wfull + c_E ** 2) == 0,
      "det G_KY = -c_E^2 identically on the witness (= its own cap limit)")
check("W_df_rate", sp.simplify(sp.limit(sp.cancel(df_w ** 2 / b_w), eta, 0, '+') - 4) == 0,
      "df^2/b -> 4 = 4 f2^2 y^2 (f2 = -2, y = -1/2, u0 = 1): series model matched")

# ===========================================================================
# E. Non-witness numeric cap-regular profile families
# ===========================================================================
print("\n--- E. non-witness families ---")

# NW1: generic off-stratum member, alpha = 7/10.
#   u = 1 + (3/10) sin^2 2eta + (1/5) sin^2 eta   (u0 = 1 at eta=0, 6/5 at pi/2)
#   f = cos 2eta (1 + (1/20) sin^2 2eta)          (f_cap = ±1 kept)
#   b = sin^2 2eta (1 + (3/20) sin^2 2eta)        (b ~ 4 eta^2, ~ 4 delta^2)
#   v = 1 + (1/10) sin^2 2eta                     (v = 1 at both caps: unit rate)
a1, a2v, sconst, tconst, v1 = [sp.Rational(p, q) for p, q in
                               [(3, 10), (1, 5), (1, 20), (3, 20), (1, 10)]]
alpha_n = sp.Rational(7, 10)
u_n = 1 + a1 * sp.sin(2 * eta) ** 2 + a2v * sp.sin(eta) ** 2
f_n = sp.cos(2 * eta) * (1 + sconst * sp.sin(2 * eta) ** 2)
b_n = sp.sin(2 * eta) ** 2 * (1 + tconst * sp.sin(2 * eta) ** 2)
v_n = 1 + v1 * sp.sin(2 * eta) ** 2
S_n = b_n * u_n + f_n ** 2
Q_n = 1 / u_n - alpha_n ** 2 * u_n

check("NW1_not_witness", sp.simplify(S_n - 1) != 0,
      "NW1 is OFF the exceptional stratum (b u + f^2 not constant) and non-witness")
check("NW1_fcap", sp.limit(f_n, eta, 0, '+') == 1 and
      sp.limit(f_n.subs(eta, sp.pi / 2 - delta), delta, 0, '+') == -1,
      "f -> +1 (eta=0), -1 (eta=pi/2)")
gwwn_0 = Q_n * ((1 - f_n) / 2) ** 2 + sp.Rational(1, 4) * b_n
check("NW1_unit_rate_eta0",
      sp.simplify(sp.limit(sp.cancel(gwwn_0 / eta ** 2), eta, 0, '+') - v_n.subs(eta, 0)) == 0,
      "g(w,w)/eta^2 -> v(0) = 1: cap-regular at eta = 0")
gwwn_p = (Q_n * ((1 + f_n) / 2) ** 2 + sp.Rational(1, 4) * b_n).subs(eta, sp.pi / 2 - delta)
check("NW1_unit_rate_etapi2",
      sp.simplify(sp.limit(sp.cancel(gwwn_p / delta ** 2), delta, 0, '+') - 1) == 0,
      "g(w,w)/delta^2 -> v(pi/2) = 1: cap-regular at eta = pi/2")

df_n = sp.diff(f_n, eta)
chi_n = -sp.diff(u_n, eta) / (2 * u_n)
det_n = -c_E ** 2 * S_n
off_n = -alpha_n * c_E * df_n * u_n ** 2 / S_n
tr_n = sp.diff(S_n, eta) / S_n
check("NW1_chi_caps",
      sp.limit(sp.cancel(chi_n), eta, 0, '+') == 0 and
      sp.limit(sp.cancel(chi_n.subs(eta, sp.pi / 2 - delta)), delta, 0, '+') == 0,
      "chi -> 0 at both caps")
check("NW1_det_caps",
      sp.simplify(sp.limit(sp.cancel(det_n), eta, 0, '+') + c_E ** 2) == 0 and
      sp.simplify(sp.limit(sp.cancel(det_n.subs(eta, sp.pi / 2 - delta)), delta, 0, '+')
                  + c_E ** 2) == 0,
      "det G_KY -> -c_E^2 at both caps (S -> 1)")
check("NW1_off_caps",
      sp.limit(sp.cancel(off_n / c_E), eta, 0, '+') == 0 and
      sp.limit(sp.cancel((off_n / c_E).subs(eta, sp.pi / 2 - delta)), delta, 0, '+') == 0,
      "off-term -> 0 at both caps despite alpha != 0")
check("NW1_trace_caps",
      sp.limit(sp.cancel(tr_n), eta, 0, '+') == 0 and
      sp.limit(sp.cancel(tr_n.subs(eta, sp.pi / 2 - delta)), delta, 0, '+') == 0,
      "tr D_KY -> 0 at both caps")
r0 = sp.limit(sp.cancel(df_n ** 2 / b_n), eta, 0, '+')
rp = sp.limit(sp.cancel((df_n ** 2 / b_n).subs(eta, sp.pi / 2 - delta)), delta, 0, '+')
check("NW1_df_rate", r0 == sp.Rational(81, 25) and rp == sp.Rational(81, 25),
      "df^2/b -> 81/25 at both caps: finite nonzero, df = O(sqrt(b))")
# full restricted response entrywise at eta = 0
G_n = sp.Matrix([[-c_E ** 2 * u_n, -alpha_n * c_E * u_n * f_n],
                 [-alpha_n * c_E * u_n * f_n, Q_n * f_n ** 2 + b_n]])
detGn = sp.cancel(G_n.det())
Gninv = sp.Matrix([[G_n[1, 1], -G_n[0, 1]], [-G_n[1, 0], G_n[0, 0]]]) / detGn
D_n = Gninv * sp.diff(G_n, eta)
D_n_lim = sp.Matrix(2, 2, lambda i, j:
                    sp.limit(sp.cancel(sp.together(D_n[i, j] * c_E ** 0)), eta, 0, '+'))
check("NW1_DKY_limit_eta0", sp.simplify(D_n_lim) == sp.zeros(2, 2),
      "full D_KY -> 0 entrywise at eta = 0")

# NW2: non-witness EXCEPTIONAL-STRATUM complete member (alpha = 0, S == 1).
u_m = 1 + a1 * sp.sin(2 * eta) ** 2 + a2v * sp.sin(eta) ** 2
f_m = sp.cos(2 * eta) * (1 + sconst * sp.sin(2 * eta) ** 2)
b_m = (1 - f_m ** 2) / u_m
S_m = sp.simplify(b_m * u_m + f_m ** 2)
check("NW2_on_stratum", sp.simplify(S_m - 1) == 0,
      "NW2: b u + f^2 = 1 identically (exceptional stratum, c = 1)")
# witness form would make (u - 1)/(1 - f^2) a CONSTANT eps; here it is not:
ratio_m = sp.cancel((u_m - 1) / (1 - f_m ** 2))
r_a = sp.nsimplify(ratio_m.subs(eta, sp.pi / 4))
r_b = sp.nsimplify(ratio_m.subs(eta, sp.pi / 3))
check("NW2_not_witness", sp.simplify(r_a - r_b) != 0,
      "NW2 is not of the witness form u = 1 + eps(1 - f^2): "
      "(u-1)/(1-f^2) = {} at eta=pi/4 but {} at eta=pi/3".format(r_a, r_b))
check("NW2_b_positive_interior",
      all(b_m.subs(eta, sp.Rational(k, 10)).evalf() > 0 for k in range(1, 15)),
      "b > 0 sampled across the interior (eta = 0.1..1.4)")
# transverse coefficient v making both caps unit-rate (v0, vpi from exact series)
bcoef0 = sp.limit(sp.cancel(b_m / eta ** 2), eta, 0, '+')
bcoefp = sp.limit(sp.cancel(b_m.subs(eta, sp.pi / 2 - delta) / delta ** 2), delta, 0, '+')
v0 = bcoef0 / 4
vpi = bcoefp / 4
check("NW2_v_exists", v0 > 0 and vpi > 0,
      "smooth positive transverse coefficient exists: v0 = {}, vpi = {}".format(v0, vpi))
v_m = v0 * sp.cos(eta) ** 2 + vpi * sp.sin(eta) ** 2
gwwm_0 = (1 / u_m) * ((1 - f_m) / 2) ** 2 + sp.Rational(1, 4) * b_m
check("NW2_unit_rate_eta0",
      sp.simplify(sp.limit(sp.cancel(gwwm_0 / eta ** 2), eta, 0, '+') - v_m.subs(eta, 0)) == 0,
      "g(w,w)/eta^2 -> v(0): cap-regular at eta = 0")
gwwm_p = ((1 / u_m) * ((1 + f_m) / 2) ** 2 + sp.Rational(1, 4) * b_m).subs(eta, sp.pi / 2 - delta)
check("NW2_unit_rate_etapi2",
      sp.simplify(sp.limit(sp.cancel(gwwm_p / delta ** 2), delta, 0, '+')
                  - v_m.subs(eta, sp.pi / 2)) == 0,
      "g(w,w)/delta^2 -> v(pi/2): cap-regular at eta = pi/2")
check("NW2_corollary_instance",
      sp.limit(sp.cancel(S_m), eta, 0, '+') == 1 and sp.simplify(S_m - 1) == 0,
      "NW2 is a complete two-cap exceptional member with c = 1: corollary instance")

# NW3: failure controls — the same profiles with c != 1 cannot close the caps.
for cval, nm in [(sp.Rational(6, 5), "NW3_c_gt1_fails"),
                 (sp.Rational(4, 5), "NW3_c_lt1_fails")]:
    b_c = (cval - f_m ** 2) / u_m
    blim0 = sp.limit(sp.cancel(b_c), eta, 0, '+')
    blimp = sp.limit(sp.cancel(b_c.subs(eta, sp.pi / 2 - delta)), delta, 0, '+')
    if cval > 1:
        ok = (blim0 == cval - 1) and (blimp == sp.simplify((cval - 1) / u_m.subs(eta, sp.pi / 2)))
        det_msg = ("b -> {} != 0 at eta=0 (closing norm y^2 b -> {} != 0): the circle "
                   "does NOT close; no two-cap completion".format(blim0, blim0 / 4))
    else:
        ok = (blim0 < 0) and (blimp < 0)
        det_msg = ("b -> {} < 0 at eta=0: negative horizontal norm; inadmissible "
                   "(q_B positive)".format(blim0))
    check(nm, ok, det_msg)

# ===========================================================================
# F. T-c4 records
# ===========================================================================
print("\n--- F. T-c4 records ---")

trD3_s = db_s / b_s          # P-OWN §3: tr D3 = db/b (full three-direction response)
check("Tc4_D3_trace_diverges", lim0(rho * trD3_s, rho) == 2,
      "tr D3 = db/b = 2/rho + O(rho): DIVERGES at a regular cap "
      "(rank drop; NOT a certificate quantity)")
check("Tc4_certificate_continuous",
      all(RESULT["checks"][i]["pass"] for i in range(len(RESULT["checks"]))
          if RESULT["checks"][i]["name"].startswith(("Tc2_det", "Tc2_off", "Tc2_trace",
                                                     "Tc2_DKY", "Tc2_DKV"))),
      "every certificate leg extends continuously to the caps (limits above)")

# ===========================================================================
# Verdicts + summary
# ===========================================================================
RESULT["verdicts"] = {
    "T-c1": ("Regular-cap conditions DERIVED (given the registered toric structure): "
             "the closing circle at each cap is a primitive cap cycle w = x V + y Y with "
             "|x| = |y| = 1/2 — i.e. (V±Y)/2 — NEVER V (impossible: A(V) = 1 constant) and "
             "never Y in the registered completion (Y is a free line). At a regular cap: "
             "f -> f_cap = -x/y = ±1 (opposite signs at the two caps), b -> 0 with "
             "b = rho^2/y^2 (1 + O(rho^2)) = 4 rho^2 (...) registered, u -> u0 > 0, and "
             "u, f, b are even in the transverse geodesic distance rho, so "
             "chi -> 0, df -> 0, db -> 0, each at rate O(rho) = O(sqrt(b)); "
             "df^2/b -> 4 f2^2 y^2 finite."),
    "T-c2": ("Cap limit atlas: det G_KY -> -c_E^2 f_cap^2 = -c_E^2 (equal to det G_KV); "
             "off-term -alpha c_E df u^2/(b u + f^2) -> 0 at rate O(rho); "
             "tr D_KY -> 0; the full restricted responses D_KY and D_KV -> 0 entrywise. "
             "df -> 0 at regular caps is FORCED by smoothness (evenness of the invariant "
             "scalar f), NOT witness-specific; the odd-jet negative control breaks C^1."),
    "T-c3": ("FORCED: a complete two-cap exceptional-stratum member (alpha = 0, "
             "b u + f^2 == c) has c = f_cap^2 = 1 EXACTLY, from either cap and for either "
             "possible closing cap cycle. Corollary: on complete two-cap exceptional "
             "members |det G_KY| = c_E^2 = |det G_KV| — the two silent planes carry the "
             "SAME constant area. Second lock: S == c also forces the moment jet "
             "f2 = -b2 u0/(2 f_cap) (witness: f2 = -2, matched). General toric record: "
             "c = x^2/y^2; a (non-registered) completion closing the second circle itself "
             "would force c = 0."),
    "T-c4": ("No certificate leg is singular or discontinuous at a regular cap: all "
             "extend continuously, with the rate pair (-2 chi, +2 chi) -> (0, 0) because "
             "chi -> 0 is forced (regular caps are depth-critical points). The cap value "
             "is degenerate exactly like interior chi = 0 points already covered by the "
             "theorem's quantifier discipline. The FULL response trace tr D3 = db/b "
             "diverges like 2/rho (rank drop) — a non-certificate quantity; the "
             "principal-orbit scope stamp is RETAINED with this atlas as its boundary "
             "annotation, and TIGHTENED on the exceptional stratum for complete members "
             "(c = 1)."),
    "falsifiers": ("F-c1 does not fire (conditions derivable; the preregistration's "
                   "V-closes/Y-closes dichotomy is corrected: neither free line closes — "
                   "recorded, not papered). F-c2 does not fire for certificate "
                   "quantities (the only divergent object, tr D3 = db/b, is not a "
                   "certificate leg). F-c3 does not fire (off/trace/det formulas "
                   "recomputed independently from the Gram matrix in this run; witness "
                   "and two non-witness families agree)."),
}

n_tot = len(RESULT["checks"])
n_fail = sum(1 for cchk in RESULT["checks"] if not cchk["pass"])
RESULT["n_checks"] = n_tot
RESULT["n_failed"] = n_fail
print("\n" + "=" * 78)
print("CHECKS: {} total, {} failed".format(n_tot, n_fail))
for key, val in RESULT["verdicts"].items():
    print("\n[{}] {}".format(key, val))

with open(os.path.join(HERE, "DERIVATION_RESULT.json"), "w") as fh:
    json.dump(RESULT, fh, indent=2)
print("\nWrote DERIVATION_RESULT.json")

sys.exit(0 if n_fail == 0 else 1)
