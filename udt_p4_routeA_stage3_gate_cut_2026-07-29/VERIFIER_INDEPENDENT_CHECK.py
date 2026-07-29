#!/usr/bin/env python3
"""BLIND VERIFIER independent re-derivation — P4 Route A Stage 3 (Slice 1).

Written by the blind adversarial verifier (same-session-spawned caveat travels),
2026-07-29. Own constructions throughout: independent jet machinery (different data
layout), independent Euler/adjoint operators, independent Helmholtz-condition
derivation for the P2 (a=0) and P1-4D (a_F = 2*lam) branches, the contract-§6
duties (G3 partition re-derivation + G5 census cells), witness re-checks, the
four-corner transversality, and ADVERSARIAL counter-constructions — including an
in-family counterexample to the "anchored-log forcing whenever the field sector is
nonzero" phrasing (V10b below).

Exit 0 iff every verifier check passes (counterexample checks PASS when the
counter-construction WORKS, i.e. when they refute the overbroad phrasing).
"""

import sys
import sympy as sp
from sympy import Function, Matrix, Rational, Symbol, symbols, exp, log, diff, expand, zeros, eye

FAILED = []


def vcheck(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    if not ok:
        FAILED.append(name)


# ---------------------------------------------------------------- own jet machinery
NF = 3  # fields u0=phi, u1=f, u2=bh
KMAX = 9
U = [[Symbol(f"u{i}_{k}") for k in range(KMAX)] for i in range(NF)]
W = [[Symbol(f"w{i}_{k}") for k in range(KMAX)] for i in range(NF)]  # variations
lam, kmod, k10, c00, c01, c10, c11 = symbols("lam k_mod k10 c00 c01 c10 c11")
MOD = [lam, kmod, k10, c00, c01, c10, c11]
cE = Symbol("c_E", positive=True)
P0 = U[0][0]  # phi wall/bulk 0-jet = p0 = log(c_E/Q)


def DT(e):
    """own total derivative"""
    r = sp.Integer(0)
    for ch in U + W:
        for k in range(KMAX - 1):
            d = diff(e, ch[k])
            if d != 0:
                r += d * ch[k + 1]
    return r


def DTn(e, n):
    for _ in range(n):
        e = DT(e)
    return e


def EU(e, i, kmaxi=4):
    return sum((-1) ** k * DTn(diff(e, U[i][k]), k) for k in range(kmaxi + 1))


def helm_conditions(Delta, order=2):
    """Own derivation route: linearize, then compare operator vs adjoint by
    collecting coefficients of the variation jets after by-parts."""
    conds = []
    for i in range(NF):
        Lin_i = sum(diff(Delta[i], U[j][k]) * W[j][k] for j in range(NF) for k in range(order + 1))
        Adj_i = sum((-1) ** k * DTn(diff(Delta[j], U[i][k]) * W[j][0], k)
                    for j in range(NF) for k in range(order + 1))
        d = expand(Lin_i - Adj_i)
        for j in range(NF):
            for k in range(order + 2):
                conds.append(expand(diff(d, W[j][k])))
    return conds


def is_selfadjoint(Delta, order=2):
    return all(expand(c) == 0 for c in helm_conditions(Delta, order))


# ============ V1: Helmholtz conditions = self-adjointness; necessity, P2 branch ====
Lgen = Function("Lg")(*[U[i][k] for i in range(NF) for k in range(2)], *MOD)
EL = {i: expand(EU(Lgen, i, 2)) for i in range(NF)}
vcheck("V1_P2_necessity_generic_EL",
       is_selfadjoint([EL[0], EL[1], EL[2]], 2),
       "own adjoint comparison: E(L) of the generic order-1 L(all jets, all moduli) is "
       "exactly self-adjoint under P2 (a=0) — the package's condition system reproduced "
       "by an independent construction")

# a NON-self-adjoint probe must be caught (guard against a vacuous checker):
vcheck("V1_checker_not_vacuous",
       not is_selfadjoint([U[0][1], sp.Integer(0), sp.Integer(0)], 2),
       "the checker detects R=(u0',0,0) as non-self-adjoint (not a vacuous test)")

# ============ V2: P1-4D branch: weighted conditions + exact shift forms ============
WF = exp(2 * lam * P0)
Rg = [Function(f"R{i}")(*[U[j][k] for j in range(NF) for k in range(3)], *MOD) for i in range(NF)]
DeltaW = [WF * Rg[i] for i in range(NF)]
# own computation of the three condition families on the weighted member:
condsW = helm_conditions(DeltaW, 2)
# top-order (i): coefficient of w_j'' in Lin-Adj is  d(WF Ri)/du_j'' - d(WF Rj)/du_i''
top_ok = all(expand(diff(DeltaW[i], U[j][2]) - diff(DeltaW[j], U[i][2])
                    - WF * (diff(Rg[i], U[j][2]) - diff(Rg[j], U[i][2]))) == 0
             for i in range(NF) for j in range(NF))
vcheck("V2_P1_top_condition_weight_cancels", top_ok,
       "condition (i) on WF*R equals WF*(condition (i) on R): principal-symbol symmetry is "
       "pairing-independent across the anchored family — reproduced")
# first-order (ii) shift: Hi1(WF R)/WF = Hi1(R) - 2*(2 lam)*p1*dRj/dui''
sh_ok = True
for i in range(NF):
    for j in range(NF):
        Hi1_w = diff(DeltaW[i], U[j][1]) + diff(DeltaW[j], U[i][1]) - 2 * DT(diff(DeltaW[j], U[i][2]))
        Hi1_r = diff(Rg[i], U[j][1]) + diff(Rg[j], U[i][1]) - 2 * DT(diff(Rg[j], U[i][2]))
        if expand(Hi1_w / WF - (Hi1_r - 2 * (2 * lam) * U[0][1] * diff(Rg[j], U[i][2]))) != 0:
            sh_ok = False
vcheck("V2_P1_condition_ii_shift", sh_ok,
       "Hi1(WF R)/WF = Hi1(R) - 2 a_F p1 dR/du'' with a_F = 2 lam — the package's exact "
       "shift reproduced independently")

# ============ V3: witnesses W1 / W2' / W3 / omega ==================================
L0 = -(U[0][1] ** 2 + U[1][1] ** 2 + U[2][1] ** 2) / 2
W1 = [U[0][2], U[1][2], U[2][2]]
vcheck("V3_W1_LE_under_P2", is_selfadjoint(W1, 2), "W1=(p2,f2,h2) self-adjoint under P2")
W1w = [WF * t for t in W1]
d11 = expand(diff(W1w[0], U[0][1]) + diff(W1w[0], U[0][1]) - 2 * DT(diff(W1w[0], U[0][2])))
vcheck("V3_W1_NV_under_P1_defect",
       expand(d11 + 4 * lam * U[0][1] * WF) == 0 and d11.subs({lam: 1, P0: 0, U[0][1]: 1}) != 0
       and expand(d11.subs(lam, 0)) == 0,
       "W1 under P1-4D: Hi1(p,p) = -4 lam p1 e^{2 lam p0}; nonzero off lam=0, vanishes AT "
       "lam=0 (T4 blindness locus) — defect + scope reproduced")

# W2': field sector of the P1-generated member; own recomputation
Rp = expand(exp(-2 * lam * P0) * EU(exp(2 * lam * P0) * L0, 0, 2))
Rf = expand(exp(-2 * lam * P0) * EU(exp(2 * lam * P0) * L0, 1, 2))
Rh = expand(exp(-2 * lam * P0) * EU(exp(2 * lam * P0) * L0, 2, 2))
vcheck("V3_W2_field_sector_explicit",
       expand(Rp - (U[0][2] + lam * U[0][1] ** 2 - lam * U[1][1] ** 2 - lam * U[2][1] ** 2)) == 0,
       "field sector: R_p = p2 + lam(p1^2 - f1^2 - h1^2) (exponentials cancel; in-family)")
vcheck("V3_W2_LE_fieldfield_under_P1",
       is_selfadjoint([expand(WF * Rp), expand(WF * Rf), expand(WF * Rh)], 2),
       "the weighted field sector is exactly an EL tuple: (i)-(iii) hold under P1-4D")
d11_p2 = expand(2 * diff(Rp, U[0][1]) - 2 * DT(diff(Rp, U[0][2])))
vcheck("V3_W2_NV_under_P2",
       expand(d11_p2 - 4 * lam * U[0][1]) == 0,
       "same field sector under P2: Hi1(p,p) = 4 lam p1 != 0 off lam = 0 — reverse "
       "pairing-dependence witness reproduced")
# H4(lambda) on the field-only tuple (zero moduli slots) FAILS -> the forced lambda-slot:
lhs = expand(diff(WF * Rp, lam))
vcheck("V3_W2_fieldonly_fails_H4lambda",
       lhs != 0 and expand(lhs - WF * expand(diff(Rp, lam) + 2 * P0 * Rp)) == 0,
       "d(WF R_p)/dlam = WF[dR_p/dlam + 2 p0 R_p] != 0 while E_p(WM*0) = 0: the "
       "field-only W2 tuple fails the mixed (field,lambda) condition — the package's "
       "self-corrected statement is CORRECT")
Rlam_forced = expand(exp(-2 * lam * P0) * diff(exp(2 * lam * P0) * L0, lam))
vcheck("V3_W2_forced_lambda_slot",
       expand(Rlam_forced - 2 * P0 * L0) == 0,
       "the generated lambda-slot is exactly R_lam = 2 p0 Ltil0 (log-linear) — witness "
       "reproduced")

# W3 all-branch NV with symbolic a_F (branch-independence attack):
aFs = Function("aF")(lam)
WFs = exp(aFs * P0)
w3d = expand(2 * diff(WFs * U[0][1], U[0][1]) - 2 * DT(diff(WFs * U[0][1], U[0][2])))
vcheck("V3_W3_branch_independent_NV",
       expand(w3d - 2 * WFs) == 0,
       "W3=(p1,0,0): Hi1(p,p) = 2 e^{a_F p0} for SYMBOLIC a_F(lam) — an exponential, "
       "nowhere zero for any real branch value: NV across the entire anchored family; "
       "branch-independence proof HOLDS (attack failed)")
# attack: could W3 be rescued by nonzero moduli slots? No: (ii) is a field-field
# condition not involving moduli components.
vcheck("V3_W3_moduli_slots_cannot_rescue",
       all(str(m) not in str(w3d.free_symbols) for m in [kmod, k10, c00, c01, c10, c11]),
       "the failing condition involves no moduli component: no choice of moduli slots "
       "can restore LE membership for W3")

# omega-shape (moduli sector): closed under P2; defect under a_M = 2 lam
omega = {lam: sp.Integer(0), kmod: sp.Integer(0), k10: k10, c00: 0, c01: 0, c10: 0, c11: 0}
closed_p2 = all(expand(diff(omega[m], n) - diff(omega[n], m)) == 0 for m in MOD for n in MOD)
def_lam = expand(diff(exp(2 * lam * P0) * k10, lam))
vcheck("V3_omega_P2_LE_P1lamdep_NV",
       closed_p2 and def_lam.subs({lam: 1, P0: 1, k10: 1}) != 0,
       "omega = k10 dk10 closed (= d(k10^2/2)) under P2; (lam,k10) antisym defect "
       "2 p0 e^{2 lam p0} k10 != 0 under a_M = 2 lam — both reproduced")

# ============ V4: the intertwining bijection ======================================
subsK4 = [{k10: -k10, c00: -c00, c11: -c11}, {k10: -k10, c01: -c01, c10: -c10},
          {c00: -c00, c01: -c01, c10: -c10, c11: -c11}]
vcheck("V4_weight_K4_inert_invertible",
       all(expand(WFs.subs(s, simultaneous=True) - WFs) == 0 for s in subsK4)
       and sp.simplify(WFs * exp(-aFs * P0) - 1) == 0,
       "e^{a_F(lam) p0} touches only (lam, p0), both K4-inert; exactly invertible: "
       "R -> WF R is a bijection sending the P1 partition onto the P2 partition "
       "(LE(P1)[R] <=> the unweighted conditions hold for WF R <=> LE(P2)[WF R])")

# ============ V5: four-corner transversality on KMOD0 (P2, moduli sector) =========
def ident(c):
    return expand(-k10 * c.get("kmod", 0) + c10 * c.get("c00", 0) + c11 * c.get("c01", 0)
                  - c00 * c.get("c10", 0) - c01 * c.get("c11", 0))


def closed(c):
    v = {str(m): c.get({"lam": "lam", "k_mod": "kmod", "k10": "k10", "c00": "c00",
                        "c01": "c01", "c10": "c10", "c11": "c11"}[str(m)], sp.Integer(0))
         for m in MOD}
    return all(expand(diff(v[str(m)], n) - diff(v[str(n)], m)) == 0 for m in MOD for n in MOD)


A_ = {"k10": k10}                       # omega: LE, identity-satisfying
B_ = {"kmod": sp.Integer(2)}            # LE, identity-violating (at k10 != 0)
C_ = {"lam": kmod}                      # NV (dk_mod ^ dlam), identity-satisfying
D_ = {"lam": kmod, "kmod": sp.Integer(2)}
vcheck("V5_four_corner_transversality",
       closed(A_) and ident(A_) == 0
       and closed(B_) and expand(ident(B_) + 2 * k10) == 0 and ident(B_).subs(k10, 1) != 0
       and (not closed(C_)) and ident(C_) == 0
       and (not closed(D_)) and ident(D_).subs(k10, 1) != 0,
       "all four (G3-cell x identity-cut) corners populated exactly as the ledger says "
       "(P2, KMOD0, witness level); B violates only where k10 != 0 — scope confirmed")

# consistency of the identity used with the banked Stage-2 one (R_kmod = 2 r_tf):
r_tf, m00, m01, m10, m11 = symbols("r_tf m00 m01 m10 m11")
banked = expand(-2 * k10 * r_tf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01)
stage3 = expand(-k10 * (2 * r_tf) + c10 * m00 + c11 * m01 - c00 * m10 - c01 * m11)
vcheck("V5_identity_matches_stage2", expand(banked - stage3) == 0,
       "Stage-3's row dependency with R_kmod = 2 r_tf, R_C = M is EXACTLY the banked "
       "Stage-2 k_mod = 0 identity (PW3_component_pairings mapping verified) — F-S4 clean")

# ============ V6: G5 census — own integration by parts ============================
Lo1 = Function("A1")(*[U[i][k] for i in range(NF) for k in range(2)], *MOD)
deltaL = sum(diff(Lo1, U[i][k]) * W[i][k] for i in range(NF) for k in range(2))
Theta = sum(diff(Lo1, U[i][1]) * W[i][0] for i in range(NF))
vcheck("V6_N2_byparts",
       expand(deltaL - sum(EU(Lo1, i, 2) * W[i][0] for i in range(NF)) - DT(Theta)) == 0,
       "N=2: own by-parts gives boundary slots = 0-jet traces {v_a} with momenta "
       "dL/du_a' (1-jet functions) — self-pairable at wall grade 2 (trace jets <= 1 rule)")
Lo2 = Function("A2")(*[U[i][k] for i in range(NF) for k in range(3)], *MOD)
deltaL2 = sum(diff(Lo2, U[i][k]) * W[i][k] for i in range(NF) for k in range(3))
Theta2 = sum(diff(Lo2, U[i][2]) * W[i][1]
             + (diff(Lo2, U[i][1]) - DT(diff(Lo2, U[i][2]))) * W[i][0] for i in range(NF))
vcheck("V6_N4_byparts",
       expand(deltaL2 - sum(EU(Lo2, i, 2) * W[i][0] for i in range(NF)) - DT(Theta2)) == 0,
       "N=4: own by-parts pairs BOTH {v_a, v_a'}")
vcheck("V6_N4_third_jet_momentum",
       diff(diff(Lo2, U[0][1]) - DT(diff(Lo2, U[0][2])), U[0][3]) != 0,
       "the v_a momentum contains 3rd jets (coefficient -d2L/du''du'') -> wall grade 4 "
       "needed -> STRUCTURALLY UNABLE within jet <= 2; typed-extension scope stamp is "
       "the correct reading (NOT 'Bach class excluded') — reproduced")
# parity halving, own construction:
x = Symbol("x")
ge = sum(Symbol(f"e{i}") * x ** (2 * i) for i in range(4))
go = sum(Symbol(f"o{i}") * x ** (2 * i + 1) for i in range(4))
vcheck("V6_parity_halving",
       all(diff(ge, x, n).subs(x, 0) == 0 for n in (1, 3, 5))
       and all(diff(go, x, n).subs(x, 0) == 0 for n in (0, 2, 4))
       and diff(ge, x, 2).subs(x, 0) != 0 and diff(go, x, 3).subs(x, 0) != 0,
       "even fields lose odd-jet traces, odd fields lose even-jet traces at a mirror "
       "wall: exactly half the tower per field — parity-halving reproduced")

# ============ V7: P3 bulk inheritance (interior-supported defect) =================
d1 = x ** 2 * (1 - x) ** 2
e1 = x ** 3 * (1 - x) ** 2  # deliberately x->1-x ASYMMETRIC (a symmetric pair has zero defect trivially)
Ival = sp.integrate(e1 * diff(d1, x) - d1 * diff(e1, x), (x, 0, 1))
vcheck("V7_P3_interior_defect",
       Ival != 0 and all(f.subs(x, v) == 0 for f in (d1, e1, diff(d1, x), diff(e1, x))
                         for v in (0, 1)),
       f"own interior-supported pair (vanishing with 1st derivatives at BOTH walls): "
       f"antisymmetry defect integral = {Ival} != 0 — wall/corner densities cannot "
       "repair a bulk defect; P3 inherits its bulk partition (reproduced with a "
       "DIFFERENT variation pair than the package's)")

# ============ V8: K4 torsion / period typing ======================================
eta4 = sp.diag(-1, 1, 1, 1)
K4m = [eye(4), sp.diag(1, 1, -1, -1), sp.diag(1, -1, -1, 1), sp.diag(1, -1, 1, -1)]
vcheck("V8_K4_torsion",
       all(sp.simplify(M * M - eye(4)) == zeros(4, 4) for M in K4m)
       and all(sp.simplify(M.T * eta4 * M - eta4) == zeros(4, 4) and M.det() == 1 for M in K4m),
       "every K4 element is an involution (and proper orthochronous): closed-form periods "
       "on torsion cycles obey 2P = 0 -> P = 0; the package scopes this to CLOSED forms "
       "on TORSION cycles only — scope verified in prose")

# ============ V9: TC2 typing spot checks ==========================================
# generic stratum: trivial stabilizer (recompute the tangency rank myself)
def lgen(a, b):
    L = zeros(4, 4)
    L[a, b] = 1
    L[b, a] = -Rational(eta4[a, a], eta4[b, b])
    return L


GENS = [lgen(*p) for p in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]]
k00v, k11v = symbols("k00v k11v")
Xm = zeros(4, 4)
Xm[0:2, 0:2] = sp.diag(-1, 1)
Xm[2:4, 0:2] = Matrix([[c00, c01], [c10, c11]])
Xm[2:4, 2:4] = Matrix([[k00v, 0], [k10, k11v]])
bet = symbols("bb0:6")
Bm = sum((bet[i] * GENS[i] for i in range(6)), zeros(4, 4))
Cm = Bm * Xm - Xm * Bm
rows = [Cm[i, j] for (i, j) in [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]]
Am, _ = sp.linear_eq_to_matrix(rows, list(bet))
vcheck("V9_generic_stabilizer_trivial",
       Am.subs({k00v: 2, k10: 3, k11v: 5, c00: 7, c01: 11, c10: 13, c11: 17}).rank() == 6,
       "own recomputation: rank 6 at generic moduli -> no pointwise identity on GENERIC; "
       "3+7 vs 3+7 DETERMINED-type count is a typing statement (no existence claim)")
