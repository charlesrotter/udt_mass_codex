#!/usr/bin/env python3
"""R09 certificate adjudication — restricted-plane certificate C_restricted vs
full-response invariance C_full (gate (b), preregistered targets T-b1..T-b4).

Contract: udt_r09_certificate_adjudication_2026-07-28/PREREGISTRATION.md.
Parents:
  P-OWN = udt_higher_isometry_plane_ownership_audit_2026-07-28
          (G3 Sec.2, D3 + quoted entries Sec.3, Cartan Sec.3, witness Sec.6)
  P-SEL = udt_alpha_plane_selector_theorem_2026-07-28
          (certificate C_restricted, conventions, derivative rules
           X(u) = -2*chi*u, X(f) = df, X(b) = db).

Conventions (frozen, inherited from the parents): global Killing basis
(K, V, Y); a Killing vector z0*K + z1*V + z2*Y is the column (z0, z1, z2)^T;
D3 = G3^{-1} X(G3) acts on columns from the left.  Membership functional for
the plane P = span(K, W), W = m*V + n*Y, (m, n) real, (m, n) != (0, 0):
    L(v) = n*v[1] - m*v[2]      (v in the (K,V,Y) column convention);
v in P  iff  L(v) = 0.  P is D3-invariant AT A POINT iff
    I1 := L(D3 K) = 0   and   I2 := L(D3 W) = 0
there; P is D3-invariant ON A REGION iff both hold at every point (this is
exactly the parent R02 usage: for (m,n) = (1,0) the two conditions are the
Y-components of D3(K) and D3(V), gated below).

Self-contained, deterministic (seed 20260728).  All symbolic gates are
zero-residual sympy identities; numeric spot checks use exact rationals.
Exit 0 iff every check passes; the F-b2 parent-reproduction gate runs FIRST
and aborts on mismatch.
"""

import json
import os
import random
import sys

import sympy as sp

CHECKS = []


def require(name, ok):
    ok = bool(ok)
    CHECKS.append({"name": name, "ok": ok})
    if not ok:
        print("FAILED CHECK: %s" % name)
    return ok


def all_ok():
    return all(c["ok"] for c in CHECKS)


# ---------------------------------------------------------------- symbols ---
c, u, b = sp.symbols("c_E u b", positive=True, real=True)
alpha, f = sp.symbols("alpha f", real=True)
chi, df, db = sp.symbols("chi df db", real=True)
m, n = sp.symbols("m n", real=True)
lam = sp.Symbol("lambda")
z = m + n * f  # V+f-weighted coefficient of the candidate line W = m V + n Y

Q = 1 / u - alpha**2 * u
G3 = sp.Matrix(
    [
        [-c**2 * u, -c * alpha * u, -c * alpha * u * f],
        [-c * alpha * u, Q, Q * f],
        [-c * alpha * u * f, Q * f, Q * f**2 + b],
    ]
)


def X(expr):
    """Transverse derivation on the free jet: X(u)=-2 chi u, X(f)=df, X(b)=db;
    alpha, c_E, m, n are constants (X annihilates them)."""
    return (
        sp.diff(expr, u) * (-2 * chi * u)
        + sp.diff(expr, f) * df
        + sp.diff(expr, b) * db
    )


D3 = sp.simplify(G3.inv() * G3.applyfunc(X))

# ================= PART 0 — F-b2 GATE: reproduce the parent's D3 exactly ====
require("P00_G3_det_matches_parent", sp.factor(G3.det()) == -b * c**2)
require("P01_trace_matches_parent", sp.simplify(sp.trace(D3) - db / b) == 0)

