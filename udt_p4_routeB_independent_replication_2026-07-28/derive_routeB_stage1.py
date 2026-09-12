#!/usr/bin/env python3
"""
P4 Route B Stage 1 -- extension-stratum classification under C1/C2/C3(algebraic
cross-checks only)/T4 seat map.  Contract: PREREGISTRATION.md in this package
(targets T1-T5 mechanized here; T5 is citation assembly, only its algebraic
cross-checks run here).  Fully symbolic sympy; CPU only; no numeric solves;
every check is a zero-residual / exact-solve test; failures recorded as-is
(falsifier F-C); exit 0 iff all pass.

REPRESENTATION (stated per the T1 representation-care clause):
  * The registered chart presents the coframe as a COLUMN e of 4 one-forms,
    slots ordered (clock, ruler, screen1, screen2) = indices (0,1,2,3).
  * The extension operation acts on the coframe by LEFT multiplication:
        e  ->  exp(phi X) e,
    with X = [[H, 0], [C, K]], H = diag(-1, +1) fixed (founded, G01/G02),
    K = [[a, b], [0, d]] triangular (registered chart), C = 2x2 mixing block.
    (Conventions identical to udt_founded_phi_complete_coframe_extension_audit_
    2026-07-25/derive_extension_class.py; E07 = diag(-1,+1,-k,+k), E08 = lower
    shift s(1-e^{-phi}).)
  * A local Lorentz gauge change acts on FRAME indices, also on the left:
        e  ->  L e,   L in SO+(1,3),  lam in so(1,3):  lam^T eta + eta lam = 0,
        eta = diag(-1, 1, 1, 1).
    The SAME physical extension operation expressed in the new gauge is
        X  ->  L X L^{-1},     infinitesimally   delta_lam X = [lam, X].
    T1 therefore computes ad_lam(X) = lam*X - X*lam restricted to the class.
  * Composition order convention (T2/T3): "phi1 then phi2" means the segment-2
    map is applied AFTER segment 1, i.e. the matrix product is
        g_2 * g_1   (later action multiplies on the LEFT).

BANKED INPUTS (cited, verified here only as consistency cross-checks, never
re-derived as new results):
  * scalar-only so(1,3)-centralizer / equivariance correction and zero active
    selector rank: udt_complete_coframe_native_selector_audit_2026-07-26.
  * so(1,3) perfect (no additive characters); holonomy centralizer dims
    1/3/3/1 for X_lambda: udt_metric_natural_joint_selector_nogo_2026-07-28.
  * conditional SO(3)->+1 / SO+(1,2)->-1 / swap->lambda=0(diagonal subfamily):
    udt_metric_natural_complete_extension_selector_audit_2026-07-27.
  * isotropic orbit metric, V_q exponent (1+2*lambda), blind at lambda=-1/2:
    udt_metric_native_selector_rank_closure_audit_2026-07-27.
"""

import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------
phi, phi1, phi2, psi = sp.symbols("phi phi1 phi2 psi", real=True)
a, b, d, k21 = sp.symbols("a b d k21", real=True)
s11, s12, s21, s22 = sp.symbols("s11 s12 s21 s22", real=True)
lamq = sp.Symbol("lambda_iso", real=True)   # isotropic seat coordinate
kq = sp.Symbol("k_e07", real=True)          # E07 seat coordinate
c = sp.Symbol("c", positive=True)
theta = sp.Symbol("theta", real=True)
# gauge parameters, ordered basis (B01, B02, B03, R12, R13, R23)
t1, t2, t3, r1, r2, r3 = sp.symbols("t1 t2 t3 r1 r2 r3", real=True)
GAUGE = (t1, t2, t3, r1, r2, r3)

eta = sp.diag(-1, 1, 1, 1)
H = sp.diag(-1, 1)


def E(i, j):
    M = sp.zeros(4)
    M[i, j] = 1
    return M


# so(1,3) basis: boosts symmetric, rotations antisymmetric (this signature)
B01 = E(0, 1) + E(1, 0)
B02 = E(0, 2) + E(2, 0)
B03 = E(0, 3) + E(3, 0)
R12 = E(1, 2) - E(2, 1)
R13 = E(1, 3) - E(3, 1)
R23 = E(2, 3) - E(3, 2)
BASIS = [B01, B02, B03, R12, R13, R23]
LAM = sum((g * M for g, M in zip(GAUGE, BASIS)), sp.zeros(4))


def classX(av, bv, dv, k21v, c11, c12, c21, c22):
    K = sp.Matrix([[av, bv], [k21v, dv]])
    C = sp.Matrix([[c11, c12], [c21, c22]])
    return H.row_join(sp.zeros(2)).col_join(C.row_join(K))


XT = classX(a, b, d, 0, s11, s12, s21, s22)          # triangular chart member
XF = classX(a, b, d, k21, s11, s12, s21, s22)        # full-K (chart dropped)
X0 = classX(0, 0, 0, 0, 0, 0, 0, 0)                  # spectator E06
XLAM = sp.diag(-1, 1, lamq, lamq)                    # isotropic line member


