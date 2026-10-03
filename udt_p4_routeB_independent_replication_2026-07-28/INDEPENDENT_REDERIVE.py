#!/usr/bin/env python3
"""BLIND-VERIFIER INDEPENDENT REDERIVATION -- P4 Route B Stage 1.

Written WITHOUT importing or copying derive_routeB_stage1.py internals.

MY OWN SETUP (stated per duty 2a):
  * eta = diag(-1,1,1,1); slots (clock, ruler, screen1, screen2) = (0,1,2,3).
  * MY so(1,3) basis: the standard covariant generators
        (M_ab)^mu_nu = delta^mu_a * eta_b:nu - delta^mu_b * eta_a:nu,
    for (a,b) in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)] -- constructed from the
    defining formula, NOT copied from the production basis (E-matrix sums).
  * Action: the registered chart presents the coframe as a COLUMN e of 4
    one-forms; the extension acts pointwise algebraically e -> exp(phi X) e
    (left), a gauge change acts e -> L e (left).  Then the same physical
    extension in the new gauge is FORCED (no choice, no inhomogeneous term,
    because the extension map contains no derivative of L):
        L exp(phi X) e = [L exp(phi X) L^{-1}] (L e) = exp(phi L X L^{-1}) e',
    so X -> L X L^{-1}, infinitesimally delta X = [lam, X].  I verify below
    that my basis spans the SAME 6-dim algebra as the production's, i.e. the
    two scripts compute the same action (duty 2a sameness check).
  * Composition: segment 1 then segment 2 under left action is g2*g1.
Every check is exact (sympy, zero residual).  Exit 0 iff all pass.
"""
import sys

import sympy as sp

ph, ph1, ph2, ph3 = sp.symbols("ph ph1 ph2 ph3", real=True)
Ttot = sp.Symbol("Ttot", positive=True)
A, B, D, K21 = sp.symbols("A B D K21", real=True)
c11, c12, c21, c22 = sp.symbols("c11 c12 c21 c22", real=True)
w11, w12, w21, w22 = sp.symbols("w11 w12 w21 w22", real=True)
A2, B2, D2 = sp.symbols("A2 B2 D2", real=True)
lam, kk = sp.symbols("lam kk", real=True)
cc = sp.Symbol("cc", positive=True)
s1v, s2v, s3v = sp.symbols("s1v s2v s3v", real=True)
g6 = list(sp.symbols("g0:6", real=True))

eta = sp.diag(-1, 1, 1, 1)
eta2 = sp.diag(-1, 1)
H = sp.diag(-1, 1)

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def Mgen(ia, ib):
    M = sp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            M[mu, nu] = (sp.Integer(1) if mu == ia else 0) * eta[ib, nu] \
                - (sp.Integer(1) if mu == ib else 0) * eta[ia, nu]
    return M


GEN = [Mgen(*p) for p in PAIRS]
LAMG = sum((gi * Mi for gi, Mi in zip(g6, GEN)), sp.zeros(4))

FAILS = []


def check(name, ok, note=""):
    ok = bool(ok)
    print(("PASS" if ok else "FAIL"), name, ("-- " + note) if note else "")
    if not ok:
        FAILS.append(name)


def z(e):
    return sp.simplify(sp.expand(e)) == 0


def mz(M):
    return all(z(x) for x in M)


def blockX(K, C):
    return H.row_join(sp.zeros(2)).col_join(C.row_join(K))


Kfull = sp.Matrix([[A, B], [K21, D]])
Ktri = sp.Matrix([[A, B], [0, D]])
Cgen = sp.Matrix([[c11, c12], [c21, c22]])
Cgen2 = sp.Matrix([[w11, w12], [w21, w22]])
XF = blockX(Kfull, Cgen)
XT = blockX(Ktri, Cgen)


def stab_nullspace(X, xpars, positions):
    """Gauge directions whose commutator with X vanishes at the given entry
    positions identically in xpars.  My own construction."""
    AD = sp.expand(LAMG * X - X * LAMG)
    eqs = []
    for (i, j) in positions:
        e = sp.expand(AD[i, j])
        if xpars:
            eqs.extend(sp.Poly(e, *xpars).coeffs())
        else:
            eqs.append(e)
    rows = []
    for e in eqs:
        row = [sp.expand(sp.diff(e, gi)) for gi in g6]
        # linearity guard
        if not z(e - sum(r * gi for r, gi in zip(row, g6))):
            raise RuntimeError("nonlinear gauge equation")
        rows.append(row)
    M = sp.Matrix(rows) if rows else sp.zeros(1, 6)
    return M.nullspace()