charpoly = sp.factor(D3.charpoly(lam).as_expr())
parent_charpoly = sp.factor(
    lam**3
    - (db / b) * lam**2
    + (alpha**2 * df**2 * u / b - df**2 / (b * u) - 4 * chi**2) * lam
    - 2 * alpha**2 * df**2 * u * chi / b
    + 4 * db * chi**2 / b
    - 2 * df**2 * chi / (b * u)
)
require("P02_charpoly_matches_parent", sp.simplify(charpoly - parent_charpoly) == 0)
require(
    "P03_p_minus_2chi_matches_parent",
    sp.factor(charpoly.subs(lam, -2 * chi)) == -4 * alpha**2 * df**2 * u * chi / b,
)
require(
    "P04_p_plus_2chi_matches_parent",
    sp.factor(charpoly.subs(lam, 2 * chi)) == -4 * df**2 * chi / (b * u),
)
require(
    "P05_D3_K_Ycomponent_matches_parent",
    sp.simplify(D3[2, 0] - (-alpha * c * df * u / b)) == 0,
)
require(
    "P06_D3_V_Ycomponent_matches_parent",
    sp.simplify(D3[2, 1] - (-df * (alpha**2 * u**2 - 1) / (b * u))) == 0,
)
require(
    "P07_df0_factorization_matches_parent",
    sp.factor(
        charpoly.subs(df, 0) - (lam + 2 * chi) * (lam - 2 * chi) * (lam - db / b)
    )
    == 0,
)
# full-matrix cross-check against the parent MACHINE record (expected_D of
# derive_higher_isometry_plane_ownership.py, check A04 there):
parent_D3 = sp.Matrix(
    [
        [-2 * chi, -4 * alpha * chi / c, -4 * alpha * chi * f / c],
        [
            alpha * c * df * f * u / b,
            (alpha**2 * df * f * u**2 + 2 * b * chi * u - df * f) / (b * u),
            (
                alpha**2 * df * f**2 * u**2
                + 2 * b * chi * f * u
                + b * df * u
                - db * f * u
                - df * f**2
            )
            / (b * u),
        ],
        [
            -alpha * c * df * u / b,
            -df * (alpha * u - 1) * (alpha * u + 1) / (b * u),
            -(alpha**2 * df * f * u**2 - db * u - df * f) / (b * u),
        ],
    ]
)
require(
    "P08_full_D3_matches_parent_machine_record",
    sp.simplify(D3 - parent_D3) == sp.zeros(3),
)

if not all_ok():
    print("F-b2 FIRED: parent D3 entries NOT reproduced. STOP (per contract).")
    summary = {
        "schema": "r09_certificate_adjudication_v1",
        "falsifier_F_b2": "FIRED",
        "checks": CHECKS,
    }
    print(json.dumps(summary, indent=1))
    sys.exit(2)

# ============ PART 1 — invariance conditions I1, I2 in exact closed form ====
K_col = sp.Matrix([1, 0, 0])
W_col = sp.Matrix([0, m, n])


def L(v):
    return n * v[1] - m * v[2]


I1 = sp.simplify(L(D3 * K_col))
I2 = sp.simplify(L(D3 * W_col))

E1_closed = alpha * c * df * u * z / b
E2_closed = (
    alpha**2 * df * u**2 * z**2 + u * n * z * (2 * b * chi - db) + df * (n**2 * b * u - z**2)
) / (b * u)
require("C01_I1_closed_form", sp.simplify(I1 - E1_closed) == 0)
require("C02_I2_closed_form", sp.simplify(I2 - E2_closed) == 0)
# parent-R02 correspondence: (m,n)=(1,0) gives (minus) the parent's quoted
# Y-components of D3(K), D3(V):
require(
    "C03_R02_correspondence_registered_plane",
    sp.simplify(I1.subs({m: 1, n: 0}) + D3[2, 0]) == 0
    and sp.simplify(I2.subs({m: 1, n: 0}) + D3[2, 1]) == 0,
)

# ===================== PART 2 — T-b1: stratified enumeration ================
# Stratum A: alpha != 0, df != 0.  I1 = 0 with u,c,b > 0 and alpha*df != 0
# forces z = 0 at the point; then I2 collapses:
require(
    "SA1_I2_on_z_zero_slice",
    sp.simplify(I2.subs(m, -n * f) - df * n**2) == 0,
)
# so I2 = df n^2 != 0 unless n = 0, and z = 0 with n = 0 gives m = 0:
# NO plane is D3-invariant at ANY single point with alpha*df != 0 (pointwise
# emptiness; documented in EXACT_DERIVATION.md Sec T-b1).