def zero(e):
    e2 = sp.cancel(sp.together(sp.expand(sp.sympify(e))))
    if e2 == 0:
        return True
    e3 = sp.simplify(e2)
    if e3 == 0:
        return True
    r = sp.simplify(sp.trigsimp(e3)).equals(0)
    return bool(r) if r is not None else False


def mzero(M):
    return all(zero(x) for x in M)


checks = []


def record(name, ok, note):
    checks.append({"name": name, "pass": bool(ok), "note": note})
    print(("PASS" if ok else "FAIL"), name, "::", note)


def vanish_eqs(exprs, xparams):
    """Coefficient equations for 'exprs == 0 identically in xparams'."""
    eqs = []
    for e in exprs:
        e = sp.expand(e)
        if xparams:
            p = sp.Poly(e, *xparams)
            eqs.extend(p.coeffs())
        else:
            eqs.append(e)
    return eqs


def gauge_nullspace(eqs):
    """Solution space of linear homogeneous eqs in the 6 gauge params.

    Returns (dim, nullspace_basis, linear_ok)."""
    rows = []
    lin_ok = True
    for eq in eqs:
        row = [sp.diff(eq, g) for g in GAUGE]
        resid = sp.expand(eq - sum(rv * g for rv, g in zip(row, GAUGE)))
        if not zero(resid):
            lin_ok = False
        rows.append(row)
    M = sp.Matrix(rows) if rows else sp.zeros(1, 6)
    ns = M.nullspace()
    return len(ns), ns, lin_ok


def span_equals(ns, expected_cols):
    """Exact span equality of two column collections in R^6."""
    if len(ns) != len(expected_cols):
        return False
    if not ns:
        return True
    A = sp.Matrix.hstack(*ns)
    Bm = sp.Matrix.hstack(*expected_cols)
    both = sp.Matrix.hstack(A, Bm)
    return A.rank() == len(ns) and Bm.rank() == len(ns) and both.rank() == len(ns)


def unit6(i):
    v = sp.zeros(6, 1)
    v[i] = 1
    return v


def comm(A, B):
    return sp.expand(A * B - B * A)


# ===========================================================================
# T1 -- equivariance / covariance of the strata
# ===========================================================================
ok = all(mzero(M.T * eta + eta * M) for M in BASIS)
tan6 = sp.Matrix.hstack(*(M.reshape(16, 1) for M in BASIS))
record("T1_so13_basis_valid", ok and tan6.rank() == 6,
       "6 generators each satisfy lam^T*eta + eta*lam = 0; rank 6")

brackets = sp.Matrix.hstack(*(comm(Mi, Mj).reshape(16, 1)
                              for i, Mi in enumerate(BASIS)
                              for Mj in BASIS[i + 1:]))
record("T1_so13_perfect_crosscheck", brackets.rank() == 6,
       "[so(1,3),so(1,3)] spans all 6 directions -- consistency with the "
       "CITED perfectness fact (joint no-go 2026-07-28), not a re-derivation")

AD = comm(LAM, XF)          # generic gauge direction on generic full-K member
ADT = comm(LAM, XT)         # on triangular-chart member
XPAR_F = (a, b, d, k21, s11, s12, s21, s22)
XPAR_T = (a, b, d, s11, s12, s21, s22)

# (1) preservation of the upper-right-zero (block-lower-triangular) condition
eqs_ur = vanish_eqs([AD[i, j] for i in range(2) for j in range(2, 4)], XPAR_F)
dim_ur, ns_ur, lin_ur = gauge_nullspace(eqs_ur)
record("T1_split_stabilizer_dim2",
       lin_ur and dim_ur == 2 and span_equals(ns_ur, [unit6(0), unit6(5)]),
       "upper-right-zero condition preserved EXACTLY by span(B01, R23) = "
       "so(1,1)+so(2), dim 2: the base/angular split is only subgroup-"
       "covariant; for the 4 mixing generators the condition is not preserved")

# (2) add the fixed founded base block H: base block of ad must vanish
eqs_base = eqs_ur + vanish_eqs(
    [AD[i, j] for i in range(2) for j in range(2)], XPAR_F)
dim_b, ns_b, lin_b = gauge_nullspace(eqs_base)
record("T1_fixedH_stabilizer_dim1_so2",
       lin_b and dim_b == 1 and span_equals(ns_b, [unit6(5)]),
       "adding the fixed founded H = diag(-1,+1) cuts the stabilizer to "
       "span(R23) = so(2), dim 1: even the base boost B01 moves H "
       "([B01_base, H] != 0) -- consistent with the CITED scalar-only-"
       "centralizer correction (07-26)")

record("T1_base_boost_moves_H",
       not mzero(comm(sp.Matrix([[0, 1], [1, 0]]), H)),
       "[so(1,1) boost, H] = 2*[[0,1],[-1,0]] != 0: the founded generator is "
       "equivariant, not invariant, under base boosts (witness entry)")