def span_eq(ns, cols):
    if len(ns) != len(cols):
        return False
    if not ns:
        return True
    Am = sp.Matrix.hstack(*ns)
    Bm = sp.Matrix.hstack(*cols)
    return (Am.rank() == len(ns) and Bm.rank() == len(cols)
            and sp.Matrix.hstack(Am, Bm).rank() == len(ns))


def e6(i):
    v = sp.zeros(6, 1)
    v[i] = 1
    return v


# ---- A. setup validity and SAMENESS with the production action -------------
check("A1_my_basis_in_so13",
      all(mz(M.T * eta + eta * M) for M in GEN),
      "all 6 M_ab satisfy lam^T eta + eta lam = 0")
myspan = sp.Matrix.hstack(*(M.reshape(16, 1) for M in GEN))
check("A1_rank6", myspan.rank() == 6)
# production basis, reconstructed from its stated definition only:
prod = [sp.zeros(4) for _ in range(6)]
for idx, (i, j, s) in enumerate([(0, 1, 1), (0, 2, 1), (0, 3, 1),
                                 (1, 2, -1), (1, 3, -1), (2, 3, -1)]):
    m = sp.zeros(4)
    m[i, j] = 1
    m[j, i] = s
    prod[idx] = m
prodspan = sp.Matrix.hstack(*(M.reshape(16, 1) for M in prod))
check("A2_same_algebra_as_production",
      sp.Matrix.hstack(myspan, prodspan).rank() == 6,
      "my basis and the production basis span the SAME so(1,3); same "
      "defining-representation adjoint action")

# ---- B. stabilizer chain (duty 2a) -----------------------------------------
UR = [(i, j) for i in range(2) for j in range(2, 4)]
BASEB = [(i, j) for i in range(2) for j in range(2)]
LL = [(i, j) for i in range(2, 4) for j in range(2)]
SCR = [(i, j) for i in range(2, 4) for j in range(2, 4)]

xpF = (A, B, D, K21, c11, c12, c21, c22)
ns = stab_nullspace(XF, xpF, UR)
check("B1_split_stabilizer_dim2",
      len(ns) == 2 and span_eq(ns, [e6(0), e6(5)]),
      "upper-right-zero preserved exactly by span(M01, M23): dim 2")
check("B1_direct_sum", mz(GEN[0] * GEN[5] - GEN[5] * GEN[0]),
      "[M01, M23] = 0: so(1,1) + so(2) direct sum")
ns = stab_nullspace(XF, xpF, UR + BASEB)
check("B2_fixedH_stabilizer_dim1",
      len(ns) == 1 and span_eq(ns, [e6(5)]),
      "adding fixed H cuts to span(M23): dim 1")
ns = stab_nullspace(XT, (A, B, D, c11, c12, c21, c22), UR + BASEB + [(3, 2)])
check("B3_triangular_stabilizer_dim0", len(ns) == 0,
      "adding K[1,0]=0 cuts to {0}: the triangular chart is a gauge section")
obstr = sp.expand((GEN[5] * XT - XT * GEN[5])[3, 2])
check("B3_obstruction_entry", z(obstr - (D - A)),
      "[M23, X]_[3,2] = d - a (adjudicates the production sign d-a: CORRECT "
      "for R23 = E23 - E32)")
# trace + other spectral invariants (F-D probe on 'unique covariant condition')
Xany = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"x{i}{j}"))
check("B4_trace_invariant_any_X",
      z(sp.trace(LAMG * Xany - Xany * LAMG)),
      "tr[lam, X] = 0 for ANY X: det-one condition fully covariant")
t = sp.Symbol("t")
ADF = LAMG * XF - XF * LAMG
check("B4_det_also_invariant",
      z(sp.diff((XF + t * ADF).det(), t).subs(t, 0)),
      "delta(det X) = 0 too: det X = -a*d is ANOTHER fully covariant function "
      "on the class -- 'unique stratum condition' must be quantified over the "
      "package's OWN stratum/chart condition list (F-D note), where it holds")