# Strata B/D: df = 0 (either alpha).  Both conditions reduce to one product:
require("SB1_I1_vanishes_at_df0", sp.simplify(I1.subs(df, 0)) == 0)
require(
    "SB2_I2_factored_at_df0",
    sp.simplify(I2.subs(df, 0) - n * z * (2 * chi - db / b)) == 0,
)
# db-free reading (identity in the free jet symbols db, f, chi): n*z != 0 is
# impossible identically, so n = 0: span(K,V) is the UNIQUE invariant plane.
# Pointwise exceptional loci: z = 0 (plane span(K, H-direction)) or
# db = 2 b chi (EVERY plane invariant).  Rates on each, gated below (T-b4):
D3_df0 = D3.subs(df, 0)
require(
    "SB3_registered_plane_rates_founded_at_df0",
    sp.simplify(D3_df0 * K_col - (-2 * chi) * K_col) == sp.zeros(3, 1)
    and sp.simplify(
        D3_df0 * sp.Matrix([0, 1, 0])
        - ((-4 * alpha * chi / c) * K_col + 2 * chi * sp.Matrix([0, 1, 0]))
    )
    == sp.zeros(3, 1),
)
D3_deg = D3.subs({df: 0, db: 2 * b * chi})
require(
    "SB4_degenerate_locus_D3_is_minus2chi_plus_2chi_block",
    sp.simplify(
        D3_deg
        - sp.Matrix(
            [
                [-2 * chi, -4 * alpha * chi / c, -4 * alpha * chi * f / c],
                [0, 2 * chi, 0],
                [0, 0, 2 * chi],
            ]
        )
    )
    == sp.zeros(3),
)
require(
    "SB5_degenerate_locus_every_plane_founded",
    sp.simplify(
        D3_deg * W_col - ((-4 * alpha * chi * z / c) * K_col + 2 * chi * W_col)
    )
    == sp.zeros(3, 1),
)
H_col = sp.Matrix([0, -n * f, n])  # z = 0 representative: W = n(Y - f V) ~ H
require(
    "SB6_pointwise_z0_plane_rate_db_over_b",
    sp.simplify(D3_df0 * H_col - (db / b) * H_col) == sp.zeros(3, 1),
)

# Stratum C: alpha = 0, df != 0.  I1 == 0 identically; I2 = 0 has NO solution
# with db free (coefficient of db is -n z/b; n z = 0 kills it but then
# I2 = -m^2 df/(b u) (n=0) or df n^2 (z=0), both nonzero).  Gates:
require("SC1_I1_vanishes_at_alpha0", sp.simplify(I1.subs(alpha, 0)) == 0)
require(
    "SC2_db_coefficient",
    sp.simplify(sp.diff(I2.subs(alpha, 0), db) + n * z / b) == 0,
)
require(
    "SC3_n0_obstruction",
    sp.simplify(I2.subs({alpha: 0, n: 0}) + m**2 * df / (b * u)) == 0,
)
# Fixed-member locus (db equal to the member's own X(b)): invariance iff
db_locus = 2 * b * chi + df * (n**2 * b * u - z**2) / (u * n * z)
I2_locus = sp.simplify(I2.subs(alpha, 0).subs(db, db_locus))
require("SC4_locus_solves_invariance", I2_locus == 0)
# rates on the locus: D3(K) = -2 chi K and D3(W) = mu W with mu = 2chi + n df/z
D3_a0 = D3.subs(alpha, 0)
require(
    "SC5_alpha0_K_exact_eigenvector",
    sp.simplify(D3_a0 * K_col - (-2 * chi) * K_col) == sp.zeros(3, 1),
)
mu = 2 * chi + n * df / z
require(
    "SC6_locus_rate_mu",
    sp.simplify(D3_a0.subs(db, db_locus) * W_col - mu * W_col) == sp.zeros(3, 1),
)
require("SC7_rate_defect_exact", sp.simplify(mu - 2 * chi - n * df / z) == 0)
# mu - 2chi = n df / z != 0 wherever df != 0 (invariance forces n != 0, z != 0
# there) -> the founded-rates leg FAILS at every alpha = 0, df != 0 invariant
# point.  This is the with-leg emptiness engine (T-b2).

# ================= PART 3 — T-b2: the adjudication ==========================
# (b-i) WITHOUT-rates-leg CONFLICT witness (principal-orbit admissibility):
# member: alpha = 0, Hopf chart, V = d_xi1 + d_xi2, Y = d_xi1 - d_xi2,
# f = cos(2 eta) (parent Sec.6 registration), u = 2 + f, b u = 6 + f - f^2,
# X = d/d eta, principal region eta in (0, pi/2).  Plane P = span(K, 2V + Y).
eta = sp.symbols("eta", real=True)
fw = sp.cos(2 * eta)
uw = 2 + fw
sw = 6 + fw - fw**2
bw = sw / uw
chiw = -sp.diff(uw, eta) / (2 * uw)
dfw = sp.diff(fw, eta)
dbw = sp.diff(bw, eta)
wsub = {alpha: 0, u: uw, b: bw, f: fw, chi: chiw, df: dfw, db: dbw}

require("W00_bu_positive_factorization", sp.expand((3 - f) * (2 + f) - (6 + f - f**2)) == 0)