# (3) add the triangular-chart condition K[1,0] = 0
eqs_tri = eqs_base + vanish_eqs([ADT[3, 2]], XPAR_T)
dim_t, ns_t, lin_t = gauge_nullspace(eqs_tri)
record("T1_triangular_chart_stabilizer_zero",
       lin_t and dim_t == 0,
       "the triangular-K chart condition cuts the stabilizer to {0}: the "
       "registered triangular presentation is CHART-DEPENDENT (a gauge "
       "section), not a covariant condition")

obstr = comm(R23, XT)[3, 2]
record("T1_triangularity_obstruction_is_d_minus_a",
       zero(obstr - (d - a)),
       "[R23, X]_[3,2] = d - a exactly (basis R23 = E23 - E32; a first run "
       "asserted a - d and FAILED on this sign -- recorded honestly, target "
       "corrected): R23 preserves triangularity only on the a = d locus")

# (4) trace condition (E03 det-one) is invariant under the FULL algebra
record("T1_trace_condition_fully_invariant",
       zero(sp.trace(AD)),
       "tr[lam, X] = 0 identically for generic lam in so(1,3) and generic "
       "class member: the det-one condition tr X = a + d = 0 is the unique "
       "stratum condition covariant under the FULL gauge algebra")

# (5) per-stratum stabilizers (full-K = chart-free form vs triangular chart)
XE04 = classX(0, 0, 0, 0, s11, s12, s21, s22)
AD04 = comm(LAM, XE04)
eqs04 = vanish_eqs(
    [AD04[i, j] for i in range(2) for j in range(4)]      # base + UR rows
    + [AD04[i, j] for i in range(2, 4) for j in range(2, 4)],  # angular block
    (s11, s12, s21, s22))
dim04, ns04, lin04 = gauge_nullspace(eqs04)
record("T1_E04_stabilizer_so2",
       lin04 and dim04 == 1 and span_equals(ns04, [unit6(5)]),
       "E04 (K=0, C free): stabilizer = span(R23), dim 1 -- covariant under "
       "the residual screen so(2) once the split+H are supplied")

XE05F = classX(a, b, d, k21, 0, 0, 0, 0)
AD05 = comm(LAM, XE05F)
eqs05 = vanish_eqs(
    [AD05[i, j] for i in range(2) for j in range(4)]
    + [AD05[i, j] for i in range(2, 4) for j in range(2)],   # lower-left = 0
    (a, b, d, k21))
dim05, ns05, lin05 = gauge_nullspace(eqs05)
record("T1_E05_fullK_stabilizer_so2",
       lin05 and dim05 == 1 and span_equals(ns05, [unit6(5)]),
       "E05 (C=0) in chart-free full-K form: stabilizer = span(R23), dim 1")

eqs05t = vanish_eqs(
    [comm(LAM, classX(a, b, d, 0, 0, 0, 0, 0))[i, j]
     for i in range(2) for j in range(4)]
    + [comm(LAM, classX(a, b, d, 0, 0, 0, 0, 0))[i, j]
       for i in range(2, 4) for j in range(2)]
    + [comm(LAM, classX(a, b, d, 0, 0, 0, 0, 0))[3, 2]],
    (a, b, d))
dim05t, _, lin05t = gauge_nullspace(eqs05t)
record("T1_E05_triangular_stabilizer_zero",
       lin05t and dim05t == 0,
       "E05 in the triangular chart: stabilizer {0} (chart artifact again)")

eqs06 = vanish_eqs(list(comm(LAM, X0)), [])
dim06, ns06, lin06 = gauge_nullspace(eqs06)
record("T1_E06_stabilizer_so2",
       lin06 and dim06 == 1 and span_equals(ns06, [unit6(5)]),
       "E06 spectator point: [lam, X0] = 0 iff lam in span(R23), dim 1 -- "
       "matches the CITED lambda=0 holonomy-centralizer dim 1 (07-28)")

# so(2)-fixed-point set inside the full 7-parameter triangular class
fix = sp.solve(list(comm(R23, XT)), [a, b, d, s11, s12, s21, s22], dict=True)
fix_ok = (len(fix) == 1 and fix[0].get(b, None) == 0
          and fix[0].get(a, None) == d
          and all(fix[0].get(sv, None) == 0 for sv in (s11, s12, s21, s22)))
record("T1_so2_fixed_set_is_isotropic_line", fix_ok,
       "[R23, X] = 0 within the class iff b=0, C=0, a=d: the EXACT fixed-"
       "point set of the residual screen so(2) is the isotropic line "
       "X_lambda = diag(-1,+1,lambda,lambda) -- reproduces the CITED "
       "SO(2)-screen row of the joint no-go table (07-28)")