# per-stratum stabilizers
ns = stab_nullspace(blockX(sp.zeros(2), Cgen), (c11, c12, c21, c22),
                    UR + BASEB + SCR)
check("B5_E04_dim1", len(ns) == 1 and span_eq(ns, [e6(5)]))
ns = stab_nullspace(blockX(Kfull, sp.zeros(2)), (A, B, D, K21),
                    UR + BASEB + LL)
check("B5_E05_fullK_dim1", len(ns) == 1 and span_eq(ns, [e6(5)]))
ns = stab_nullspace(blockX(Ktri, sp.zeros(2)), (A, B, D),
                    UR + BASEB + LL + [(3, 2)])
check("B5_E05_triangular_dim0", len(ns) == 0)
ns = stab_nullspace(blockX(sp.zeros(2), sp.zeros(2)), (),
                    [(i, j) for i in range(4) for j in range(4)])
check("B5_E06_dim1", len(ns) == 1 and span_eq(ns, [e6(5)]))
# so(2)-fixed sets: triangular vs chart-free (scope probe)
sol = sp.solve(list(GEN[5] * XT - XT * GEN[5]),
               [A, B, D, c11, c12, c21, c22], dict=True)
check("B6_so2_fixed_set_triangular_is_isotropic_line",
      len(sol) == 1 and sol[0].get(B) == 0 and sol[0].get(A) == D
      and all(sol[0].get(s) == 0 for s in (c11, c12, c21, c22)),
      "[M23,X]=0 in the TRIANGULAR class iff b=0, C=0, a=d")
sol = sp.solve(list(GEN[5] * XF - XF * GEN[5]),
               [A, B, D, K21, c11, c12, c21, c22], dict=True)
# shape-robust: substitute the solution back and verify the residual ideal
# is exactly {a-d, b+k21, C}: two free moduli remain
fixed_full_dim2 = False
if len(sol) == 1:
    sub = sol[0]
    onset = all(z(e.subs(sub)) for e in (A - D, B + K21, c11, c12, c21, c22))
    freedims = len({A, B, D, K21} - set(sub.keys()))
    fixed_full_dim2 = onset and freedims == 2 \
        and all(sub.get(s) == 0 for s in (c11, c12, c21, c22))
check("B6_so2_fixed_set_chartfree_is_bigger", fixed_full_dim2,
      "in the CHART-FREE full-K class the so(2)-fixed set is {a=d, k21=-b, "
      "C=0}: 2 moduli (lambda, rotation) -- the 'isotropic line' fixed-set "
      "statement is triangular-chart-scoped (verifier scope note)")
# centralizer dims of X_lambda
XL = sp.diag(-1, 1, lam, lam)
ns = stab_nullspace(XL, (lam,), [(i, j) for i in range(4) for j in range(4)])
check("B7_centralizer_generic_dim1", len(ns) == 1)
dims = []
for v in (1, -1, 0):
    nsv = stab_nullspace(XL.subs(lam, v), (),
                         [(i, j) for i in range(4) for j in range(4)])
    dims.append(len(nsv))
check("B7_centralizer_dims_3_3_1", dims == [3, 3, 1],
      "lambda=+1: 3, lambda=-1: 3, lambda=0: 1 -- matches the cited 1/3/3/1")
# E07 sign is chart gauge
R90 = sp.Matrix([[0, -1], [1, 0]])
check("B8_e07_sign_chart",
      mz(R90 * sp.diag(-kk, kk) * R90.T - sp.diag(kk, -kk)),
      "pi/2 screen rotation flips the sign of k; invariant is |k|")

# ---- C. cocycle (duty 2b) --------------------------------------------------
tt = sp.Symbol("tt", real=True)
Mphi = sp.integrate(sp.exp(tt * H[0, 0]), (tt, 0, ph)), \
    sp.integrate(sp.exp(tt * H[1, 1]), (tt, 0, ph))
Mphi = sp.diag(Mphi[0], Mphi[1])   # my own derivation: integral of e^{tH}
check("C1_M_by_integration",
      mz(Mphi - sp.diag(1 - sp.exp(-ph), sp.exp(ph) - 1)),
      "M(phi) = int_0^phi e^{tH} dt = diag(1-e^{-phi}, e^{phi}-1)")