def I_w(mm, nn):
    return (
        sp.simplify(I1.subs(wsub).subs({m: mm, n: nn})),
        sp.simplify(I2.subs(wsub).subs({m: mm, n: nn})),
    )


i1w, i2w = I_w(2, 1)
require("W01_P_2V_plus_Y_invariant_everywhere", i1w == 0 and i2w == 0)
i1w2, i2w2 = I_w(-3, 1)
require("W02_second_invariant_plane_minus3V_plus_Y", i1w2 == 0 and i2w2 == 0)
# the COMPLETE invariant-plane list on the witness: I2 * b u = -df (m+3n)(m-2n)
T_w = sp.simplify(I2.subs(wsub) * bw * uw)
require(
    "W03_witness_complete_enumeration_quadratic",
    sp.simplify(T_w + dfw * (m + 3 * n) * (m - 2 * n)) == 0,
)
# span(K,V), span(K,Y), span(K,V+Y) all FAIL C_full on the witness:
require(
    "W04_registered_and_other_planes_fail",
    all(
        sp.simplify(I_w(a_, b_)[1].subs(eta, sp.pi / 6)) != 0
        for (a_, b_) in [(1, 0), (0, 1), (1, 1)]
    ),
)
# C_restricted side: b u + f^2 = 6 + f is NONCONSTANT (X of it = df != 0), so
# the selector theorem branch (c) crowns span(K,V) uniquely on this member:
require(
    "W05_bu_plus_f2_nonconstant",
    sp.simplify(sp.diff(sw + fw**2, eta) - dfw) == 0
    and sp.simplify(dfw.subs(eta, sp.pi / 6)) != 0,
)
# direct C_restricted leg (i) exact areas (native recomputation, matches the
# selector T6 record): det G(K, mV+nY) = -c^2 (z^2 + n^2 b u)
G_KW = sp.Matrix(
    [
        [-c**2 * u, -c * alpha * u * z],
        [-c * alpha * u * z, Q * z**2 + n**2 * b],
    ]
)
require(
    "W06_det_GKW_matches_selector_T6",
    sp.simplify(G_KW.det() + c**2 * (z**2 + n**2 * b * u)) == 0,
)
XdetKW = sp.simplify(X(G_KW.det()))
require(
    "W07_Xdet_matches_selector_T6",
    sp.simplify(XdetKW + c**2 * (2 * m * n * df + n**2 * X(b * u + f**2))) == 0,
)
require(
    "W08_P_fails_C_restricted_area_leg",
    sp.simplify(XdetKW.subs(wsub).subs({m: 2, n: 1}) + 5 * c**2 * dfw) == 0
    and sp.simplify((5 * c**2 * dfw).subs(eta, sp.pi / 6)) != 0,
)
require(
    "W09_registered_plane_keeps_constant_area",
    sp.simplify(XdetKW.subs({m: 1, n: 0})) == 0,
)
# rates of D3 restricted to the witness plane P: (-2 chi, 2 chi + df/(2+f))
mu_w = sp.simplify((2 * chi + n * df / z).subs(wsub).subs({m: 2, n: 1}))
img_w = sp.simplify((D3_a0 * sp.Matrix([0, 2, 1])).subs(wsub))
require(
    "W10_witness_rate",
    sp.simplify(img_w - mu_w * sp.Matrix([0, 2, 1])) == sp.zeros(3, 1)
    and sp.simplify(mu_w - (2 * chiw + dfw / (2 + fw))) == 0
    and sp.simplify((mu_w - 2 * chiw).subs(eta, sp.pi / 6)) != 0,
)