# holonomy-centralizer dims for X_lambda (consistency with cited 1/3/3/1)
eqsL = vanish_eqs(list(comm(LAM, XLAM)), (lamq,))
dimL, _, linL = gauge_nullspace(eqsL)
dims_pm = []
for val in (1, -1, 0):
    eqsv = vanish_eqs(list(comm(LAM, XLAM.subs(lamq, val))), [])
    dv, _, lv = gauge_nullspace(eqsv)
    dims_pm.append((val, dv, lv))
record("T1_centralizer_dims_1_3_3_1",
       linL and dimL == 1
       and dims_pm[0][1:] == (3, True) and dims_pm[1][1:] == (3, True)
       and dims_pm[2][1:] == (1, True),
       "so(1,3)-centralizer of diag(-1,+1,lambda,lambda): generic 1, "
       "lambda=+1: 3, lambda=-1: 3, lambda=0: 1 -- consistency cross-check "
       "of the CITED dims (joint no-go 07-28), not a re-derivation")

# diagonal subfamily is NOT so(2)-stable off a=d
diag_move = comm(R23, sp.diag(-1, 1, a, d))
record("T1_diagonal_subfamily_not_so2_stable",
       zero(diag_move[2, 3] - (d - a)) and zero(diag_move[3, 2] - (d - a)),
       "[R23, diag(-1,1,a,d)] has symmetric off-diagonal screen entries "
       "(a-d): the diagonal (a,d) subfamily is a chart section, so(2)-stable "
       "only on its isotropic diagonal a=d")

# so(2)-invariants of the screen block K (what survives the residual gauge)
R2 = sp.Matrix([[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]])
Kfull = sp.Matrix([[a, b], [k21, d]])
Kc = R2 * Kfull * R2.T
record("T1_so2_invariants_tr_det_antisym",
       zero(sp.trace(Kc) - sp.trace(Kfull))
       and zero(sp.simplify(Kc.det() - Kfull.det()))
       and mzero(sp.simplify((Kc - Kc.T) - (Kfull - Kfull.T))),
       "under the residual so(2) conjugation the invariant content of the "
       "screen generator K is exactly (tr K, det K, antisymmetric part)")

Ke07 = sp.diag(-kq, kq)
Krot = sp.simplify(R2.subs(theta, sp.pi / 2) * Ke07 * R2.subs(theta, sp.pi / 2).T)
record("T1_e07_k_sign_is_chart",
       mzero(Krot - sp.diag(kq, -kq)),
       "a pi/2 screen rotation conjugates diag(-k,+k) -> diag(+k,-k): the "
       "SIGN of the E07 modulus k is chart gauge; the invariant is "
       "(tr K = 0, det K = -k^2), i.e. |k|")

# ===========================================================================
# T2 -- composition / closure
# ===========================================================================
a2s, b2s, d2s = sp.symbols("a2 b2 d2", real=True)
u11, u12, u21, u22 = sp.symbols("u11 u12 u21 u22", real=True)
X1 = classX(a, b, d, 0, s11, s12, s21, s22)
X2 = classX(a2s, b2s, d2s, 0, u11, u12, u21, u22)
BR = comm(X1, X2)
K1 = sp.Matrix([[a, b], [0, d]])
K2 = sp.Matrix([[a2s, b2s], [0, d2s]])
C1 = sp.Matrix([[s11, s12], [s21, s22]])
C2 = sp.Matrix([[u11, u12], [u21, u22]])
record("T2_bracket_block_formula",
       mzero(BR[:2, :2]) and mzero(BR[:2, 2:])
       and mzero(BR[2:, :2] - ((C1 - C2) * H + K1 * C2 - K2 * C1))
       and mzero(BR[2:, 2:] - comm(K1, K2)),
       "[X1,X2] = [[0,0],[(C1-C2)H + K1C2 - K2C1, [K1,K2]]] exactly: the "
       "bracket of two class members has ZERO base block -- it points OUT of "
       "the affine class (base coefficient 1) into its linear part")
record("T2_K_bracket_stays_triangular",
       zero(comm(K1, K2)[1, 0]),
       "[K1,K2] is again upper triangular (triangular 2x2 = solvable "
       "subalgebra): the angular chart condition is bracket-stable")
record("T2_K_bracket_nonabelian_witness",
       zero(comm(K1, K2)[0, 1]
            - (a * b2s + b * d2s - a2s * b - b2s * d)),
       "[K1,K2]_[0,1] = a*b2 + b*d2 - a2*b - b2*d: nonzero generically -- "
       "E05/E03/E02 are non-abelian strata (b-direction active)")

# L8 = R*H_ext + {lower-left C} + {triangular K} is a Lie algebra
sA, sB = sp.symbols("sA sB", real=True)
Y1 = sp.diag(sA * H, sp.zeros(2)) + classX(a, b, d, 0, s11, s12, s21, s22) \
    - classX(0, 0, 0, 0, 0, 0, 0, 0)
Y2 = sp.diag(sB * H, sp.zeros(2)) + classX(a2s, b2s, d2s, 0, u11, u12, u21, u22) \
    - classX(0, 0, 0, 0, 0, 0, 0, 0)