def myexp(phv, Cm):
    Mp = sp.diag(1 - sp.exp(-phv), sp.exp(phv) - 1)
    return sp.diag(sp.exp(-phv), sp.exp(phv)).row_join(sp.zeros(2)) \
        .col_join((Cm * Mp).row_join(sp.eye(2)))


NC = blockX(sp.zeros(2), Cgen)
FF = myexp(ph, Cgen)
check("C2_closed_form_solves_ODE",
      mz(sp.simplify(sp.diff(FF, ph) - NC * FF))
      and mz(FF.subs(ph, 0) - sp.eye(4)),
      "F' = X_C F, F(0) = I: closed form is exp(phi X_C) by uniqueness")
Cnum = sp.Matrix([[2, 3], [5, 7]])
spot = sp.simplify((sp.Rational(1, 1) * blockX(sp.zeros(2), Cnum)).exp()
                   - myexp(1, Cnum))
check("C2_matrix_exp_spot_check", mz(spot),
      "sympy 4x4 .exp() at phi=1, C=[[2,3],[5,7]] agrees exactly")
# two-segment composition, my own multiply (phi1 then phi2 = g2*g1)
prod2 = sp.expand(myexp(ph2, Cgen2) * myexp(ph1, Cgen))
law = Cgen2 * sp.diag(1 - sp.exp(-ph2), sp.exp(ph2) - 1) \
    * sp.diag(sp.exp(-ph1), sp.exp(ph1)) \
    + Cgen * sp.diag(1 - sp.exp(-ph1), sp.exp(ph1) - 1)
check("C3_full_C_cocycle",
      mz(sp.simplify(prod2[2:, :2] - law)),
      "lower-left = C2 M(phi2) e^{phi1 H} + C1 M(phi1): CONFIRMED")
sig1 = s1v * (1 - sp.exp(-ph1))
sig2 = s2v * (1 - sp.exp(-ph2))
e08prod = sp.expand(myexp(ph2, sp.diag(s2v, 0) * sp.Matrix([[1, 0], [0, 0]]))
                    * 0)  # placeholder guard, not used
G1 = myexp(ph1, sp.Matrix([[s1v, 0], [0, 0]]))
G2 = myexp(ph2, sp.Matrix([[s2v, 0], [0, 0]]))
Gp = sp.expand(G2 * G1)
check("C4_E08_sigma_law",
      z(sp.simplify(Gp[2, 0] - (sig1 + sp.exp(-ph1) * sig2))),
      "sigma_tot = sigma1 + e^{-phi1} sigma2: CONFIRMED (clock-channel "
      "weight e^{-phi1})")
G3 = myexp(ph3, sp.Matrix([[s3v, 0], [0, 0]]))
Gt = sp.expand(G3 * Gp)
sig3 = s3v * (1 - sp.exp(-ph3))
check("C4_associative_path_ordered",
      z(sp.simplify(Gt[2, 0] - (sig1 + sp.exp(-ph1) * sig2
                                + sp.exp(-ph1 - ph2) * sig3))))
sbar = (sig1 + sp.exp(-ph1) * sig2) / (1 - sp.exp(-(ph1 + ph2)))
hist = sp.simplify(sbar.subs({ph1: Ttot / 2, ph2: Ttot / 2}) - s1v)
claimed = (s2v - s1v) * sp.exp(-Ttot / 2) * (1 - sp.exp(-Ttot / 2)) \
    / (1 - sp.exp(-Ttot))
check("C5_history_dependence_witness",
      z(sp.simplify(hist - claimed))
      and sp.simplify(claimed.subs({s1v: 0, s2v: 1, Ttot: sp.log(4)})) != 0,
      "sbar(T/2,T/2) - sbar(T,0) = (s2-s1) e^{-T/2}(1-e^{-T/2})/(1-e^{-T}), "
      "nonzero at exact witness point: history dependence CONFIRMED")

# ---- D. T4 plane facts (duty 2c), SOURCE-package metric convention ---------
Ld = sp.diag(sp.exp(-ph), sp.exp(ph), sp.exp(A * ph), sp.exp(D * ph))
check("D1_diagonal_finite_form",
      mz(sp.simplify(sp.diff(Ld, ph) - sp.diag(-1, 1, A, D) * Ld))
      and mz(Ld.subs(ph, 0) - sp.eye(4)))