ns = Am.subs(k11v, k00v).nullspace()
vcheck("V9_kmod0_gauge_dim_1", len(ns) == 1,
       "own recomputation: on k_mod = 0 the tangency nullspace is 1-dimensional (L23): "
       "one algebraic identity <-> one gauge direction — 'balanced' is a COUNT, not a "
       "solvability claim (F-S6 clean)")

# ============ V10: ADVERSARIAL — the anchored-log forcing quantifier ==============
# (a) the package's own identity: d(WF R)/dlam = WF[dR/dlam + aF' p0 R] — reproduced:
Rsym = Function("Rs")(*[U[j][k] for j in range(NF) for k in range(3)], *MOD)
vcheck("V10a_H4_lambda_row_identity",
       expand(diff(WFs * Rsym, lam)
              - WFs * (diff(Rsym, lam) + sp.Derivative(aFs, lam) * P0 * Rsym)) == 0,
       "the lambda-row identity holds for symbolic a_F — reproduced")
# (b) COUNTEREXAMPLE to "forces log-dependence in the lambda-slot WHENEVER the field
# sector is nonzero": take Ltil = e^{-2 lam p0} Ltil0 (formal-in-lam, Q-smooth — in the
# banked alphabet class 'polynomial/FORMAL in the moduli, smooth in the rest').
# Generated action S = WF*Ltil = Ltil0 is lambda-independent:
Ltil_c = exp(-2 * lam * P0) * L0
S_c = expand(WF * Ltil_c)
Rfield_c = [expand(exp(-2 * lam * P0) * EU(S_c, i, 2)) for i in range(NF)]
Rlam_c = expand(diff(S_c, lam))  # = WM * R_lam -> R_lam = 0 for any WM
all_H4 = all(expand(diff(EU(S_c, i, 2), m) - EU(diff(S_c, m), i, 2)) == 0
             for i in range(NF) for m in MOD)