# (b-ii) cap-closure corollary.  On any interval where df != 0 pointwise,
# region-wide invariance (alpha = 0) is a linear first-order ODE in s = b u as
# a function of f; its full solution family is s = z (Ct - f/n):
Ct = sp.Symbol("C_t", real=True)
s_gen = z * (Ct - f / n)
lhs = sp.diff(s_gen, f)  # X(s)/df with X = df * d/df on f-parameterized data
rhs = (n**2 * s_gen - z**2) / (n * z)
require("K01_general_solution_of_invariance_ODE", sp.simplify(lhs - rhs) == 0)
hom = sp.Symbol("A_h") * z
require(
    "K02_homogeneous_solutions_are_multiples_of_z",
    sp.simplify(sp.diff(hom, f) - n * hom / z) == 0,
)
# two-cap closure b u -> 0 at f = +1 AND f = -1:
s_p1 = sp.factor(s_gen.subs(f, 1))
s_m1 = sp.factor(s_gen.subs(f, -1))
require(
    "K03_cap_conditions_factor",
    sp.simplify(s_p1 - (m + n) * (Ct - 1 / n)) == 0
    and sp.simplify(s_m1 - (m - n) * (Ct + 1 / n)) == 0,
)
require(
    "K04_cap_branch_m_eq_n_gives_1_minus_f2",
    sp.simplify(s_gen.subs({m: n, Ct: 1 / n}) - (1 - f**2)) == 0,
)
require(
    "K05_cap_branch_m_eq_minus_n_gives_1_minus_f2",
    sp.simplify(s_gen.subs({m: -n, Ct: -1 / n}) - (1 - f**2)) == 0,
)
require("K06_generic_mn_two_cap_contradiction", sp.simplify(sp.Rational(1, 1) / n - (-1 / n)) != 0)
# both closing branches land EXACTLY on the selector's exceptional stratum:
require(
    "K07_closing_branches_on_exceptional_stratum",
    sp.simplify((1 - f**2) + f**2 - 1) == 0,
)
# parent Sec.6 witness realization: b = (1-f^2)/u, any u(eta): planes
# span(K, V+Y) and span(K, V-Y) (= the two coordinate-circle planes) are
# D3-invariant.  Gate at the jet level with db = X((1-f^2)/u):
b_pw = (1 - f**2) / u
db_pw = sp.simplify(-2 * f * df / u + 2 * chi * (1 - f**2) / u)  # = X(b_pw)
require(
    "K08_db_of_parent_witness",
    sp.simplify(
        sp.diff(b_pw, u) * (-2 * chi * u) + sp.diff(b_pw, f) * df - db_pw
    )
    == 0,
)
for name, (mm, nn) in [("K09_parent_witness_V_plus_Y", (1, 1)), ("K10_parent_witness_V_minus_Y", (-1, 1))]:
    val = sp.simplify(I2.subs(alpha, 0).subs({m: mm, n: nn}).subs({b: b_pw, db: db_pw}))
    require(name, val == 0)

# ============ PART 4 — numeric spot checks (exact rationals, seeded) ========
rng = random.Random(20260728)


def rq(lo=-9, hi=9, den=4):
    return sp.Rational(rng.randint(lo, hi), rng.randint(1, den))


def rq_pos():
    return sp.Rational(rng.randint(1, 9), rng.randint(1, 4))


def rq_nz(lo=-9, hi=9):
    while True:
        v = rq(lo, hi)
        if v != 0:
            return v


NUM = {"A": [], "B": [], "C": [], "D": [], "W": []}