gmet = sp.simplify((sp.diag(cc, 1, 1, 1) * Ld).T * eta
                   * (sp.diag(cc, 1, 1, 1) * Ld))
check("D2_metric_readout_source_convention",
      mz(gmet - sp.diag(-cc**2 * sp.exp(-2 * ph), sp.exp(2 * ph),
                        sp.exp(2 * A * ph), sp.exp(2 * D * ph))),
      "g = (diag(c,1,1,1) Lambda)^T eta (diag(c,1,1,1) Lambda): entry m -> "
      "e^{2m phi}; matches the 07-25 source spectator readout convention")
check("D2_E07_record_reproduced",
      mz(gmet.subs({A: -kk, D: kk})[2:, 2:]
         - sp.diag(sp.exp(-2 * kk * ph), sp.exp(2 * kk * ph))),
      "(a,d)=(-k,+k) gives screen metric diag(e^{-2k phi}, e^{+2k phi}) = "
      "the banked E07 record, signs included")
sqg = sp.simplify(sp.sqrt(-gmet.det()))
check("D3_volume_exponent_a_plus_d",
      z(sp.simplify(sqg - cc * sp.exp((A + D) * ph))),
      "sqrt|det g| = c e^{(a+d)phi}: 4D chart volume exponent a+d; base "
      "pair contributes (-1)+(+1)=0")
check("D3_blind_iff_antidiagonal",
      sp.solve(sp.Eq(sp.diff(sqg, ph), 0), A) == [-D],
      "phi-independent iff a+d=0 exactly")
lamc, kc = (A + D) / 2, (D - A) / 2
check("D4_axes_change",
      z(A - (lamc - kc)) and z(D - (lamc + kc))
      and z(lamc.subs({A: -kk, D: kk}))
      and z(sp.simplify(kc.subs({A: -kk, D: kk}) - kk))
      and z(kc.subs({A: lam, D: lam}))
      and z(sp.simplify(lamc.subs({A: lam, D: lam}) - lam)),
      "(a,d) = (lambda-k, lambda+k); E07 seat and isotropic seat are "
      "orthogonal axes: DECOMPOSITION confirmed")
check("D5_three_name_coincidence",
      z((A + D).subs({A: -kk, D: kk}))
      and sp.solve(sp.Eq(A + D, 0), D) == [-A]
      and z(sp.simplify(Ld.det() - sp.exp((A + D) * ph)))
      and sp.trace(sp.diag(-1, 1, A, D)) == A + D,
      "E07 line {(-k,+k)} = {a+d=0} (surjective parametrization) = det-one "
      "line (tr X = a+d) = 4D volume-blind line: three names, one line")
check("D6_orbit_vs_chart_functionals_distinct",
      sp.solve(sp.Eq(1 + 2 * lam, 0), lam) == [sp.Rational(-1, 2)]
      and sp.solve(sp.Eq(2 * lam, 0), lam) == [0]
      and not z((1 + 2 * lam) - 2 * lam),
      "1+2lambda (cited 3D orbit exponent) and 2lambda (4D chart exponent "
      "on the isotropic line) are distinct functionals with distinct blind "
      "loci (-1/2 vs 0): conflation would be an error; package keeps them "
      "separate")
check("D7_banked_pins_on_k_zero_axis",
      all(z(kc.subs({A: v, D: v})) for v in (1, -1, 0)),
      "(1,1), (-1,-1), (0,0) all have k=0; NOTE: the truthful strong claim "
      "is only 'no banked gate pins k != 0' -- banked supplied gates DO "
      "constrain k conditionally (they force k=0): see verifier report")

# ---- E. spot checks of other production claims (duty 2d) -------------------
X1 = blockX(Ktri, Cgen)
X2 = blockX(sp.Matrix([[A2, B2], [0, D2]]), Cgen2)
BR = sp.expand(X1 * X2 - X2 * X1)
K2m = sp.Matrix([[A2, B2], [0, D2]])
check("E1_bracket_block_formula",
      mz(BR[:2, :2]) and mz(BR[:2, 2:])
      and mz(BR[2:, :2] - ((Cgen - Cgen2) * H + Ktri * Cgen2 - K2m * Cgen))
      and mz(BR[2:, 2:] - (Ktri * K2m - K2m * Ktri))
      and z(sp.expand((Ktri * K2m - K2m * Ktri)[1, 0])),
      "[X1,X2] block formula and triangular bracket-stability: CONFIRMED")