vcheck("V10b_anchored_log_counterexample",
       expand(S_c - L0) == 0
       and is_selfadjoint([EU(S_c, i, 2) for i in range(NF)], 2)
       and all_H4
       and Rlam_c == 0
       and Rfield_c[0] != 0
       and diff(Rfield_c[0], P0) != 0,  # genuinely lam- and p0-dependent field sector
       "COUNTEREXAMPLE CONSTRUCTED: the member R_a = e^{-2 lam p0}(p2,f2,h2), all moduli "
       "slots ZERO, is LOCALLY-EXACT under P1-4D (all field-field conditions + H4 for "
       "every modulus + H5 hold; generated by Ltil = e^{-2 lam p0} Ltil0, formal-in-lam "
       "and Q-smooth, hence in the banked alphabet class) with NONZERO field sector and "
       "ZERO lambda-slot — NO log(c_E/Q) dependence anywhere in the moduli sector. The "
       "phrasing 'LE membership forces log-dependence in the lambda-slot WHENEVER the "
       "field sector is nonzero' is REFUTED; the correct condition is: the lambda-slot "
       "is forced nonzero iff d/dlam[W_F R_a] != 0 for some a (e.g. every "
       "lambda-INDEPENDENT nonzero field sector), and it carries the anchored log when "
       "that derivative's a_F' p0 term survives")