BR8 = comm(Y1, Y2)
record("T2_L8_is_lie_algebra",
       mzero(BR8[:2, :2]) and mzero(BR8[:2, 2:]) and zero(BR8[3, 2]),
       "the 8-dim envelope L8 = {[[s*H,0],[C,K_triangular]]} closes as a Lie "
       "algebra with the bracket's s-component = 0: class exponentials "
       "generate exp(L8), an 8-dim group, NOT the class itself")

# finite non-closure witness inside E05 (even for commuting-free diagonal K)
P1 = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(phi), 1)     # exp(phi*X_{a=1})
P2 = sp.diag(sp.exp(phi), sp.exp(-phi), 1, sp.exp(-phi))    # exp(-phi*X_{d=1})
W = sp.simplify(P2 * P1)
record("T2_nonclosure_witness_base_identity",
       mzero(W[:2, :2] - sp.eye(2)),
       "exp(-phi*X_{d=1})*exp(phi*X_{a=1}) has base block = identity exactly")
record("T2_nonclosure_witness_not_class_form",
       zero(W[2, 2] - sp.exp(phi)) and zero(W[3, 3] - sp.exp(-phi))
       and sp.solve(sp.Eq(sp.exp(-psi), 1), psi) == [0],
       "its screen block is diag(e^phi, e^-phi) != I for phi != 0, but any "
       "class element exp(psi*X) with base = I forces psi = 0 hence = I: "
       "EXACT witness that the stratum exponential sets (all strata with "
       ">= 2 members) are not closed under composition at total phi = 0")

# diagonal subfamily: abelian, closure off phi1+phi2=0 with renormalized modulus
XD1 = sp.diag(-1, 1, a, d)
XD2 = sp.diag(-1, 1, a2s, d2s)
record("T2_diagonal_subfamily_abelian",
       mzero(comm(XD1, XD2)),
       "[diag(-1,1,a1,d1), diag(-1,1,a2,d2)] = 0: the diagonal subfamily "
       "(E07 line and isotropic line included) is abelian -- zero BCH "
       "obstruction; only the affine renormalization failure remains")
abar = (phi1 * a + phi2 * a2s) / (phi1 + phi2)
dbar = (phi1 * d + phi2 * d2s) / (phi1 + phi2)
prod_diag = sp.diag(sp.exp(-(phi1 + phi2)), sp.exp(phi1 + phi2),
                    sp.exp(phi1 * a + phi2 * a2s), sp.exp(phi1 * d + phi2 * d2s))
class_diag = sp.diag(sp.exp(-(phi1 + phi2)), sp.exp(phi1 + phi2),
                     sp.exp((phi1 + phi2) * abar), sp.exp((phi1 + phi2) * dbar))
record("T2_diagonal_composition_renormalized_modulus",
       mzero(sp.simplify(prod_diag - class_diag)),
       "for phi1+phi2 != 0 the diagonal product IS class form, with modulus "
       "abar = (phi1*a1 + phi2*a2)/(phi1+phi2): a phi-weighted mean -- the "
       "composed modulus is HISTORY-DEPENDENT unless a1=a2, d1=d2")
record("T2_diagonal_modulus_shift_vanishes_iff_equal",
       sp.solve(sp.Eq(sp.simplify(abar - a) * (phi1 + phi2), 0), a2s) == [a],
       "abar - a1 = phi2*(a2-a1)/(phi1+phi2) = 0 iff a2 = a1 (phi2 != 0): a "
       "CONSTANT modulus assignment survives composition only if every "
       "segment carries the same member (J07/J11-typed requirement)")

# ===========================================================================
# T3 -- mixing cocycle
# ===========================================================================
s1c, s2c, sbar = sp.symbols("s1c s2c sbar", real=True)


def shift_g(ph, sv):
    g = sp.diag(sp.exp(-ph), sp.exp(ph), 1, 1)
    g[2, 0] = sv * (1 - sp.exp(-ph))
    return g


XC_s = classX(0, 0, 0, 0, s1c, 0, 0, 0)
G1 = shift_g(phi, s1c)
record("T3_E08_finite_form_is_exponential",
       mzero(sp.simplify(sp.diff(G1, phi) - XC_s * G1))
       and mzero(G1.subs(phi, 0) - sp.eye(4)),
       "g(phi,s): dg/dphi = X_s g, g(0) = I -- the E08 finite form IS "
       "exp(phi*X_s) by linear-ODE uniqueness (matches the banked E08 entry "
       "s*(1 - e^-phi))")
Gprod = sp.expand(shift_g(phi2, s2c) * shift_g(phi1, s1c))   # phi1 then phi2
sigma1 = s1c * (1 - sp.exp(-phi1))
sigma2 = s2c * (1 - sp.exp(-phi2))
record("T3_shift_cocycle_law",
       zero(Gprod[2, 0] - (sigma1 + sp.exp(-phi1) * sigma2)),
       "composition (phi1 then phi2, product g2*g1): the cross entry obeys "
       "sigma_tot = sigma1 + e^{-phi1}*sigma2 with sigma = s*(1-e^{-phi}) -- "
       "an exact affine 1-cocycle of the reciprocal channel valued in the "
       "weight e^{-phi} module (ax+b-type composition)")