sA, sB = sp.symbols("sA sB", real=True)
Y1 = sp.diag(sA * H, sp.zeros(2)) + blockX(Ktri, Cgen) - blockX(sp.zeros(2), sp.zeros(2))
Y2 = sp.diag(sB * H, sp.zeros(2)) + blockX(K2m, Cgen2) - blockX(sp.zeros(2), sp.zeros(2))
BR8 = sp.expand(Y1 * Y2 - Y2 * Y1)
check("E2_L8_closes",
      mz(BR8[:2, :2]) and mz(BR8[:2, 2:]) and z(BR8[3, 2]),
      "L8 = {[[sH,0],[C,K_tri]]} closes as a Lie algebra: CONFIRMED")
W = sp.simplify(sp.diag(sp.exp(ph), sp.exp(-ph), 1, sp.exp(-ph))
                * sp.diag(sp.exp(-ph), sp.exp(ph), sp.exp(ph), 1))
check("E3_nonclosure_witness_E05",
      mz(W[:2, :2] - sp.eye(2)) and z(W[2, 2] - sp.exp(ph))
      and sp.solve(sp.Eq(sp.exp(-s1v), 1), s1v) == [0],
      "base = I, screen != I; class element with base I is I: total-phi=0 "
      "non-closure CONFIRMED")
W3 = sp.simplify(sp.diag(sp.exp(ph), sp.exp(-ph), sp.exp(ph), sp.exp(-ph))
                 * sp.diag(sp.exp(-ph), sp.exp(ph), sp.exp(ph), sp.exp(-ph)))
check("E3_E03_internal_witness",
      mz(W3[:2, :2] - sp.eye(2)) and z(W3[2, 2] - sp.exp(2 * ph)),
      "det-one members (a,d)=(1,-1) and (-1,1): exp(-phi X2) exp(phi X1) = "
      "diag(1,1,e^{2phi},e^{-2phi}) -- an E03-INTERNAL witness exists "
      "(repairs the garbled TSV E03/C2 parenthetical)")
abar = (ph1 * A + ph2 * A2) / (ph1 + ph2)
lhs = sp.exp(ph2 * A2) * sp.exp(ph1 * A)
check("E4_diagonal_weighted_mean_modulus",
      z(sp.simplify(lhs - sp.exp((ph1 + ph2) * abar)))
      and mz(sp.expand(sp.diag(-1, 1, A, D) * sp.diag(-1, 1, A2, D2)
                       - sp.diag(-1, 1, A2, D2) * sp.diag(-1, 1, A, D))),
      "diagonal subfamily abelian; composed modulus = phi-weighted mean: "
      "CONFIRMED")
check("E5_detM_zero_iff_phi_zero",
      sp.solve(sp.Eq((1 - sp.exp(-ph)) * (sp.exp(ph) - 1), 0), ph) == [0],
      "det M(phi) = 0 iff phi = 0: CONFIRMED")
Gs = sp.diag(sp.exp(-ph), sp.exp(ph), 1, 1)
Gs[2, 0] = s1v * (1 - sp.exp(-ph))
XCs = blockX(sp.zeros(2), sp.Matrix([[s1v, 0], [0, 0]]))
check("E6_E08_finite_form",
      mz(sp.simplify(sp.diff(Gs, ph) - XCs * Gs))
      and mz(Gs.subs(ph, 0) - sp.eye(4)),
      "banked E08 finite form s(1-e^{-phi}) IS exp(phi X_s): CONFIRMED")
bra = sp.Matrix.hstack(*((GEN[i] * GEN[j] - GEN[j] * GEN[i]).reshape(16, 1)
                         for i in range(6) for j in range(i + 1, 6)))
check("E7_so13_perfect", bra.rank() == 6,
      "bracket span rank 6: perfectness cross-check CONFIRMED")

print()
print("INDEPENDENT REDERIVATION:", "ALL PASS" if not FAILS else
      f"FAILURES: {FAILS}")
sys.exit(0 if not FAILS else 1)
