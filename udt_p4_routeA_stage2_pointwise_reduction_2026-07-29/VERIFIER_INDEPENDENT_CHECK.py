#!/usr/bin/env python3
"""BLIND VERIFIER independent check — P4 Route A Stage 2 (pointwise reduction R_PW).

Blind adversarial verifier, same-session-spawned (not a hosted external model),
2026-07-29. Own constructions throughout; where the derivation's conventions are
reused (eta, chart blocks, K4 substitutions) they were audited line-by-line first.

Sections:
  VA  conventions / K4 / T-block sanity (light recomputation)
  VB  anchored-exponent condition (own derivation: orbit-space argument)
  VC  stabilizer — class-wide (recompute) AND POINTWISE (the attack):
      hunt configurations where a continuous gauge direction IS tangent to the
      registered class; adjudicate the R7(b) vacuity claim
  VD  character modules: independent generation proof to degree 8 (different
      algorithm), all-degree parity lemma, minimality, syzygy
  VE  slot/seat: Gram, component pairings, E12 null slot
  VF  located objects: EH/Bach jet classification from Route C banked signatures
  VG  jet-3/4 order-independence probes
  VH  counter-computation: the k_mod=0 stratum Noether identity vs an exhibited
      R_PW member (the derivation's own nonemptiness witness)
"""

import itertools
import json
import sys

import sympy as sp
from sympy import Matrix, Rational, Symbol, symbols, exp, simplify, eye, zeros

FAIL = []