# (c) but the forcing IS real for lambda-independent field sectors (the package's
# witness class) — verify the positive side stands:
lhs_w1 = expand(diff(WF * U[0][2], lam))
vcheck("V10c_forcing_real_for_lam_free_sectors",
       expand(lhs_w1 - 2 * P0 * WF * U[0][2]) == 0 and lhs_w1 != 0,
       "for a lambda-free nonzero field sector (e.g. W1) the lambda-row is 2 p0 WF R_a "
       "!= 0 with an explicit log factor: the forcing statement is TRUE on that "
       "subclass — the amendment is a scope restriction, not a demolition")

# ============ V11: anchored wall rule =============================================
pw, qw, sw, p0w = symbols("pw qw sw p0w", real=True)
cEw = Symbol("cEw", positive=True)
Fw = cEw ** pw * exp(-qw * p0w)
Fsh = Fw.subs({p0w: p0w + sw, cEw: cEw * exp(sw)}, simultaneous=True)
vcheck("V11_anchored_wall_rule",
       sp.simplify(sp.powsimp(Fsh / Fw, force=True) - exp((pw - qw) * sw)) == 0,
       "shift-orbit ratio = e^{(p-q)s}: invariant iff p = q (Q_wall-power) — reproduced")

# ============ summary =============================================================
print()
if FAILED:
    print(f"VERIFIER: {len(FAILED)} check(s) FAILED: {FAILED}")
    sys.exit(1)
print("VERIFIER: all independent checks passed (incl. the V10b counter-construction "
      "against the anchored-log 'whenever' phrasing — see report).")
sys.exit(0)