for i in range(5):
    # ---- stratum A: alpha != 0, df != 0 ----
    pt = {u: rq_pos(), b: rq_pos(), f: rq(), chi: rq(), db: rq(), c: rq_pos(), alpha: rq_nz(), df: rq_nz()}
    mn = (rq_nz(), rq_nz())
    v1 = I1.subs(pt).subs({m: mn[0], n: mn[1]})
    v2 = I2.subs(pt).subs({m: mn[0], n: mn[1]})
    okA1 = sp.simplify(v1) != 0 or sp.simplify(v2) != 0  # generic plane fails
    # tuned z = 0 plane (m = -n f): I1 = 0 but I2 = n^2 df != 0
    nn_ = rq_nz()
    v1z = sp.simplify(I1.subs(pt).subs({m: -nn_ * pt[f], n: nn_}))
    v2z = sp.simplify(I2.subs(pt).subs({m: -nn_ * pt[f], n: nn_}))
    okA2 = v1z == 0 and v2z == nn_**2 * pt[df] and v2z != 0
    NUM["A"].append(okA1 and okA2)
    require("N_A_pt%d" % i, okA1 and okA2)

    # ---- stratum B: alpha != 0, df = 0 ----
    pt = {u: rq_pos(), b: rq_pos(), f: rq(), chi: rq_nz(), db: rq_nz(), c: rq_pos(), alpha: rq_nz(), df: sp.Integer(0)}
    okB1 = (
        sp.simplify(I1.subs(pt).subs({m: 1, n: 0})) == 0
        and sp.simplify(I2.subs(pt).subs({m: 1, n: 0})) == 0
    )  # span(K,V) invariant
    mn = (rq(), rq_nz())
    zval = mn[0] + mn[1] * pt[f]
    v2 = sp.simplify(I2.subs(pt).subs({m: mn[0], n: mn[1]}))
    okB2 = (v2 == 0) == (zval * (2 * pt[chi] - pt[db] / pt[b]) == 0)  # exact locus law
    ptdeg = dict(pt)
    ptdeg[db] = 2 * pt[b] * pt[chi]
    v2d = sp.simplify(I2.subs(ptdeg).subs({m: mn[0], n: mn[1]}))
    okB3 = v2d == 0  # degenerate locus: every plane invariant
    NUM["B"].append(okB1 and okB2 and okB3)
    require("N_B_pt%d" % i, okB1 and okB2 and okB3)

    # ---- stratum C: alpha = 0, df != 0 ----
    pt = {u: rq_pos(), b: rq_pos(), f: rq(), chi: rq(), c: rq_pos(), alpha: sp.Integer(0), df: rq_nz()}
    while True:
        mn = (rq(), rq_nz())
        if mn[0] + mn[1] * pt[f] != 0:
            break
    zval = mn[0] + mn[1] * pt[f]
    dbv = 2 * pt[b] * pt[chi] + pt[df] * (mn[1] ** 2 * pt[b] * pt[u] - zval**2) / (pt[u] * mn[1] * zval)
    ptl = dict(pt)
    ptl[db] = dbv
    v1 = sp.simplify(I1.subs(ptl).subs({m: mn[0], n: mn[1]}))
    v2 = sp.simplify(I2.subs(ptl).subs({m: mn[0], n: mn[1]}))
    okC1 = v1 == 0 and v2 == 0  # locus db makes the plane invariant
    muv = 2 * pt[chi] + mn[1] * pt[df] / zval
    img = (D3_a0 * sp.Matrix([0, mn[0], mn[1]])).subs(ptl)
    okC2 = sp.simplify(img - muv * sp.Matrix([0, mn[0], mn[1]])) == sp.zeros(3, 1)
    okC3 = sp.simplify(muv - 2 * pt[chi]) != 0  # founded-rates leg fails
    ptg = dict(pt)
    ptg[db] = dbv + 1  # generic db: invariance fails
    okC4 = sp.simplify(I2.subs(ptg).subs({m: mn[0], n: mn[1]})) != 0
    okC5 = sp.simplify(I2.subs(ptg).subs({m: 1, n: 0})) != 0  # span(K,V) fails
    ok = okC1 and okC2 and okC3 and okC4 and okC5
    NUM["C"].append(ok)
    require("N_C_pt%d" % i, ok)

    # ---- stratum D: alpha = 0, df = 0 ----
    pt = {u: rq_pos(), b: rq_pos(), f: rq(), chi: rq_nz(), db: rq_nz(), c: rq_pos(), alpha: sp.Integer(0), df: sp.Integer(0)}
    okD1 = (
        sp.simplify(I1.subs(pt).subs({m: 1, n: 0})) == 0
        and sp.simplify(I2.subs(pt).subs({m: 1, n: 0})) == 0
    )
    mn = (rq(), rq_nz())
    zval = mn[0] + mn[1] * pt[f]
    v2 = sp.simplify(I2.subs(pt).subs({m: mn[0], n: mn[1]}))
    okD2 = (v2 == 0) == (zval * (2 * pt[chi] - pt[db] / pt[b]) == 0)
    ptdeg = dict(pt)
    ptdeg[db] = 2 * pt[b] * pt[chi]
    okD3 = sp.simplify(I2.subs(ptdeg).subs({m: mn[0], n: mn[1]})) == 0
    ok = okD1 and okD2 and okD3
    NUM["D"].append(ok)
    require("N_D_pt%d" % i, ok)

# witness spot checks at 6 exact eta values in (0, pi/2):
for j, ev in enumerate([sp.pi / 12, sp.pi / 8, sp.pi / 6, sp.pi / 4, sp.pi / 3, sp.Rational(5, 12) * sp.pi]):
    r1 = sp.simplify(i1w.subs(eta, ev)) if hasattr(i1w, "subs") else i1w
    r2 = sp.simplify(I2.subs(wsub).subs({m: 2, n: 1}).subs(eta, ev))
    r3 = sp.simplify(I2.subs(wsub).subs({m: -3, n: 1}).subs(eta, ev))
    r4 = sp.simplify(I2.subs(wsub).subs({m: 1, n: 0}).subs(eta, ev))
    r5 = sp.simplify(sp.diff(sw + fw**2, eta).subs(eta, ev))
    bval = sp.simplify(bw.subs(eta, ev))
    uval = sp.simplify(uw.subs(eta, ev))
    ok = (
        (r1 == 0 or r1 == sp.S.Zero)
        and r2 == 0
        and r3 == 0
        and r4 != 0
        and r5 != 0
        and bval > 0
        and uval > 0
    )
    NUM["W"].append(bool(ok))
    require("N_W_pt%d" % j, ok)