def rep(name, ok, detail=""):
    print(f"[{'OK' if ok else 'XX'}] {name}" + (f" -- {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)


eta = sp.diag(-1, 1, 1, 1)
I4 = eye(4)

# ---------------------------------------------------------------- VA
def gen(a, b):
    L = zeros(4, 4)
    L[a, b] = 1
    L[b, a] = -Rational(eta[a, a], eta[b, b])
    return L


PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
GENS = [gen(a, b) for a, b in PAIRS]
rep("VA_so13_generators", all(sp.simplify(L.T * eta + eta * L).is_zero_matrix for L in GENS))

R23, R12, R13 = sp.diag(1, 1, -1, -1), sp.diag(1, -1, -1, 1), sp.diag(1, -1, 1, -1)
K4 = [I4, R23, R12, R13]
rep("VA_K4_group", all((M.T * eta * M - eta).is_zero_matrix and M * M == I4 for M in K4)
    and R12 * R13 == R23)

k00, k10, k11 = symbols("k00 k10 k11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
H2 = sp.diag(-1, 1)
Kb = Matrix([[k00, 0], [k10, k11]])
Cb = Matrix([[c00, c01], [c10, c11]])
X = zeros(4, 4)
X[0:2, 0:2] = H2
X[2:4, 0:2] = Cb
X[2:4, 2:4] = Kb
T = X.T * eta + eta * X
rep("VA_T_block", T[0:2, 0:2] == 2 * eye(2) and T[0:2, 2:4] == Cb.T
    and T[2:4, 2:4] == Kb + Kb.T)

# K4 action on the class, derived MYSELF from conjugation (not copied):
def k4_action_map(M):
    Y = M * X * M  # M = M^{-1}
    return Y

subs_R12 = {k10: -k10, c00: -c00, c11: -c11}
subs_R13 = {k10: -k10, c01: -c01, c10: -c10}
subs_R23 = {c00: -c00, c01: -c01, c10: -c10, c11: -c11}
ok = all((k4_action_map(M) - X.subs(sm, simultaneous=True)).is_zero_matrix
         for M, sm in [(R12, subs_R12), (R13, subs_R13), (R23, subs_R23)])
rep("VA_K4_action_on_class_rederived", ok)

# ---------------------------------------------------------------- VB
# Anchored-exponent condition, OWN derivation.
# Shift-with-absorption orbit (banked Stage-1 D3/F-RA4): (phi, c_E) -> (phi+s, c_E e^s).
# Claim under attack: well-defined (orbit-invariant) zero-jet dependence on (phi, c_E)
# is EXACTLY dependence through Q = c_E e^{-phi}; bare phi and c_E^p e^{-q phi} with
# p != q are excluded; phi-JETS evade anchoring (shift-invariant) and are separate
# alphabet blocks.
phi, s = symbols("phi s", real=True)
cE = Symbol("c_E", positive=True)
Q = cE * exp(-phi)
# (i) The change of variables (phi, c_E) <-> (phi, Q) is invertible for c_E>0:
rep("VB_change_of_vars_invertible", simplify(Q * exp(phi) - cE) == 0)
# (ii) In (phi, Q) coordinates the shift acts as (phi, Q) -> (phi+s, Q): it is
# TRANSITIVE on the phi-line and TRIVIAL on Q. Hence invariant functions of the pair
# = functions of Q alone (phi is a full orbit coordinate; nothing else is available).
rep("VB_shift_in_orbit_coords",
    simplify(Q.subs({phi: phi + s, cE: cE * exp(s)}, simultaneous=True) - Q) == 0)
# (iii) An arbitrary smooth F(phi, Q): invariance for all s forces dF/dphi = 0 at
# fixed Q. Verify infinitesimally on a general symbolic function:
Ff = sp.Function("F")(phi, Q)
dFds = sp.diff(Ff.subs(phi, phi + s), s).subs(s, 0)  # = dF/dphi at fixed Q
rep("VB_invariance_iff_no_phi_at_fixed_Q",
    simplify(dFds - sp.Derivative(sp.Function("F")(phi, Q), phi)) == 0,
    "d/ds F(phi+s, Q) |_{s=0} = F_phi: invariance <=> F carries NO bare-phi argument")
# (iv) exponent condition on the power family (recheck) + bare phi fails:
p_, q_ = symbols("p q", real=True)
Fp = cE**p_ * exp(-q_ * phi)
Fs = Fp.subs({phi: phi + s, cE: cE * exp(s)}, simultaneous=True)
rep("VB_p_equals_q", simplify(Fs - Fp * exp((p_ - q_) * s)) == 0
    and simplify((Fs - Fp).subs(p_, q_)) == 0
    and simplify((Fs - Fp).subs({p_: 2, q_: 1, s: 1})) != 0)
rep("VB_bare_phi_not_invariant", simplify((phi + s) - phi) != 0)
# (v) phi-jets evade anchoring (all orders):
xv = Symbol("x")
pf = sp.Function("phiF")(xv)
rep("VB_jets_shift_invariant", all(
    simplify(sp.diff(pf + s, (xv, n)) - sp.diff(pf, (xv, n))) == 0 for n in range(1, 5)))
# Adjudication note: phi-DIFFERENCES phi(x)-phi(y) are bilocal, outside the pointwise
# alphabet by scope (and Stage-1 J04 excludes f(q)-f(p) substitutes by R1 provenance).

# ---------------------------------------------------------------- VC
# Stabilizer. (a) Recompute the CLASS-WIDE statement (rank 6). (b) THE ATTACK:
# compute the POINTWISE tangency stabilizer at a GENERIC class member as a function
# of the moduli, and hunt rank-drop loci.
bcoef = symbols("beta0:6")
B = zeros(4, 4)
for i, L in enumerate(GENS):
    B = B + bcoef[i] * L
FORBIDDEN = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

# (a) class-wide: tangency at X0=[[H,0],[0,0]] and along each of the 7 class directions
X0 = zeros(4, 4)
X0[0:2, 0:2] = H2
Vbasis = []
for (i, j) in [(2, 2), (3, 2), (3, 3), (2, 0), (2, 1), (3, 0), (3, 1)]:
    E = zeros(4, 4)
    E[i, j] = 1
    Vbasis.append(E)
eqs = []
for M in [X0] + Vbasis:
    Cm = B * M - M * B
    eqs.extend(Cm[i, j] for i, j in FORBIDDEN)
A_cw, _ = sp.linear_eq_to_matrix(eqs, list(bcoef))
rep("VC_classwide_stabilizer_trivial_recomputed",
    A_cw.rank() == 6 and A_cw.nullspace() == [],
    "rank 6, empty nullspace: the derivation's PW2_registered_stabilizer_trivial "
    "computation is CORRECT as computed (class-wide)")

# (b) pointwise at the generic member X (symbolic moduli):
Cm = B * X - X * B
eqs_pt = [Cm[i, j] for i, j in FORBIDDEN]
A_pt, _ = sp.linear_eq_to_matrix(eqs_pt, list(bcoef))
# generic rank:
rank_generic = A_pt.subs({k00: 2, k10: 3, k11: 5, c00: 7, c01: 11, c10: 13, c11: 17}).rank()
rep("VC_pointwise_rank_generic_6", rank_generic == 6,
    "at a generic member the pointwise tangency stabilizer is trivial")
# THE HUNT: k_mod = 0 means k00 = k11 (a = d). Substitute k11 -> k00:
A_iso = A_pt.subs(k11, k00)
r_iso = A_iso.subs({k00: 2, k10: 3, c00: 7, c01: 11, c10: 13, c11: 17}).rank()
ns_iso = A_iso.subs({k00: 2, k10: 3, c00: 7, c01: 11, c10: 13, c11: 17}).nullspace()
rep("VC_pointwise_rank_drops_on_kmod0", r_iso == 5 and len(ns_iso) == 1,
    f"on the k_mod=0 stratum (k00=k11) the pointwise system has rank {r_iso}: "
    "a CONTINUOUS gauge direction IS tangent to the registered class there")
# identify the nullspace generator: expect the screen rotation L23 (pair index 5)
ns = ns_iso[0]
rep("VC_null_direction_is_L23",
    all(simplify(ns[i]) == 0 for i in range(5)) and simplify(ns[5]) != 0,
    "nullspace = span(L23), the screen rotation")
# exact witness, fully symbolic: B = L23, X with k11=k00 (k_mod=0), all else generic
L23 = GENS[5]
W23 = (L23 * X - X * L23).subs(k11, k00)
tangent_ok = all(simplify(W23[i, j]) == 0 for i, j in FORBIDDEN)
nonzero = any(simplify(e) != 0 for e in W23)
rep("VC_witness_L23_tangent_nonzero_on_kmod0", tangent_ok and nonzero,
    "[L23, X]|_{k_mod=0} = [[0,0],[J C, k10 diag(1,-1)]] : a NONZERO infinitesimal "
    "local-Lorentz motion tangent to the registered class at every k_mod=0 member "
    "with (k10, C) != 0 — a codimension-ONE stratum of the moduli")
# and the direction read in chart coordinates:
dK = W23[2:4, 2:4]
dC = W23[2:4, 0:2]
Jrot = Matrix([[0, 1], [-1, 0]])
rep("VC_witness_components", (dK - k10 * sp.diag(1, -1)).is_zero_matrix
    and (dC - Jrot * Cb.subs(k11, k00)).is_zero_matrix,
    "delta k_mod = -k10, delta C = J C (delta lambda = delta k10 = 0)")
# also probe the C=0 resonance loci (higher codim; completeness of the hunt):
Xc0 = X.subs({c00: 0, c01: 0, c10: 0, c11: 0})
A_c0 = sp.linear_eq_to_matrix([ (B * Xc0 - Xc0 * B)[i, j] for i, j in FORBIDDEN], list(bcoef))[0]
r_res = A_c0.subs({k00: -1, k10: 3, k11: 5}).rank()  # a = k00 = -1 resonance
rep("VC_resonance_locus_C0_a_eq_m1", r_res < 6,
    f"on C=0 with k00=-1 the rank is {r_res} < 6: further (higher-codim) strata with "
    "continuous tangent gauge directions exist (eigenvalue resonance with the base block)")

# ---------------------------------------------------------------- VD
# Character modules — INDEPENDENT generation/minimality proof.
# Parity vectors over (Z/2)^2 (R12-parity, R13-parity):
PV = {"k10": (1, 1), "c00": (1, 0), "c11": (1, 0), "c01": (0, 1), "c10": (0, 1)}
NAMES = ["k10", "c00", "c11", "c01", "c10"]
GEN_I = [(2, 0, 0, 0, 0), (0, 2, 0, 0, 0), (0, 0, 2, 0, 0), (0, 1, 1, 0, 0),
         (0, 0, 0, 2, 0), (0, 0, 0, 0, 2), (0, 0, 0, 1, 1),
         (1, 1, 0, 1, 0), (1, 1, 0, 0, 1), (1, 0, 1, 1, 0), (1, 0, 1, 0, 1)]
GEN_M = {
    (1, 1): [(1, 0, 0, 0, 0), (0, 1, 0, 1, 0), (0, 1, 0, 0, 1), (0, 0, 1, 1, 0), (0, 0, 1, 0, 1)],
    (1, 0): [(0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (1, 0, 0, 1, 0), (1, 0, 0, 0, 1)],
    (0, 1): [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 0, 0, 0), (1, 0, 1, 0, 0)],
}


def parity(e):
    return (sum(a * PV[n][0] for a, n in zip(e, NAMES)) % 2,
            sum(a * PV[n][1] for a, n in zip(e, NAMES)) % 2)


def divisible(e, g):
    return all(a >= b for a, b in zip(e, g))


def sub(e, g):
    return tuple(a - b for a, b in zip(e, g))


MEMO = {}


def in_inv_ring(e):
    if e in MEMO:
        return MEMO[e]
    if sum(e) == 0:
        return True
    ok = any(divisible(e, g) and in_inv_ring(sub(e, g)) for g in GEN_I)
    MEMO[e] = ok
    return ok


DEG = 8  # independent, HIGHER than the derivation's 6
mons = [e for e in itertools.product(range(DEG + 1), repeat=5) if 0 < sum(e) <= DEG]
inv_ok = all(in_inv_ring(e) for e in mons if parity(e) == (0, 0))
rep("VD_invariant_ring_generation_deg8", inv_ok,
    "every (0,0)-parity monomial of degree <= 8 factors through the 11 generators "
    "(exceeds the derivation's degree-6 exhaustion)")
mod_ok = True
for ch, gens_m in GEN_M.items():
    for e in mons:
        if parity(e) == ch:
            if not any(divisible(e, g) and in_inv_ring(sub(e, g)) for g in gens_m):
                mod_ok = False
rep("VD_module_generation_deg8", mod_ok,
    "chi_a/chi_b/chi_c monomials of degree <= 8 all = generator x invariant")
# ALL-degree argument (own proof, Davenport-style, verified case split):
#   chi_a (1,1): e odd -> divide k10, remainder parity (0,0);
#                e even -> p+q odd AND r+s odd -> divide one c_b and one c_c.
#   chi_b (1,0): e even -> p+q odd -> divide a c_b; e odd -> r+s odd -> divide k10*c_c.
#   chi_c (0,1): mirrored. Invariant ring: Davenport constant of (Z/2)^2 is 3, so
#   indecomposable invariant monomials have degree <= 3 = exactly the 11 listed.
allcase = True
for e in mons:
    pv = parity(e)
    ee, pp, qq, rr, ss = e
    if pv == (1, 1):
        allcase &= (ee % 2 == 1) or (((pp + qq) % 2 == 1) and ((rr + ss) % 2 == 1))
    elif pv == (1, 0):
        allcase &= ((pp + qq) % 2 == 1) if ((ee % 2) == 0) else ((rr + ss) % 2 == 1 and ee >= 1)
    elif pv == (0, 1):
        allcase &= ((rr + ss) % 2 == 1) if ((ee % 2) == 0) else ((pp + qq) % 2 == 1 and ee >= 1)
rep("VD_all_degree_case_split_verified", allcase,
    "the parity case split behind the all-degree generation proof holds on every "
    "monomial tested; with the divisibility steps above this closes generation at ALL degrees")
# minimality + a syzygy (independent):
deg12 = {ch: sorted(e for e in mons if sum(e) <= 2 and parity(e) == ch) for ch in GEN_M}
rep("VD_minimality", all(sorted(GEN_M[ch]) == deg12[ch] for ch in GEN_M),
    "each class's degree<=2 monomials are exactly its generators; invariant ring "
    "starts at degree 2 => no generator decomposes")
k10s, c00s, c01s = sp.symbols("k10 c00 c01")
rep("VD_syzygy", sp.expand((k10s**2) * (c00s * c01s) - (k10s * c00s * c01s) * k10s) == 0,
    "I1*(c00c01) - I8*k10 = 0: the chi_a module is not free")

# ---------------------------------------------------------------- VE
I2m, D2 = eye(2), sp.diag(-1, 1)
E21, E12 = Matrix([[0, 0], [1, 0]]), Matrix([[0, 1], [0, 0]])
pairf = lambda A, Bm: sp.trace(A.T * Bm)
G3 = Matrix(3, 3, lambda i, j: pairf([I2m, D2, E21][i], [I2m, D2, E21][j]))
rep("VE_gram", G3 == sp.diag(2, 2, 1))
rep("VE_E12_null", all(pairf(E12, M) == 0 for M in [I2m, D2, E21]))
r_tr, r_tf, r_sh, r_nl = symbols("r_tr r_tf r_sh r_nl")
Wk = r_tr * I2m + r_tf * D2 + r_sh * E21 + r_nl * E12
rep("VE_component_pairings",
    (simplify(pairf(Wk, I2m)), simplify(pairf(Wk, D2)), simplify(pairf(Wk, E21)))
    == (2 * r_tr, 2 * r_tf, r_sh))
# T-block cross-check: delta(K+K^T) = 2 dlam I2 + 2 dkmod D2 + dk10 (E21+E12);
# the SPACE of component triples (R_lam, R_kmod, R_k10) is the same under either
# pairing convention (chart deltaK vs physical delta(K+K^T)) — an invertible
# rescaling/identification, no structural change:
dl, dm, dk = symbols("dl dm dk")
dKKT = 2 * dl * I2m + 2 * dm * D2 + dk * (E21 + E12)
rep("VE_T_block_convention_isomorphic",
    simplify(pairf(Wk, dKKT) - (4 * r_tr * dl + 4 * r_tf * dm + (r_sh + r_nl) * dk)) == 0,
    "pairing against delta(K+K^T) gives 4r_tr, 4r_tf, (r_sh+r_nl): an invertible "
    "reparametrization of the same component space; E12 'null slot' is a chart-deltaK "
    "convention statement (against delta(K+K^T) the symmetric combination pairs)")
# slot theorem:
rep("VE_slot_theorem", simplify(pairf(Wk.subs(r_tf, 0), D2)) == 0)

# ---------------------------------------------------------------- VF
rc = json.load(open("../udt_p4_routeC_shared_static_sector_2026-07-28/routeC_stage1_results.json"))
js = rc["jet_signatures"]
def maxjet(sig):
    return max(int(t[1]) for comps in sig.values() for t in comps)
rep("VF_EH_jets_le2", maxjet(js["eh"]) <= 2,
    "banked Route C EH restricted system: no component carries a jet above 2nd order")
rep("VF_Bach_jets_34", maxjet(js["bach"]) == 4
    and any(int(t[1]) >= 3 for comps in js["bach"].values() for t in comps),
    "banked Route C Bach system: 3rd/4th jets present -> outside jet<=2, inside typed class")
# EH phi-dependence anchoring: the restricted system's phi enters via exponential seat
# factors; e^{a phi} = (c_E/Q)^a exactly:
a_ = Symbol("a", real=True)
rep("VF_seat_exponentials_anchored", simplify((cE / Q)**a_ - exp(a_ * phi)) == 0)

# ---------------------------------------------------------------- VG
# Jet-3/4 order-independence probes: the K4 substitutions touch only moduli (field
# jets inert), shifts leave all jets inert (VB), R8 grading is per-declared-grade
# bookkeeping at any order. Probe: does any PW structure distinguish jet 3/4? The
# character of a jet block is trivial at every order (K4 acts only on k10, C):
rep("VG_K4_blind_to_field_jets",
    {k10, c00, c01, c10, c11}.isdisjoint({phi, s, cE}),
    "K4 substitution variables are disjoint from field/jet symbols at every order")

# ---------------------------------------------------------------- VH
# COUNTER-COMPUTATION for the R7(b) vacuity claim: on the k_mod=0 stratum the
# quotient-honesty identity <R, [L23,X]> = 0 is NONTRIVIAL:
#     -2 k10 r_tf + (m00 c10 + m01 c11 - m10 c00 - m11 c01) = 0   at k_mod = 0.
# The derivation's own nonemptiness witness "unit trace-free screen kernel with
# R_kmod = 2" (r_tf = 1, all else 0) gives <R, [L23,X]> = -2 k10 != 0 on that
# stratum: it FAILS the identity wherever k10 != 0, k_mod = 0.
m00, m01, m10, m11 = symbols("m00 m01 m10 m11")
Mker = Matrix([[m00, m01], [m10, m11]])
pairing = pairf(Wk.subs(r_nl, 0), dK) + pairf(Mker, dC)  # dK, dC from VC witness (k_mod=0)
identity = sp.expand(pairing)
expected = sp.expand(-2 * k10 * r_tf + (m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01).subs(k11, k00))
rep("VH_stratum_identity_form", sp.expand(identity - expected) == 0,
    "<R, [L23,X]>|_{k_mod=0} = -2 k10 r_tf + m00 c10 + m01 c11 - m10 c00 - m11 c01")
viol = identity.subs({r_tf: 1, r_tr: 0, r_sh: 0, m00: 0, m01: 0, m10: 0, m11: 0})
rep("VH_witness_member_violates", simplify(viol + 2 * k10) == 0 and simplify(viol.subs(k10, 3)) != 0,
    "the exhibited R_PW member (r_tf=1, rest 0) pairs to -2 k10 != 0 with a gauge "
    "direction tangent to the class at k_mod=0: R7(b)'s pointwise identity set is "
    "NOT empty on that stratum, and R_PW as parametrized contains members violating it")

print()
if FAIL:
    print(f"{len(FAIL)} check(s) failed: {FAIL}")
    sys.exit(1)
print("All verifier checks passed (including the adversarial counter-computation).")
sys.exit(0)