G3 = shift_g(phi, s2c)  # third segment symbols reused safely below
ph3, s3c = sp.symbols("ph3 s3c", real=True)
Gtriple = sp.expand(shift_g(ph3, s3c) * Gprod)
sigma3 = s3c * (1 - sp.exp(-ph3))
record("T3_cocycle_associativity",
       zero(Gtriple[2, 0]
            - (sigma1 + sp.exp(-phi1) * sigma2
               + sp.exp(-phi1 - phi2) * sigma3)),
       "triple composition: sigma_123 = sigma1 + e^{-phi1} sigma2 + "
       "e^{-phi1-phi2} sigma3 -- associative, path-ordered weights")
sbar_expr = (sigma1 + sp.exp(-phi1) * sigma2) / (1 - sp.exp(-phi1 - phi2))
record("T3_class_form_recovered_off_zero_total",
       mzero(sp.simplify(Gprod - shift_g(phi1 + phi2, sbar_expr))),
       "for phi1+phi2 != 0 the product equals g(phi1+phi2, sbar) with "
       "sbar = [sigma1 + e^{-phi1} sigma2]/(1 - e^{-(phi1+phi2)}): class "
       "form survives but the shift modulus composes non-trivially")
record("T3_same_s_consistency",
       zero(sp.simplify(sbar_expr.subs(s2c, s1c) - s1c)),
       "s1 = s2 = s gives sbar = s exactly: single-member segments compose "
       "within one one-parameter subgroup, as they must")
T = sp.Symbol("T_tot", positive=True)
half = sbar_expr.subs({phi1: T / 2, phi2: T / 2})
full = s1c  # (phi1, phi2) = (T, 0) gives g2 = I, sbar = s1
hist = sp.simplify(half - full)
record("T3_history_dependence_witness",
       sp.simplify(hist - (s2c - s1c) * sp.exp(-T / 2)
                   * (1 - sp.exp(-T / 2)) / (1 - sp.exp(-T))) == 0
       or zero(hist - (s2c - s1c) * sp.exp(-T / 2)
               * (1 - sp.exp(-T / 2)) / (1 - sp.exp(-T))),
       "sbar at (T/2, T/2) minus sbar at (T, 0) = (s2-s1)*e^{-T/2}"
       "*(1-e^{-T/2})/(1-e^{-T}) != 0 unless s1=s2: the composed shift "
       "depends on the phi-HISTORY, not only on the total phi")

# general C block: finite form, cocycle, and first-order bracket
Cg = sp.Matrix([[s11, s12], [s21, s22]])
Mphi = sp.diag(1 - sp.exp(-phi), sp.exp(phi) - 1)   # H^{-1}(e^{phi H} - I)
Ff = sp.Matrix(sp.BlockMatrix([[sp.exp(phi * H), sp.zeros(2)],
                               [Cg * Mphi, sp.eye(2)]]))


def FC(ph, Cm):
    Mp = sp.diag(1 - sp.exp(-ph), sp.exp(ph) - 1)
    top = sp.diag(sp.exp(-ph), sp.exp(ph))
    return top.row_join(sp.zeros(2)).col_join((Cm * Mp).row_join(sp.eye(2)))


XCg = classX(0, 0, 0, 0, s11, s12, s21, s22)
FCg = FC(phi, Cg)
record("T3_general_C_finite_form",
       mzero(sp.simplify(sp.diff(FCg, phi) - XCg * FCg))
       and mzero(FCg.subs(phi, 0) - sp.eye(4)),
       "exp(phi*[[H,0],[C,0]]) = [[e^{phi H},0],[C*M(phi), I]] with "
       "M(phi) = diag(1-e^{-phi}, e^{phi}-1) exactly (E08 is its s11 axis)")
Cu = sp.Matrix([[u11, u12], [u21, u22]])
prodC = sp.expand(FC(phi2, Cu) * FC(phi1, Cg))
M1 = sp.diag(1 - sp.exp(-phi1), sp.exp(phi1) - 1)
M2 = sp.diag(1 - sp.exp(-phi2), sp.exp(phi2) - 1)
E1 = sp.diag(sp.exp(-phi1), sp.exp(phi1))
record("T3_general_C_cocycle",
       mzero(sp.simplify(prodC[2:, :2] - (Cu * M2 * E1 + Cg * M1))),
       "lower-left of the composition = C2*M(phi2)*e^{phi1 H} + C1*M(phi1): "
       "the full mixing block composes by the same path-ordered affine "
       "cocycle, channel-weighted by e^{-phi1} (clock leg) and e^{+phi1} "
       "(ruler leg)")