# ========================= PART 5 — assemble the verdicts ===================
t_b1 = {
    "invariance_formulation": (
        "P=span(K,W), W=mV+nY, (m,n)!=(0,0); membership L(v)=n*v_V-m*v_Y; "
        "P D3-invariant at a point iff I1=L(D3 K)=0 and I2=L(D3 W)=0; "
        "on a region iff at every point (parent R02 usage, gated C03)"
    ),
    "exact_conditions": {
        "I1": "alpha*c_E*df*u*(m+n*f)/b",
        "I2": "[alpha^2*df*u^2*(m+n*f)^2 + u*n*(m+n*f)*(2*b*chi-db) + df*(n^2*b*u-(m+n*f)^2)]/(b*u)",
    },
    "strata": {
        "alpha_nonzero_df_nonzero": {
            "invariant_planes": "NONE — empty even POINTWISE (I1=0 forces z=m+n*f=0; then I2=df*n^2!=0 unless n=0, and z=0,n=0 gives m=0)",
        },
        "alpha_nonzero_df_zero": {
            "invariant_planes_db_free": "span(K,V) UNIQUELY (I2=n*z*(2*chi-db/b); identity in free db,f forces n=0)",
            "pointwise_exceptions": "z=0 (plane span(K,H), rate db/b) or db=2*b*chi (EVERY plane invariant, founded rates)",
        },
        "alpha_zero_df_nonzero": {
            "invariant_planes_db_free": "NONE (db-coefficient -n*z/b must vanish; n=0 gives I2=-m^2*df/(b*u)!=0; z=0 gives I2=df*n^2!=0)",
            "fixed_member_locus": "db = 2*b*chi + df*(n^2*b*u-z^2)/(u*n*z) with n*z!=0 — realizable member-wise (T-b2 witness); rates (-2*chi, 2*chi+n*df/z)",
        },
        "alpha_zero_df_zero": {
            "invariant_planes_db_free": "span(K,V) UNIQUELY (same factorization as alpha!=0, df=0)",
            "pointwise_exceptions": "z=0 or db=2*b*chi (same as alpha!=0 stratum)",
        },
    },
}

t_b2 = {
    "C_full_WITH_founded_rates_leg": {
        "verdict": "NO-CONFLICT",
        "basis": (
            "C_full-with-rates is EMPTY on every admissible member: {df!=0} is a "
            "nonempty open set (parent T4, banked); at any such point alpha!=0 "
            "kills invariance outright (stratum A pointwise emptiness), and "
            "alpha=0 invariance forces n!=0, z!=0, db=locus, whereupon the "
            "second restricted rate is 2*chi+n*df/z != +2*chi — the rates leg "
            "fails there, hence region-wide"
        ),
    },
    "C_full_WITHOUT_founded_rates_leg": {
        "verdict": "CONFLICT",
        "falsifier_F_b1": "FIRED (first-class outcome, preregistered)",
        "admissibility": "principal-orbit-region member (the parents' evaluation domain; premise ledger 'principal orbits only')",
        "witness": {
            "member": "alpha=0; Hopf chart; V=d_xi1+d_xi2, Y=d_xi1-d_xi2; f=cos(2*eta); u=2+f; b*u=6+f-f^2=(3-f)*(2+f)>0; X=d/d_eta; eta in (0,pi/2); c_E>0 arbitrary; q_B torus-invariant positive with q_B(H,H)=b",
            "conflicting_plane": "P=span(K, 2V+Y) (and also span(K, -3V+Y)); complete list on this member: (m+3n)(m-2n)=0",
            "C_full_status": "P is D3-invariant at EVERY principal point (W01/W02, zero-residual)",
            "C_restricted_status": "b*u+f^2=6+f NONCONSTANT, so C_restricted crowns span(K,V) uniquely (selector branch (c)); P itself FAILS C_restricted leg (i): X(det G(K,W))=-5*c_E^2*df!=0",
            "crowns": "the two criteria crown DIFFERENT planes on this member",
            "K_eigenline_note": "at alpha=0, K is an exact D3 eigenvector (rate -2*chi), so adding a K-eigenline leg to C_full would NOT dissolve the conflict; only the founded-rates leg does",
        },
    },
    "cap_closure_corollary_record": {
        "statement": (
            "if admissibility is strengthened to complete two-cap S3 members "
            "(b->0 at BOTH caps, forced since the base projection of Y vanishes "
            "at the poles) and df!=0 throughout the principal region, then "
            "region-wide invariance (alpha=0) forces s=b*u=z*(Ct-f/n) and cap "
            "closure forces (m,n) prop (1,1) or (1,-1) with b*u=1-f^2, hence "
            "b*u+f^2=1 CONSTANT: the member lies ON the selector's exceptional "
            "stratum, C_restricted is silent, and NO-CONFLICT is restored even "
            "without the rates leg. The parent Sec.6 witness realizes this: "
            "span(K,V+Y) and span(K,V-Y) (the two coordinate-circle planes) are "
            "D3-invariant on it (K09/K10)"
        ),
        "status": "RECORD (conditional on the pointwise df!=0 strengthening / standard toric presentation)",
    },
}

