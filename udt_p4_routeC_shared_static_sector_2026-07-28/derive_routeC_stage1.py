#!/usr/bin/env python3
"""P4 Route C Stage 1 — shared exact static sector comparison (TC1-TC6).

Contract: udt_p4_routeC_shared_static_sector_2026-07-28/PREREGISTRATION.md (frozen first).

Compares, on the declared CHOSE comparison domain (the registered stationary family
g = -u(c_E dt + alpha A)^2 + u^{-1} A^2 + q_B with A = dz + f(x) dy,
q_B = e^{2 lambda phi}(dx^2 + bh(x) dy^2), u = e^{-2 phi(x)}, in the local toric chart
of the R x T^2 stratum, which locally contains the R_t x S^3 Hopf members),
the FULL field equations of the two CONDITIONAL candidate actions:

  C2/Bach side  [stamp: UNIQUE_CONDITIONAL_ONLY_IF_STRONG_CSN_RETAINED; strong CSN is
                 CHALLENGED_OWNER_POSTULATE_NOT_DERIVED (G04/G10) - INACTIVE branch]:
     unrestricted metric variation of sqrt|g| C_abcd C^abcd -> equation proportional to
     the Bach tensor  B_ab = nabla^c nabla^d C_acbd + (1/2) R^cd C_acbd
     (banked: c2_finite_cell_boundary_variation_2026-07-20/AUDIT_REPORT.md, "The
     unrestricted bulk equation is proportional to the Bach tensor").  The nonzero
     convention constant does not change the vanishing locus.

  EH+Lambda side [stamp: CONDITIONAL_NOT_SELECTED (G11); EH-H3 spatial-infinity
                 normalization NOT used]:
     unrestricted metric variation of sqrt|g| (R - 2 Lambda) -> equation proportional to
     E_ab = G_ab + Lambda g_ab,  G_ab = R_ab - (1/2) R g_ab,  Lambda symbolic.

ORDER: full unrestricted variational output (the covariant tensor) FIRST, THEN
restriction to the domain by componentwise evaluation on the ansatz.  No equation here
is obtained by varying a pre-restricted action (F-C1 respected by construction).

Falsifiers respected: F-C1..F-C6 (see PREREGISTRATION.md).  All components including
the lapse/momentum ("constraint") rows tt, ty, tz enter the comparison (F-C2).
Every check is an exact zero-residual SymPy assertion; any failure exits nonzero with
the failure recorded (F-C3).  Pure CPU, single process, deterministic.

Outputs: routeC_stage1_results.json, SECTOR_COMPARISON_LEDGER.tsv,
BACH_ODE_SYSTEM_FULL.txt, EH_ODE_SYSTEM_FULL.txt, stdout check summary.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
T0 = time.time()

STAMPS = {
    "domain": "CHOSE (registered stationary family + R x T^2 stratum, local toric chart; "
              "transverse gauge g_xx = e^{2 lambda phi} is a coordinate gauge, Category-A)",
    "c2_side": "UNIQUE_CONDITIONAL_ONLY_IF_STRONG_CSN_RETAINED; strong CSN "
               "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED (G04/G10); INACTIVE without Charles reauthorization",
    "eh_side": "CONDITIONAL_NOT_SELECTED (G11); EH-H3 spatial-infinity normalization "
               "INADMISSIBLE for native finite cells and NOT used",
    "lambda_seat": "kept symbolic (G08 OPEN; freezing lambda is the named scar)",
    "ker_r": "KER-R bound (banked): 'Static restriction cannot determine all four-dimensional terms' "
             "- any agreement here would be scoped-only",
    "bdy_td": "BDY-TD threat (banked): 'Bulk equation can remain while momentum and charge shift' "
              "- bulk verdicts are robust to total-derivative action shifts; condition-4 (boundary) "
              "data is typed separately (TC5)",
}

checks: list[dict[str, str]] = []
failures: list[str] = []


def check(cid: str, condition: object, detail: str = "") -> None:
    ok = bool(condition)
    checks.append({"id": cid, "status": "PASS" if ok else "FAIL", "detail": detail})
    print(f"[{time.time()-T0:7.1f}s] {'PASS' if ok else 'FAIL'} {cid} :: {detail}", flush=True)
    if not ok:
        failures.append(cid)


def simp(e):
    return sp.cancel(sp.expand(e))


def is_zero(e) -> bool:
    e2 = simp(e)
    if e2 == 0:
        return True
    e2 = sp.powsimp(e2, force=True)
    e2 = sp.cancel(e2)
    if e2 == 0:
        return True
    return sp.simplify(e2) == 0


t, x, y, z = sp.symbols("t x y z", real=True)
coords = [t, x, y, z]
NAMES = ["t", "x", "y", "z"]
c = sp.Symbol("c_E", positive=True)      # registered-family constant (CHOSE)
alpha = sp.Symbol("alpha", real=True)    # registered-family constant twist (CHOSE)
lam = sp.Symbol("lambda", real=True)     # transverse seat exponent - SYMBOLIC, never frozen
Lam = sp.Symbol("Lambda", real=True)     # EH cosmological constant - SYMBOLIC, never fitted

phi = sp.Function("phi", real=True)(x)   # free field (depth)
f = sp.Function("f", real=True)(x)       # free field (connection moment, T^2 stratum)
bh = sp.Function("bh", positive=True)(x) # free field (horizontal norm, T^2 stratum)


# ----------------------------------------------------------------------------
# Restriction pipeline: evaluate the two UNRESTRICTED variational tensors on a metric.
# The covariant formulas below ARE the unrestricted variational outputs (full-vary
# first); this function only EVALUATES them componentwise (restrict second).
# ----------------------------------------------------------------------------
def restrict_all(gmat, simplifier=simp):
    S = simplifier
    ginv = gmat.inv().applyfunc(S)
    dg = [[[sp.diff(gmat[i, j], coords[m]) for j in range(4)] for i in range(4)] for m in range(4)]
    Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for i in range(4):
            for j in range(i, 4):
                e = 0
                for d in range(4):
                    if ginv[a, d] != 0:
                        e += ginv[a, d] * (dg[i][d][j] + dg[j][d][i] - dg[d][i][j])
                e = S(e / 2)
                Gam[a][i][j] = Gam[a][j][i] = e
    Riem = {}
    for a in range(4):
        for b_ in range(4):
            for cc in range(4):
                for d in range(cc + 1, 4):
                    e = sp.diff(Gam[a][d][b_], coords[cc]) - sp.diff(Gam[a][cc][b_], coords[d])
                    for m in range(4):
                        e += Gam[a][cc][m] * Gam[m][d][b_] - Gam[a][d][m] * Gam[m][cc][b_]
                    e = S(e)
                    if e != 0:
                        Riem[(a, b_, cc, d)] = e
                        Riem[(a, b_, d, cc)] = -e
    Rl = {}
    for a in range(4):
        for b_ in range(4):
            for cc in range(4):
                for d in range(cc + 1, 4):
                    e = 0
                    for m in range(4):
                        v = Riem.get((m, b_, cc, d), 0)
                        if v != 0 and gmat[a, m] != 0:
                            e += gmat[a, m] * v
                    e = S(e)
                    if e != 0:
                        Rl[(a, b_, cc, d)] = e
                        Rl[(a, b_, d, cc)] = -e
    Ric = sp.zeros(4, 4)
    for b_ in range(4):
        for d in range(4):
            Ric[b_, d] = S(sum(Riem.get((a, b_, a, d), 0) for a in range(4)))
    Rsc = S(sum(ginv[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
    Cl = {}
    for a in range(4):
        for b_ in range(4):
            for cc in range(4):
                for d in range(4):
                    e = (Rl.get((a, b_, cc, d), 0)
                         - sp.Rational(1, 2) * (gmat[a, cc] * Ric[b_, d] - gmat[a, d] * Ric[b_, cc]
                                                - gmat[b_, cc] * Ric[a, d] + gmat[b_, d] * Ric[a, cc])
                         + Rsc / 6 * (gmat[a, cc] * gmat[b_, d] - gmat[a, d] * gmat[b_, cc]))
                    e = S(e)
                    if e != 0:
                        Cl[(a, b_, cc, d)] = e

    def cov_d_C(e_, a, b_, cc, d):
        ex_ = sp.diff(Cl.get((a, b_, cc, d), 0), coords[e_])
        for m in range(4):
            ex_ -= Gam[m][e_][a] * Cl.get((m, b_, cc, d), 0)
            ex_ -= Gam[m][e_][b_] * Cl.get((a, m, cc, d), 0)
            ex_ -= Gam[m][e_][cc] * Cl.get((a, b_, m, d), 0)
            ex_ -= Gam[m][e_][d] * Cl.get((a, b_, cc, m), 0)
        return ex_

    Tt = {}
    for a in range(4):
        for cc in range(4):
            for b_ in range(4):
                e = 0
                for d in range(4):
                    for e_ in range(4):
                        if ginv[d, e_] != 0:
                            e += ginv[d, e_] * cov_d_C(e_, a, cc, b_, d)
                e = S(e)
                if e != 0:
                    Tt[(a, cc, b_)] = e

    def cov_d_T(fq, a, cc, b_):
        e = sp.diff(Tt.get((a, cc, b_), 0), coords[fq])
        for m in range(4):
            e -= Gam[m][fq][a] * Tt.get((m, cc, b_), 0)
            e -= Gam[m][fq][cc] * Tt.get((a, m, b_), 0)
            e -= Gam[m][fq][b_] * Tt.get((a, cc, m), 0)
        return e

    Ricup = sp.zeros(4, 4)
    for a in range(4):
        for b_ in range(4):
            Ricup[a, b_] = S(sum(ginv[a, i] * ginv[b_, j] * Ric[i, j] for i in range(4) for j in range(4)))
    B = sp.zeros(4, 4)
    for a in range(4):
        for b_ in range(4):
            e1 = 0
            for cc in range(4):
                for fq in range(4):
                    if ginv[cc, fq] != 0:
                        e1 += ginv[cc, fq] * cov_d_T(fq, a, cc, b_)
            e2 = 0
            for cc in range(4):
                for d in range(4):
                    v = Cl.get((a, cc, b_, d), 0)
                    if v != 0 and Ricup[cc, d] != 0:
                        e2 += Ricup[cc, d] * v
            B[a, b_] = S(e1 + sp.Rational(1, 2) * e2)
    EH = sp.zeros(4, 4)
    for a in range(4):
        for b_ in range(4):
            EH[a, b_] = S(Ric[a, b_] - sp.Rational(1, 2) * Rsc * gmat[a, b_] + Lam * gmat[a, b_])
    return {"ginv": ginv, "Gam": Gam, "Riem": Riem, "Rl": Rl, "Ric": Ric, "Rsc": Rsc,
            "Cl": Cl, "Tt": Tt, "B": B, "EH": EH}


# ----------------------------------------------------------------------------
# TC1: the declared comparison domain (census; ledger in EXACT_DERIVATION.md)
# ----------------------------------------------------------------------------
u = sp.exp(-2 * phi)                      # u = e^{-2 phi} > 0 (registered)
W = sp.exp(2 * lam * phi)                 # screen-leg conformal seat e^{2 lambda phi}
q = 1 / u - alpha**2 * u

g = sp.zeros(4, 4)
g[0, 0] = -c**2 * u
g[0, 3] = g[3, 0] = -c * u * alpha
g[0, 2] = g[2, 0] = -c * u * alpha * f
g[1, 1] = W
g[2, 2] = q * f**2 + W * bh
g[2, 3] = g[3, 2] = q * f
g[3, 3] = q

check("C01_metric_determinant", is_zero(sp.factor(g.det()) + c**2 * bh * W**2),
      "det g = -c_E^2 bh e^{4 lambda phi} (matches plane-audit A01 with b = W*bh)")

R = restrict_all(g)
ginv, Gam, Rl, Ric, Rsc, Cl, B, EH = (R["ginv"], R["Gam"], R["Rl"], R["Ric"], R["Rsc"],
                                      R["Cl"], R["B"], R["EH"])
print(f"[{time.time()-T0:7.1f}s] full-family restriction done "
      f"({len(R['Riem'])} Riem, {len(Cl)} Weyl nonzero entries)", flush=True)

check("C02_inverse_exact", all(is_zero((g * ginv)[i, j] - (1 if i == j else 0))
                               for i in range(4) for j in range(4)), "g.g^{-1} = 1 exactly")

bianchi_ok = all(
    is_zero(Rl.get((a, b_, cc, d), 0) + Rl.get((a, cc, d, b_), 0) + Rl.get((a, d, b_, cc), 0))
    for a in range(4) for b_ in range(4) for cc in range(4) for d in range(4))
check("C03_first_bianchi", bianchi_ok, "R_a[bcd] = 0 on the restriction")
check("C04_pair_symmetry", all(is_zero(Rl.get((a, b_, cc, d), 0) - Rl.get((cc, d, a, b_), 0))
                               for a in range(4) for b_ in range(4) for cc in range(4) for d in range(4)),
      "R_abcd = R_cdab")
check("C05_ricci_symmetric", all(is_zero(Ric[i, j] - Ric[j, i]) for i in range(4) for j in range(4)))
check("C06_weyl_tracefree",
      all(is_zero(sum(ginv[a, cc] * Cl.get((a, b_, cc, d), 0) for a in range(4) for cc in range(4)))
          for b_ in range(4) for d in range(4)),
      "all traces of C_abcd vanish on the restriction")

# contracted Bianchi: nabla_a G^{ab} = 0 (soundness of the EH restriction, TC3)
Gt = EH - Lam * g
Gup = sp.zeros(4, 4)
for a in range(4):
    for b_ in range(4):
        Gup[a, b_] = simp(sum(ginv[a, i] * ginv[b_, j] * Gt[i, j] for i in range(4) for j in range(4)))
divG_ok = True
for b_ in range(4):
    e = 0
    for a in range(4):
        e += sp.diff(Gup[a, b_], coords[a])
        for m in range(4):
            e += Gam[a][a][m] * Gup[m, b_] + Gam[b_][a][m] * Gup[a, m]
    if not is_zero(e):
        divG_ok = False
check("C07_contracted_bianchi", divG_ok, "nabla_a G^{ab} = 0 exactly on the restriction")

check("C08_bach_symmetric", all(is_zero(B[a, b_] - B[b_, a]) for a in range(4) for b_ in range(4)))
check("C09_bach_tracefree", is_zero(sum(ginv[a, b_] * B[a, b_] for a in range(4) for b_ in range(4))))
check("C10_mixed_transverse_rows_vanish",
      all(is_zero(B[a, 1]) and is_zero(EH[a, 1]) for a in (0, 2, 3)),
      "B_ax = 0 and (G+Lambda g)_ax = 0 identically for a in {t,y,z}: 7 independent components each")

COMPS = [(0, 0), (0, 2), (0, 3), (1, 1), (2, 2), (2, 3), (3, 3)]
CNAMES = {(0, 0): "tt(lapse)", (0, 2): "ty(momentum)", (0, 3): "tz(momentum)",
          (1, 1): "xx(radial constraint)", (2, 2): "yy", (2, 3): "yz", (3, 3): "zz"}

# ----------------------------------------------------------------------------
# TC2/TC3 presentation: jetization (exact ODE systems in the jet variables)
# ----------------------------------------------------------------------------
P = sp.symbols("p0:5", real=True)
F = sp.symbols("f0:5", real=True)
H = sp.symbols("h0:5", real=True)
jet_subs = []
for n in range(4, 0, -1):
    jet_subs.append((sp.Derivative(phi, (x, n)), P[n]))
    jet_subs.append((sp.Derivative(f, (x, n)), F[n]))
    jet_subs.append((sp.Derivative(bh, (x, n)), H[n]))
jet_subs += [(phi, P[0]), (f, F[0]), (bh, H[0])]


def jetize(e):
    return simp(e.subs(jet_subs))


Bj = {k: jetize(B[k[0], k[1]]) for k in COMPS}
Ej = {k: jetize(EH[k[0], k[1]]) for k in COMPS}
gj = {k: jetize(g[k[0], k[1]]) for k in COMPS}
print(f"[{time.time()-T0:7.1f}s] jetization done", flush=True)


def jet_signature(e):
    return sorted([str(s_) for s_ in e.free_symbols if str(s_)[0] in "pfh" and str(s_) != "phi"])


sig_B = {CNAMES[k]: jet_signature(Bj[k]) for k in COMPS}
sig_E = {CNAMES[k]: jet_signature(Ej[k]) for k in COMPS}
b_high = all(any(s_ in ("p3", "p4", "f3", "f4", "h3", "h4") for s_ in sig_B[CNAMES[k]]) for k in COMPS)
e_low = all(not any(s_ in ("p3", "p4", "f3", "f4", "h3", "h4") for s_ in sig_E[CNAMES[k]]) for k in COMPS)
check("C11_jet_order_split", b_high and e_low,
      "every Bach component carries 3rd/4th jets; no EH component carries any jet above 2nd")

# ----------------------------------------------------------------------------
# TC4 witnesses
# ----------------------------------------------------------------------------
# W-FLAT: constants member (phi, f, bh constant) -> Riemann = 0 (in-domain flat member)
const_subs = {P[i]: 0 for i in range(1, 5)}
const_subs.update({F[i]: 0 for i in range(1, 5)})
const_subs.update({H[i]: 0 for i in range(1, 5)})
check("C12_constants_member_flat", all(is_zero(jetize(v).subs(const_subs)) for v in Rl.values()),
      "constants member has Riemann = 0")
check("C13_witness_W_FLAT",
      all(is_zero(Bj[k].subs(const_subs)) for k in COMPS)
      and all(is_zero(Ej[k].subs(const_subs) - Lam * gj[k].subs(const_subs)) for k in COMPS),
      "W-FLAT: B_ab = 0 identically; (G+Lambda g)_ab = Lambda g_ab != 0 for every Lambda != 0 "
      "(g nondegenerate)")

# Per-component jet witnesses.  Two deterministic parameter/jet-value sets; p0 = 0 keeps
# all exponentials at 1 so every evaluation is exact rational (lambda enters
# polynomially).  For each direction the solve-symbol is chosen FIRST, all other jets
# then get their set values, and the single linear equation is solved exactly.
PARAMS1 = {P[0]: 0, F[0]: sp.Rational(1, 7), H[0]: 1,
           alpha: sp.Rational(1, 2), c: 1, lam: sp.Rational(1, 3)}
PARAMS2 = {P[0]: 0, F[0]: sp.Rational(1, 5), H[0]: 2,
           alpha: sp.Rational(1, 3), c: 1, lam: sp.Rational(1, 5)}
JETVALS1 = {P[1]: sp.Rational(1, 2), P[2]: sp.Rational(1, 3), P[3]: sp.Rational(1, 5), P[4]: sp.Rational(1, 37),
            F[1]: sp.Rational(1, 11), F[2]: sp.Rational(1, 13), F[3]: sp.Rational(1, 17), F[4]: sp.Rational(1, 41),
            H[1]: sp.Rational(1, 19), H[2]: sp.Rational(1, 23), H[3]: sp.Rational(1, 29), H[4]: sp.Rational(1, 43)}
JETVALS2 = {P[1]: sp.Rational(1, 3), P[2]: sp.Rational(1, 5), P[3]: sp.Rational(1, 7), P[4]: sp.Rational(1, 41),
            F[1]: sp.Rational(1, 13), F[2]: sp.Rational(1, 17), F[3]: sp.Rational(1, 19), F[4]: sp.Rational(1, 43),
            H[1]: sp.Rational(1, 23), H[2]: sp.Rational(1, 29), H[3]: sp.Rational(1, 31), H[4]: sp.Rational(1, 47)}
TOP_ORDER = [P[4], F[4], H[4], P[3], F[3], H[3]]
LOW_ORDER = [H[2], F[2], P[2], H[1], F[1], P[1]]

ledger_rows = []
witnessA = {}
witnessB = {}
for k in COMPS:
    name = CNAMES[k]
    rowA, rowB = [], []
    okA = okB = True
    numB_polys = []
    lamstar = []
    for bi, (params, jetvals) in enumerate(((PARAMS1, JETVALS1), (PARAMS2, JETVALS2)), start=1):
        B0 = Bj[k].subs(params)
        E0 = Ej[k].subs(params)
        # ---- direction A: Bach component = 0, EH component != 0 ----
        solved = None
        for s_ in TOP_ORDER:
            if s_ in B0.free_symbols and s_ not in E0.free_symbols:
                assign = {q_: v_ for q_, v_ in jetvals.items() if q_ != s_}
                pol = sp.Poly(sp.numer(sp.together(sp.cancel(B0.subs(assign)))), s_)
                if pol.degree() == 1 and pol.nth(1) != 0:
                    root = sp.cancel(-pol.nth(0) / pol.nth(1))
                    solved = (s_, root, assign)
                    break
        if solved is None:
            okA = False
            rowA.append(f"set{bi}: no linear top jet found")
        else:
            s_, root, assign = solved
            full = dict(params)
            full.update(assign)
            full[s_] = root
            bval = sp.cancel(Bj[k].subs(full))
            eval_ = sp.cancel(Ej[k].subs(full))
            pe = sp.Poly(eval_, Lam)
            qcoef = pe.nth(1) if pe.degree() >= 1 else sp.Integer(0)
            pcoef = pe.nth(0)
            okA = okA and (bval == 0) and (qcoef != 0)
            ls = sp.cancel(-pcoef / qcoef) if qcoef != 0 else None
            lamstar.append(ls)
            rowA.append(f"set{bi}: {s_}={root}; B={bval}; E={eval_}; exceptional Lambda*={ls}")
        # ---- direction B: EH component = 0 (Lambda symbolic), Bach component != 0 ----
        if k == (1, 1):
            continue  # xx handled by the exact quadratic construction below
        solvedE = None
        for s_ in LOW_ORDER:
            if s_ in E0.free_symbols:
                assign = {q_: v_ for q_, v_ in jetvals.items() if q_ != s_}
                polE = sp.Poly(sp.numer(sp.together(sp.cancel(E0.subs(assign)))), s_)
                if polE.degree() == 1 and polE.nth(1) != 0:
                    rootE = sp.cancel(-polE.nth(0) / polE.nth(1))
                    solvedE = (s_, rootE, assign)
                    break
        if solvedE is None:
            okB = False
            rowB.append(f"set{bi}: no linear jet in EH comp")
        else:
            s_, rootE, assign = solvedE
            full = dict(params)
            full.update(assign)
            full[s_] = rootE
            eval2 = sp.cancel(Ej[k].subs(full))
            bval2 = sp.cancel(Bj[k].subs(full))
            nB = sp.expand(sp.numer(sp.together(bval2)))
            okB = okB and (eval2 == 0) and (nB != 0)
            numB_polys.append(sp.Poly(nB, Lam))
            rowB.append(f"set{bi}: {s_}={rootE}; E={eval2}; B={bval2}")
    lam_cover_A = (len(lamstar) == 2 and lamstar[0] is not None and lamstar[1] is not None
                   and sp.cancel(lamstar[0] - lamstar[1]) != 0)
    lam_cover_B = False
    if k != (1, 1) and len(numB_polys) == 2:
        gcd_ = sp.gcd(numB_polys[0], numB_polys[1])
        lam_cover_B = (gcd_.degree() == 0)
    if k == (1, 1):
        # E_xx is the 1st-order radial constraint; at p0 = 0 it is EXACTLY
        # (4 Lambda h0 + (alpha^2 - 1) f1^2 - 4 h0 p1^2)/(4 h0): quadratic in f1 and p1,
        # with h1 and all 2nd jets absent, and lambda absent.  Verify that identity,
        # then use the exact even-parity construction: set every f-jet except f1 to 0
        # (B_xx is even under flipping all f-jets - an exact discrete isometry check),
        # so B_xx depends on f1 only through f1^2, and substitute
        # f1^2 = 4 h0 (Lambda - p1^2)/(1 - alpha^2)  [makes E_xx = 0 exactly for
        # symbolic Lambda; a real domain point wherever f1^2 >= 0].
        exx_id = sp.cancel(Ej[k] - (4 * Lam * H[0] + (alpha**2 - 1) * F[1]**2
                                    - 4 * H[0] * P[1]**2) / (4 * H[0])).subs(P[0], 0)
        id_ok = sp.cancel(sp.expand(exx_id)) == 0
        flipF = {F[i]: -F[i] for i in range(5)}
        parity_ok = sp.cancel(Bj[k].subs(flipF, simultaneous=True) - Bj[k]) == 0
        XXW = [
            # (alpha, p1, h0, lam, jetset, validity as (lower, upper) with None = open)
            (sp.Rational(1, 2), 0, 1, sp.Rational(1, 3), JETVALS1, (0, None)),
            (2, 1, 1, sp.Rational(1, 5), JETVALS2, (None, 1)),
            (3, 2, 2, sp.Rational(1, 7), JETVALS1, (None, 4)),
        ]
        xx_rows = []
        xx_polys = []
        xx_ok = id_ok and parity_ok
        for wi, (av, p1v, h0v, lv, jv, valid) in enumerate(XXW, start=1):
            f1sq = sp.cancel(4 * h0v * (Lam - p1v**2) / (1 - av**2))
            sub = {P[0]: 0, P[1]: p1v, H[0]: h0v, alpha: av, c: 1, lam: lv,
                   F[0]: 0, F[2]: 0, F[3]: 0, F[4]: 0,
                   P[2]: jv[P[2]], P[3]: jv[P[3]], P[4]: jv[P[4]],
                   H[1]: jv[H[1]], H[2]: jv[H[2]], H[3]: jv[H[3]], H[4]: jv[H[4]]}
            eS = sp.together(sp.cancel(Ej[k].subs(sub)))
            bS = sp.together(sp.cancel(Bj[k].subs(sub)))
            okw = not sp.denom(eS).has(F[1]) and not sp.denom(bS).has(F[1])
            pe_ = sp.Poly(sp.numer(eS), F[1])
            pb_ = sp.Poly(sp.numer(bS), F[1])
            okw = okw and all(co == 0 for mm, co in zip(pe_.monoms(), pe_.coeffs()) if mm[0] % 2)
            okw = okw and all(mm[0] % 2 == 0 for mm in pb_.monoms())
            eval_even = sum(co * f1sq**(mm[0] // 2) for mm, co in zip(pe_.monoms(), pe_.coeffs()))
            bval_even = sum(co * f1sq**(mm[0] // 2) for mm, co in zip(pb_.monoms(), pb_.coeffs()))
            okw = okw and sp.cancel(eval_even) == 0
            nB_ = sp.Poly(sp.expand(sp.numer(sp.together(sp.cancel(bval_even)))), Lam)
            okw = okw and nB_.as_expr() != 0
            xx_ok = xx_ok and okw
            xx_polys.append((nB_, valid))
            xx_rows.append(f"w{wi}: alpha={av},p1={p1v},h0={h0v},lambda={lv},f-jets=0 except "
                           f"f1^2={f1sq}; valid Lambda in {valid}; E=0 exactly; "
                           f"B numerator in Lambda: {nB_.as_expr()}")
        # coverage: validity intervals [0,inf), (-inf,1], (-inf,4] cover R; for every
        # real root r of one witness's Bach numerator inside its validity interval,
        # another witness must be valid at r with a gcd-coprime numerator.
        def in_valid(r, valid):
            lo, hi = valid
            if lo is not None and bool(r < lo):
                return False
            if hi is not None and bool(r > hi):
                return False
            return True
        cover_ok = True
        for i_ in range(len(xx_polys)):
            Ni, vi = xx_polys[i_]
            for r in sp.Poly(Ni.as_expr(), Lam).real_roots():
                if not in_valid(r, vi):
                    continue
                saved = False
                for j_ in range(len(xx_polys)):
                    if j_ == i_:
                        continue
                    Nj, vj = xx_polys[j_]
                    if in_valid(r, vj) and sp.gcd(Ni, Nj).degree() == 0:
                        saved = True
                        break
                if not saved:
                    cover_ok = False
        okB = xx_ok
        lam_cover_B = cover_ok
        rowB = xx_rows
    short = name.split("(")[0]
    check(f"C14_{short}_witness_A", okA and lam_cover_A,
          f"{name}: Bach comp = 0, EH comp != 0 for every Lambda (two witnesses, distinct Lambda*)")
    msgB = ("three even-parity f1^2 witnesses; validity intervals cover R; roots cross-covered"
            if k == (1, 1) else "two witnesses, Lambda-numerators share no root")
    check(f"C15_{short}_witness_B", okB and lam_cover_B,
          f"{name}: EH comp = 0 (symbolic Lambda), Bach comp != 0 for every Lambda ({msgB})")
    witnessA[name] = rowA
    witnessB[name] = rowB
    verdict = "INEQUIVALENT" if (okA and lam_cover_A and okB and lam_cover_B) else "CHECK-FAILED"
    ledger_rows.append({
        "component": name,
        "bach_jets": ",".join(sig_B[name]),
        "eh_jets": ",".join(sig_E[name]),
        "verdict": verdict,
        "witness_A_bach0_eh_nonzero": " | ".join(rowA),
        "witness_B_eh0_bach_nonzero": " | ".join(rowB),
        "proportionality": "excluded by witnesses in both directions (any nonzero factor contradicted)",
    })
print(f"[{time.time()-T0:7.1f}s] per-component witnesses done", flush=True)

# ----------------------------------------------------------------------------
# W-EXP: system-level witness on the exponential subfamily of the domain:
# phi = k x, f = 0, alpha = 0, bh = e^{2 s x}.  Same restriction pipeline, applied to
# the substituted member metric (evaluation commutes with specialization; spot-checked).
# ----------------------------------------------------------------------------
s_sym = sp.Symbol("s", real=True)


def slice_metric(kval, sval):
    sm = {}
    phis = kval * x
    bhs = sp.exp(2 * sval * x)
    for n in range(4, 0, -1):
        sm[sp.Derivative(phi, (x, n))] = sp.diff(phis, (x, n))
        sm[sp.Derivative(f, (x, n))] = 0
        sm[sp.Derivative(bh, (x, n))] = sp.diff(bhs, (x, n))
    sm[phi] = phis
    sm[f] = 0
    sm[bh] = bhs
    sm[alpha] = 0
    return g.subs(sm).applyfunc(lambda e: sp.powsimp(sp.expand(e), force=True)), sm


def esimp(e):
    return sp.cancel(sp.powsimp(sp.expand(e), force=True))


# rational witness point on the Bach-flat branch with NONZERO Weyl: k=1, s=1, lambda=-5/4
gW, smW = slice_metric(1, 1)
gW = gW.subs(lam, sp.Rational(-5, 4)).applyfunc(esimp)
RW = restrict_all(gW, simplifier=esimp)
bach_zero = all(is_zero(RW["B"][i, j]) for i in range(4) for j in range(4))
weyl_nonzero = any(not is_zero(v) for v in RW["Cl"].values())
tfRic = [esimp(RW["Ric"][i, i] - RW["Rsc"] / 4 * gW[i, i]) for i in range(4)]
tf_nonzero = any(not is_zero(v) for v in tfRic)
check("C16_witness_W_EXP", bach_zero and weyl_nonzero and tf_nonzero,
      "W-EXP (phi=x, bh=e^{2x}, f=0, alpha=0, lambda=-5/4): B_ab = 0 identically, Weyl != 0 "
      "(NOT conformally flat), trace-free Ricci != 0 => (G+Lambda g)_ab != 0 for EVERY Lambda incl. 0")
# consistency spot-check: pipeline-on-slice equals substitute-into-family for B_tt, EH_tt
spot_B = is_zero(B[0, 0].subs(smW).subs(lam, sp.Rational(-5, 4)) - RW["B"][0, 0])
spot_E = is_zero(EH[0, 0].subs(smW).subs(lam, sp.Rational(-5, 4)) - RW["EH"][0, 0])
check("C16b_slice_consistency", spot_B and spot_E,
      "slice pipeline agrees with direct substitution into the family tensors (B_tt, E_tt)")
# bonus witness W-EXP-CF: the branch point k=1, s=2, lambda=-1 is CONFORMALLY FLAT
# (Weyl = 0, so Bach = 0 trivially) yet non-Einstein for every Lambda
gC, _ = slice_metric(1, 2)
gC = gC.subs(lam, -1).applyfunc(esimp)
RC = restrict_all(gC, simplifier=esimp)
cf_weyl_zero = all(is_zero(v) for v in RC["Cl"].values())
cf_bach_zero = all(is_zero(RC["B"][i, j]) for i in range(4) for j in range(4))
cf_tf = any(not is_zero(esimp(RC["Ric"][i, i] - RC["Rsc"] / 4 * gC[i, i])) for i in range(4))
check("C16c_witness_W_EXP_CF", cf_weyl_zero and cf_bach_zero and cf_tf,
      "W-EXP-CF (phi=x, bh=e^{4x}, f=0, alpha=0, lambda=-1): conformally flat (Weyl = 0) "
      "non-Einstein member - Bach = 0 trivially, (G+Lambda g) != 0 for every Lambda")

# the one-parameter Bach-flat branch on the slice (k=1, s and lambda symbolic):
gS, _ = slice_metric(1, s_sym)
RS = restrict_all(gS, simplifier=esimp)
common = 4 * lam * s_sym + s_sym**2 + 4
branch_ok = True
slice_polys = {}
for i in range(4):
    e = RS["B"][i, i]
    if e == 0:
        branch_ok = False
        continue
    w = sp.factor(esimp(e / gS[i, i] * sp.exp(4 * lam * x)))
    slice_polys[NAMES[i]] = str(w)
    if w.has(sp.exp) or w.has(x):
        branch_ok = False
        continue
    quot = sp.together(sp.cancel(w / common))
    if not sp.denom(quot).is_number:
        branch_ok = False
check("C17_bach_flat_branch", branch_ok,
      "on the exponential slice (k=1) every deweighted Bach component is an x-free polynomial "
      "divisible by (4 lambda s + s^2 + 4): a ONE-PARAMETER Bach-flat branch; it requires "
      "lambda*s = -(s^2+4)/4 < 0, hence lambda != 0 (a frozen lambda = 0 seat admits no branch)")

# A1 amendment check (verifier finding, 2026-07-28): an earlier hand-written ledger
# sentence claimed the slice Bach-flat locus was the branch "plus a discrete root pair
# lambda = +/- 5 sqrt(21)/21, s = -/+ 2 sqrt(21)/7".  That pair is a redundant sp.solve
# output: it satisfies 4 lambda s + s^2 + 4 = 0 EXACTLY, i.e. it lies ON the branch and
# is NOT a separate locus (verifier Groebner basis of the quotient system: {s - 2 lambda,
# 3 lambda^2 + 1} - no real solutions).  Zero-residual proof that both sign choices of
# the former "pair" satisfy the branch equation:
pair_on_branch = all(
    is_zero((4 * lam * s_sym + s_sym**2 + 4).subs({lam: lv, s_sym: sv}))
    for lv, sv in ((5 * sp.sqrt(21) / 21, -2 * sp.sqrt(21) / 7),
                   (-5 * sp.sqrt(21) / 21, 2 * sp.sqrt(21) / 7)))
check("C17b_pair_lies_on_branch", pair_on_branch,
      "the former 'discrete root pair' lambda = +/- 5 sqrt(21)/21, s = -/+ 2 sqrt(21)/7 "
      "satisfies 4 lambda s + s^2 + 4 = 0 exactly (both signs): it lies ON the one-parameter "
      "branch - the slice Bach-flat locus is the branch ALONE (A1 correction, check-backed)")

# Einstein rigidity on the slice: at k = 1 (scaling gauge for nonflat members) the
# EH+Lambda system has NO roots; the flat member k = s = 0 solves it with Lambda = 0 only.
eqs = [sp.numer(sp.together(esimp(RS["EH"][i, i] / gS[i, i]))) for i in range(4)]
eqs = [sp.factor(sp.cancel(sp.powsimp(e, force=True))) for e in eqs]
esols = sp.solve(eqs, [s_sym, Lam], dict=True)
gF, _ = slice_metric(0, 0)
RF = restrict_all(gF.applyfunc(esimp), simplifier=esimp)
flat_solves = all(is_zero(RF["EH"][i, j].subs(Lam, 0)) for i in range(4) for j in range(4))
flat_needs_L0 = all(is_zero(RF["EH"][i, j] - Lam * gF[i, j]) for i in range(4) for j in range(4))
check("C18_einstein_slice_rigidity", len(esols) == 0 and flat_solves and flat_needs_L0,
      f"EH+Lambda on the exponential slice (k=1 nonflat gauge) has NO roots (roots={esols}); "
      "the k=s=0 flat member solves it and only with Lambda=0 [SCOPED to the exponential subfamily]")
print(f"[{time.time()-T0:7.1f}s] slice analysis done", flush=True)

# ----------------------------------------------------------------------------
# Outputs
# ----------------------------------------------------------------------------
with (HERE / "BACH_ODE_SYSTEM_FULL.txt").open("w", encoding="utf-8") as fh:
    fh.write("# Full-family restricted Bach system B_ab = 0 in jet variables.\n"
             "# p0..p4 = phi..phi''''; f0..f4 = f..f''''; h0..h4 = bh..bh'''' (x-derivatives).\n"
             "# u = e^{-2 p0}; screen seat W = e^{2 lambda p0}; alpha, c_E, lambda symbolic constants.\n"
             "# Independent components; all others are identically zero or symmetric copies.\n\n")
    for k in COMPS:
        fh.write(f"== B_{CNAMES[k]} ==\n{sp.sstr(Bj[k])}\n\n")
with (HERE / "EH_ODE_SYSTEM_FULL.txt").open("w", encoding="utf-8") as fh:
    fh.write("# Full-family restricted EH+Lambda system (G_ab + Lambda g_ab) = 0 in jet variables.\n"
             "# Same conventions as BACH_ODE_SYSTEM_FULL.txt; Lambda symbolic.\n\n")
    for k in COMPS:
        fh.write(f"== E_{CNAMES[k]} ==\n{sp.sstr(Ej[k])}\n\n")

sys_rows = [
    {"component": "SYSTEM (all 7 components)", "bach_jets": "-", "eh_jets": "-",
     "verdict": "INEQUIVALENT (restricted equation sets differ; Bach admits members EH+Lambda excludes)",
     "witness_A_bach0_eh_nonzero":
         "W-FLAT (constants member): B == 0, E = Lambda*g != 0 for every Lambda != 0 || "
         "W-EXP (phi=x, bh=e^{2x}, f=0, alpha=0, lambda=-5/4): B == 0 identically with Weyl != 0, "
         "trace-free Ricci != 0 so (G+Lambda g) != 0 for EVERY Lambda || "
         "W-EXP-CF (phi=x, bh=e^{4x}, lambda=-1): conformally flat non-Einstein member",
     "witness_B_eh0_bach_nonzero":
         "scoped containment side: on the exponential slice EH+Lambda admits ONLY the flat member "
         "(with Lambda=0) while Bach admits the one-parameter branch 4 lambda s + s^2 + 4 = 0 "
         "ALONE (a redundant solver-output pair at lambda = +/- 5 sqrt(21)/21, s = -/+ 2 sqrt(21)/7 "
         "lies ON the branch - zero-residual check C17b; A1 correction)",
     "proportionality": "n/a"},
]
with (HERE / "SECTOR_COMPARISON_LEDGER.tsv").open("w", encoding="utf-8") as fh:
    # A2 amendment (F-C6 letter-compliance): the stand-alone verdict-bearing TSV carries
    # its three conditionality stamps in-file, as '#'-prefixed header comment lines
    # (parseable: skip lines starting with '#').
    fh.write(f"# STAMP domain: {STAMPS['domain']}\n")
    fh.write(f"# STAMP c2_side: {STAMPS['c2_side']}\n")
    fh.write(f"# STAMP eh_side: {STAMPS['eh_side']}\n")
    cols = ["component", "bach_jets", "eh_jets", "verdict", "witness_A_bach0_eh_nonzero",
            "witness_B_eh0_bach_nonzero", "proportionality"]
    fh.write("\t".join(cols) + "\n")
    for row in ledger_rows + sys_rows:
        fh.write("\t".join(str(row[c_]) for c_ in cols) + "\n")

n_pass = sum(1 for c_ in checks if c_["status"] == "PASS")
result = {
    "contract": "udt_p4_routeC_shared_static_sector_2026-07-28/PREREGISTRATION.md",
    "stamps": STAMPS,
    "scope": {
        "domain": "registered stationary family, local toric chart of the R x T^2 stratum "
                  "(locally contains the R_t x S^3 Hopf members); vacuum restricted equations only; "
                  "lambda symbolic; alpha, c_E symbolic constants; witnesses are specific domain points",
        "throughput": "FULL (u,f,bh,alpha;lambda) family computed - no fallback stratum reduction needed",
        "asymmetry": "inequivalence on this subfamily refutes exact equation-sharing on ANY superset "
                     "domain containing it (pair-scoped); agreement would have been scoped-only (KER-R)",
        "containment_note": "the standard 4D fact 'Einstein => Bach-flat' is cited as Category-A "
                            "mathematics and verified here only on slice members (flat); it is NOT "
                            "re-proven on the full ansatz",
    },
    "tc4_outcome_class": ("OC1 (exact inequivalence with witnesses)" if not failures
                          else "CHECK-FAILURES-PRESENT"),
    "jet_signatures": {"bach": sig_B, "eh": sig_E},
    "witness_A": witnessA,
    "witness_B": witnessB,
    "slice_bach_deweighted_polys": slice_polys,
    "einstein_slice_roots_k1": [str(so) for so in esols],
    "checks": checks,
    "failures": failures,
    "n_checks": len(checks),
    "n_pass": n_pass,
    "elapsed_s": round(time.time() - T0, 1),
}
(HERE / "routeC_stage1_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

print(f"\n[{time.time()-T0:7.1f}s] SUMMARY: {n_pass}/{len(checks)} checks passed; "
      f"failures: {failures if failures else 'none'}", flush=True)
if failures:
    sys.exit(1)
print("ROUTE C STAGE 1 DERIVATION: ALL CHECKS PASSED (outcome class OC1)")