record("T3_M_invertible_iff_phi_nonzero",
       sp.solve(sp.Eq((1 - sp.exp(-phi)) * (sp.exp(phi) - 1), 0), phi) == [0],
       "det M(phi) = (1-e^{-phi})(e^{phi}-1) = 0 iff phi = 0: off total "
       "phi = 0 the composed Cbar = [C2 M(phi2) e^{phi1 H} + C1 M(phi1)]"
       "*M(phi1+phi2)^{-1} exists uniquely (class form with history-"
       "dependent mixing modulus)")
resid0 = sp.simplify((Cu * M2 * E1 + Cg * M1).subs(phi2, -phi1)
                     - (Cg - Cu) * M1)
record("T3_zero_total_residual_C1_minus_C2",
       mzero(resid0),
       "at phi2 = -phi1 the residual lower-left is (C1 - C2)*M(phi1): "
       "nonzero unless C1 = C2 -- the finite E04-family witness of "
       "non-closure at total phi = 0")
XC1 = classX(0, 0, 0, 0, s11, s12, s21, s22)
XC2 = classX(0, 0, 0, 0, u11, u12, u21, u22)
BC = comm(XC1, XC2)
record("T3_first_order_C_bracket",
       mzero(BC[2:, :2] - (Cg - Cu) * H) and mzero(BC[2:, 2:])
       and mzero(BC[:2, :2]) and mzero(BC[:2, 2:]),
       "[X_C1, X_C2] = [[0,0],[(C1-C2)H, 0]] exactly: two mixing directions "
       "fail to commute at first order iff C1 != C2, the infinitesimal seed "
       "of the finite cocycle (H invertible => (C1-C2)H = 0 iff C1 = C2)")

# ===========================================================================
# T4 -- transverse-seat map: the diagonal (a,d) plane
# ===========================================================================
Xdiag = sp.diag(-1, 1, a, d)
Lam_d = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(a * phi), sp.exp(d * phi))
record("T4_diagonal_finite_form",
       mzero(sp.simplify(sp.diff(Lam_d, phi) - Xdiag * Lam_d))
       and mzero(Lam_d.subs(phi, 0) - sp.eye(4)),
       "exp(phi*diag(-1,1,a,d)) = diag(e^{-phi}, e^{phi}, e^{a phi}, "
       "e^{d phi})")
calib = sp.diag(c, 1, 1, 1) * Lam_d
gmet = sp.simplify(calib.T * eta * calib)
record("T4_metric_readout",
       mzero(gmet - sp.diag(-c**2 * sp.exp(-2 * phi), sp.exp(2 * phi),
                            sp.exp(2 * a * phi), sp.exp(2 * d * phi))),
       "physical metric diag(-c^2 e^{-2phi}, e^{2phi}, e^{2a phi}, "
       "e^{2d phi}): a generator entry m on a coframe slot gives metric "
       "factor e^{2m phi} -- sign convention CHECKED against the banked E07 "
       "record (a=-k, d=+k gives diag(e^{-2k phi}, e^{+2k phi}))")
record("T4_E07_sign_check",
       mzero(gmet.subs({a: -kq, d: kq})[2:, 2:]
             - sp.diag(sp.exp(-2 * kq * phi), sp.exp(2 * kq * phi))),
       "E07 screen metric reproduced exactly from the general readout")
detg = sp.simplify(gmet.det())
record("T4_4d_volume_exponent_a_plus_d",
       zero(detg + c**2 * sp.exp(2 * (a + d) * phi)),
       "det g = -c^2 e^{2(a+d)phi}: sqrt|det g| = c*e^{(a+d)phi} -- the "
       "NATIVE 4D chart volume exponent is a + d; the base pair contributes "
       "(-1) + (+1) = 0 exactly")
record("T4_det_one_line",
       zero(sp.simplify(Lam_d.det() - sp.exp((a + d) * phi)))
       and zero(sp.trace(Xdiag) - (a + d)),
       "det exp(phi X) = e^{(a+d)phi} and tr X = a + d (ledger E03 fact): "
       "the det-one line is a + d = 0")
record("T4_three_name_coincidence",
       zero((a + d).subs({a: -kq, d: kq}))
       and sp.solve(sp.Eq(a + d, 0), d) == [-a],
       "the E07 line (a,d) = (-k,+k), the det-one line a+d=0, and the 4D "
       "chart volume-blind locus a+d=0 are ONE line (the anti-diagonal of "
       "the (a,d) plane)")