t_b3 = {
    "df_zero_strata_crowning": {
        "alpha_nonzero_db_neq_2bchi": "AGREE — both crown span(K,V) (C_full unique invariant with founded rates; C_restricted always selects at alpha!=0)",
        "alpha_zero_db_neq_2bchi": "AGREE — both crown span(K,V) (at df=0, X(b*u+f^2)=u*(db-2*b*chi)!=0 so C_restricted selects)",
        "alpha_zero_db_eq_2bchi": "AGREEMENT-IN-SILENCE — C_restricted silent (exceptional stratum) and C_full non-selective (every plane invariant, founded)",
        "alpha_nonzero_db_eq_2bchi": "formal pointwise disagreement (C_full non-selective, all planes founded-invariant; C_restricted selects span(K,V)) — UNREALIZABLE region-wide on admissible members (Cartan/T4: {df!=0} nonempty open)",
        "realizability_note": "df=0 strata are jet-level strata; under parent T4's pointwise strengthening they contain no admissible-member points at all",
    }
}

t_b4 = {
    "rate_spectra_record": [
        {"plane": "span(K,V)", "locus": "df=0 (any alpha)", "spectrum": "(-2*chi, +2*chi)", "founded": True},
        {"plane": "every span(K,W)", "locus": "df=0 and db=2*b*chi (any alpha)", "spectrum": "(-2*chi, +2*chi)", "founded": True},
        {"plane": "span(K,H) (z=0, pointwise)", "locus": "df=0", "spectrum": "(-2*chi, db/b)", "founded": "only if db=2*b*chi"},
        {"plane": "span(K,mV+nY), n*z!=0 on db-locus", "locus": "alpha=0, df!=0, db=2*b*chi+df*(n^2*b*u-z^2)/(u*n*z)", "spectrum": "(-2*chi, 2*chi+n*df/z)", "founded": False},
        {"plane": "witness P=span(K,2V+Y)", "locus": "witness member", "spectrum": "(-2*chi, 2*chi+df/(2+f))", "founded": False},
        {"plane": "parent-witness span(K,V+Y), span(K,V-Y)", "locus": "b*u=1-f^2, alpha=0", "spectrum": "(-2*chi, 2*chi+df/(f+1)) resp. (-2*chi, 2*chi+df/(f-1))", "founded": False},
    ]
}

summary = {
    "schema": "r09_certificate_adjudication_v1",
    "contract": "udt_r09_certificate_adjudication_2026-07-28/PREREGISTRATION.md",
    "parents": [
        "udt_higher_isometry_plane_ownership_audit_2026-07-28/EXACT_DERIVATION.md",
        "udt_alpha_plane_selector_theorem_2026-07-28/EXACT_DERIVATION.md",
    ],
    "falsifiers": {
        "F_b1": "FIRED for the WITHOUT-founded-rates-leg variant (CONFLICT witness exhibited); NOT fired for the WITH-leg variant",
        "F_b2": "NOT FIRED — parent D3 reproduced exactly (P00-P08, zero-residual)",
    },
    "T_b1": t_b1,
    "T_b2": t_b2,
    "T_b3": t_b3,
    "T_b4": t_b4,
    "check_count": len(CHECKS),
    "checks_passed": sum(1 for cc in CHECKS if cc["ok"]),
    "numeric_spot_checks": {k: len(v) for k, v in NUM.items()},
    "all_checks_pass": all_ok(),
    "checks": CHECKS,
}

print(json.dumps(summary, indent=1))

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "DERIVATION_RESULT.json"), "w") as fh:
    json.dump(summary, fh, indent=1)
    fh.write("\n")

sys.exit(0 if all_ok() else 1)