lam_coord = (a + d) / 2
k_coord = (d - a) / 2
record("T4_lambda_k_coordinates",
       zero(sp.simplify(a - (lam_coord - k_coord)))
       and zero(sp.simplify(d - (lam_coord + k_coord)))
       and zero(lam_coord.subs({a: -kq, d: kq}))
       and zero(sp.simplify(k_coord.subs({a: -kq, d: kq}) - kq))
       and zero(sp.simplify(lam_coord.subs({a: lamq, d: lamq}) - lamq))
       and zero(k_coord.subs({a: lamq, d: lamq})),
       "(a,d) = (lambda-k, lambda+k) with lambda = (a+d)/2, k = (d-a)/2: the "
       "isotropic seat and the E07 seat are the two ORTHOGONAL axes of the "
       "diagonal plane, meeting only at the spectator origin -- the MAP's "
       "seat equation 'E07 k = joint-audit lambda' is resolved as a "
       "DECOMPOSITION, not an identity")
record("T4_isotropic_4d_exponent_2lambda",
       zero((a + d).subs({a: lamq, d: lamq}) - 2 * lamq),
       "on the isotropic line the 4D chart volume exponent is 2*lambda "
       "(blind at lambda = 0, the spectator)")
record("T4_orbit_exponent_reconciliation",
       zero((2 * lamq + 1) - (lamq + lamq + 1))
       and sp.solve(sp.Eq(2 * lamq + 1, 0), lamq) == [sp.Rational(-1, 2)],
       "the CITED 3D orbit-volume exponent 1+2*lambda (rank-closure audit "
       "07-27) = two screen legs at lambda plus ONE fibre leg at ruler "
       "weight +1; blind at lambda = -1/2.  It is a DIFFERENT functional on "
       "a DIFFERENT space (S3 orbit of the stationary branch) from the 4D "
       "chart volume (exponent a+d, clock and ruler cancelling): the two "
       "blind loci (a+d=0 vs lambda=-1/2) must NOT be conflated; the "
       "lambda=-1/2 pin translates to the (a,d) plane ONLY as the point "
       "(-1/2,-1/2) on the isotropic line, scope-stamped to that branch")
record("T4_conditional_pins_on_isotropic_line",
       all(zero(k_coord.subs({a: v, d: v})) for v in (1, -1, 0)),
       "the three CITED conditional pins -- SO(3)->(+1,+1), "
       "SO+(1,2)->(-1,-1), swap->(0,0) (07-27/07-28 audits) -- all lie on "
       "the isotropic axis k=0; no banked gate pins any point with k != 0")

# ===========================================================================
# Summary
# ===========================================================================
n_pass = sum(1 for cchk in checks if cchk["pass"])
n_fail = len(checks) - n_pass
all_pass = n_fail == 0
summary = {
    "package": "udt_p4_routeB_extension_selection_2026-07-28",
    "script": "derive_routeB_stage1.py",
    "date": "2026-07-28",
    "sympy_version": sp.__version__,
    "conventions": ("coframe column e, extension acts e -> exp(phi X) e "
                    "(left); gauge e -> L e; induced action X -> L X L^{-1}, "
                    "delta X = [lam, X]; composition 'phi1 then phi2' = "
                    "g2*g1; gauge basis (B01,B02,B03,R12,R13,R23); "
                    "eta = diag(-1,1,1,1)"),
    "check_count": len(checks),
    "checks": checks,
    "headline_structure": {
        "T1": ("strata are SPLIT-RELATIVE: full so(1,3) preserves only the "
               "trace (det-one) condition; the base/angular split is "
               "preserved by so(1,1)+so(2) (dim 2); fixed founded H cuts to "
               "so(2) (dim 1); the triangular chart cuts to {0}; the "
               "so(2)-fixed set inside the class is exactly the isotropic "
               "line; so(2)-invariant content of K is (tr, det, antisym)"),
        "T2": ("no stratum with >= 2 members closes under composition at "
               "total phi = 0 (exact witness); off that locus composition "
               "closes with HISTORY-DEPENDENT moduli (phi-weighted mean in "
               "the abelian diagonal subfamily; BCH/cocycle in the "
               "non-abelian strata); class exponentials generate the 8-dim "
               "exp(L8)"),
        "T3": ("mixing shift is an exact affine 1-cocycle: sigma_tot = "
               "sigma1 + e^{-phi1} sigma2 (channel-weighted, path-ordered, "
               "associative); class form recoverable off total phi = 0 with "
               "history-dependent sbar; first-order seed [X_C1,X_C2] = "
               "[[0,0],[(C1-C2)H,0]]"),
        "T4": ("(a,d) = (lambda-k, lambda+k); E07 line = det-one line = 4D "
               "volume-blind line (one anti-diagonal); isotropic line = "
               "so(2)-fixed axis carrying all three conditional pins "
               "(+1/-1/0) and the branch-scoped orbit-volume-blind point "
               "(-1/2,-1/2); 4D chart volume exponent = a+d (derived "
               "natively), distinct from the cited 3D orbit exponent "
               "1+2*lambda"),
    },
    "all_pass": bool(all_pass),
    "falsifier_FC_fired": bool(not all_pass),
}
with open(os.path.join(HERE, "DERIVATION_RESULT.json"), "w") as fh:
    json.dump(summary, fh, indent=2)
print()
print(json.dumps(summary, indent=2))
sys.exit(0 if all_pass else 1)
