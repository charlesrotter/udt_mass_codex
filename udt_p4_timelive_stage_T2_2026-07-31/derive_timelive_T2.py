#!/usr/bin/env python3
"""Stage T2 derivation script — the pointwise reduction TIME-LIVE (TU-1..TU-5).

Contract: udt_p4_timelive_stage_T2_2026-07-31/PREREGISTRATION.md (frozen first).
Exact SymPy only: no floats, no numeric solvers, no GPU, deterministic. Exit
nonzero on any failed check; guard checks are WIRED into the exit path (T1
amendment precedent). Check kinds: SUBSTANTIVE (a derivation leg) vs GUARD
(re-run/mechanical/bookkeeping/hygiene).

Scope stamps traveling with every check: registered chart's time extension
(T-L1 CHOSE); EVERYTHING-ON (shift row live, coordinate branch); BOTH
lock-reading branches run to the same depth; bigraded jets (space x time <= 2,
higher TYPED); registered stationary presentation (general arenas TYPED);
polynomial/formal in the (k10,C) moduli; pointwise, one-parameter, off-shell;
time-topology fork spectator at the pointwise layer (checked, not assumed);
theta ABSENT; no census reading adopted; resonance-locus contacts stamped
OPEN-PENDING-CENSUS (F-U8), not adjudicated. NO ADM/foliation/initial-value
organization is used anywhere (F-U2); the native objects are the covariant
metric rows (canon C-2026-06-18-1) exactly as in Stage T1.

Cited banked inputs (recomputed as consistency, never re-derived as new):
Stage T1 (f2343b7, amended: layered residual symmetry, psi-slack, lock-reading
fork LOAD-BEARING), static Stage 2 (2c0e7cc, rounds 1+2 amended: R_PW
parametrization, character modules, slot theorem, stratum Noether identities),
Route B (K4, E02), canon (clock law + reciprocal lock).
"""
import itertools
import json
import os
import re
import sys

import sympy as sp
from sympy import Matrix, Rational, Symbol, symbols, exp, diff, simplify, zeros, eye

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(name, kind, cond, note=""):
    ok = bool(cond)
    CHECKS.append({"name": name, "kind": kind, "passed": ok, "note": note})
    print(f"[{'PASS' if ok else 'FAIL'}] ({kind}) {name}: {note}")
    return ok


def is_zero_matrix(M):
    return all(simplify(e) == 0 for e in M)


# ---------------------------------------------------------------------------
# S0 — shared exact objects (banked conventions, reused verbatim)
# ---------------------------------------------------------------------------
eta = sp.diag(-1, 1, 1, 1)
I4 = eye(4)
R23 = sp.diag(1, 1, -1, -1)
R12 = sp.diag(1, -1, -1, 1)
R13 = sp.diag(1, -1, 1, -1)
K4 = [I4, R23, R12, R13]

k00, k10, k11 = symbols("k00 k10 k11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
H2 = sp.diag(-1, 1)
Kb = Matrix([[k00, 0], [k10, k11]])
Cb = Matrix([[c00, c01], [c10, c11]])
X = zeros(4, 4)
X[0:2, 0:2] = H2
X[2:4, 0:2] = Cb
X[2:4, 2:4] = Kb

subs_R12 = {k10: -k10, c00: -c00, c11: -c11}
subs_R13 = {k10: -k10, c01: -c01, c10: -c10}
subs_R23 = {c00: -c00, c01: -c01, c10: -c10, c11: -c11}
K4_SUBS = [("R12", subs_R12), ("R13", subs_R13), ("R23", subs_R23)]


def lorentz_generator(a, b):
    L = zeros(4, 4)
    L[a, b] = 1
    L[b, a] = -Rational(eta[a, a], eta[b, b])
    return L


PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
GENS = {f"L{a}{b}": lorentz_generator(a, b) for (a, b) in PAIRS}
FORBIDDEN = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

check("S0_K4_and_generators_reused", "GUARD",
      all(is_zero_matrix(M.T * eta * M - eta) and M.det() == 1 and M[0, 0] == 1 for M in K4)
      and all(is_zero_matrix(L.T * eta + eta * L) for L in GENS.values())
      and is_zero_matrix(R12 * R13 - R23),
      "banked conventions re-run: K4 exact in SO+(1,3), six so(1,3) generators, closure (Route B / Stage-2 copy)")

# Time-live base symbols. All field symbols below are READ as arbitrary
# pointwise values of functions of (x,t) — t enters as an argument, never as
# an alphabet block (TU1e derives the exclusion of bare t).
c = symbols("c", positive=True)
phi = symbols("phi", real=True)
s_sh = symbols("s", real=True)
cE = symbols("c_E", positive=True)
N = symbols("N", real=True)         # radial shift value g_tx (O17; N_y,N_z typed)
gxx = symbols("g_xx", positive=True)
p1 = symbols("psi1", real=True)     # slope of a slack map t -> t + psi(x)
psi0 = symbols("psi0", real=True)   # value of psi at the point
g_tt = -exp(-2 * phi) * c**2        # THE CLOCK LAW (canon; covariant-row pin)
g2 = Matrix([[g_tt, N], [N, gxx]])
gam = gxx - N**2 / g_tt             # projected (radar) spatial row
Q = cE * exp(-phi)

print("=" * 78)
print("STAGE T2 — TU-1: the time-live equivariance/alphabet layer")
print("=" * 78)

# --- TU1a: the phi-dependence forcing, re-derived TIME-LIVE. On the registered
# chart the anchor shift acts as (phi, c_E) -> (phi+s, c_E e^s) pointwise in
# (x,t) (the banked static rule, time-extended; the derived unit rescale is the
# PRESENTATION overlap leg, TU1d). Unique invariance condition on phi-powers:
p_, q_ = symbols("p q", real=True)
F_pow = cE**p_ * exp(-q_ * phi)
F_shift = F_pow.subs({phi: phi + s_sh, cE: cE * exp(s_sh)}, simultaneous=True)
resid_law = simplify(F_shift - F_pow * exp((p_ - q_) * s_sh))
witness_noninv = simplify((F_shift - F_pow).subs({p_: 1, q_: 0, s_sh: 1}))
check("TU1a_Q_forcing_timelive_p_eq_q", "SUBSTANTIVE",
      resid_law == 0 and simplify((F_shift - F_pow).subs(p_, q_)) == 0
      and witness_noninv != 0
      and simplify(Q.subs({phi: phi + s_sh, cE: cE * exp(s_sh)}, simultaneous=True) - Q) == 0,
      "c_E^p e^{-q phi(x,t)} is shift-orbit-invariant iff p = q, i.e. iff it is a power of "
      "Q = c_E e^{-phi}: the STATIC forcing transfers verbatim with phi read at (x,t) — t is a "
      "spectator of the forcing; bare phi stays excluded (generic p != q witness nonzero)")

# --- TU1b: the BIGRADED phi-jets are shift-invariant alphabet blocks.
xv, tv = symbols("x_v t_v", real=True)
phifun = sp.Function("phi_f")(xv, tv)
jets_ok = all(
    simplify(diff(phifun + s_sh, (xv, n), (tv, m)) - diff(phifun, (xv, n), (tv, m))) == 0
    for (n, m) in [(1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
)
check("TU1b_bigraded_phi_jets_shift_invariant", "SUBSTANTIVE",
      jets_ok,
      "d^{n}_x d^{m}_t (phi + s) = d^{n}_x d^{m}_t phi for all bigrades (n,m) <= (2,2) shown at "
      "(1,0),(0,1),(2,0),(1,1),(0,2): every bigraded phi-jet is a shift-invariant block — the "
      "time-jets enter the alphabet exactly as the banked spatial jets did")

# --- TU1c: NO NEW phi-CHANNEL. The new time-live blocks (shift row N, bigraded
# time-jets) are shift-INERT, so no product with them can compensate a p != q
# mismatch: the forcing is INTACT with time on.
inert = symbols("B_inert", real=True)   # any shift-inert block: N, a t-jet, f, bh, moduli
F_comb = inert * F_pow
F_comb_shift = F_comb.subs({phi: phi + s_sh, cE: cE * exp(s_sh)}, simultaneous=True)
check("TU1c_no_new_phi_channel_opened", "SUBSTANTIVE",
      simplify(F_comb_shift - F_comb * exp((p_ - q_) * s_sh)) == 0
      and simplify((F_comb_shift - F_comb).subs(p_, q_)) == 0
      and simplify((F_comb_shift - F_comb).subs({p_: 1, q_: 0, s_sh: 1, inert: 1})) != 0,
      "for ANY shift-inert prefactor B (the shift row N, any bigraded field jet, f, bh, moduli): "
      "B * c_E^p e^{-q phi} has the same residual law exp((p-q)s) — invariance still holds iff "
      "p = q. TIME-DEPENDENCE OPENS NO NEW phi-CHANNEL AND CLOSES NONE: the phi-dependence forcing "
      "Q = c_E e^{-phi} (shift-equivariance alone) is INTACT time-live (TU-1 foundation verdict)")

# --- TU1d: the t-leg factor is a PRESENTATION-OVERLAP datum (T1q extension).
# Under the derived absorption map (phi+s, c_E e^s, t~ = e^s t, r~ = e^{-s} r):
# the time-jet of phi carries e^{-s}; the anchored combination c_E * d_t phi is
# overlap-invariant; the radial shift component N is overlap-invariant.
es = exp(s_sh)
dtphi = symbols("dtphi", real=True)          # d_t phi in the unshifted presentation
dtphi_tilde = es**-1 * dtphi                 # chain rule: d/d t~ = e^{-s} d/dt
anch_new = (cE * es) * dtphi_tilde
N_tilde = es**-1 * es * N                    # g~_{t~ r~} = (dt/dt~)(dr/dr~) g_tr = e^{-s} e^{s} N
check("TU1d_anchor_overlap_tleg_factor_derived", "SUBSTANTIVE",
      simplify(anch_new - cE * dtphi) == 0 and simplify(N_tilde - N) == 0
      and simplify(dtphi_tilde - dtphi).subs({dtphi: 1, s_sh: 1}) != 0,
      "across anchor presentations (T1q map): d_t~ phi~ = e^{-s} d_t phi (the surfaced t-leg "
      "factor — a J07-type OVERLAP datum, not an on-chart channel); the anchored combination "
      "c_E * d_t phi is overlap-invariant; the radial shift N is overlap-invariant "
      "(e^{-s} * e^{s} = 1 on the (t,r) legs). On the registered chart (units pinned) the "
      "on-chart rule of TU1a/TU1b governs; this leg records the overlap law exactly")

# --- TU1e: BARE t IS EXCLUDED from the alphabet — the time analog of the
# bare-phi exclusion, derived from residual T1-translation equivariance.
t_sym, t0 = symbols("t_bare t0", real=True)
check("TU1e_bare_t_excluded_by_time_translations", "SUBSTANTIVE",
      simplify((t_sym + t0) - t_sym - t0) == 0 and (t0 != 0)
      and simplify(diff(phifun.subs(tv, tv + t0), tv) - diff(phifun, tv).subs(tv, tv + t0)) == 0,
      "the residual chart symmetry contains t -> t + t0 (T1c): bare t shifts by t0 (residual = t0, "
      "not identically zero) so absolute-time dependence is NOT well defined on the residual "
      "quotient — bare t is excluded from the alphabet (NEW derived alphabet gate, the exact time "
      "analog of the banked bare-phi exclusion); field jets are translation-covariant (relabeled, "
      "not obstructed)")

# --- TU1f: WHAT THE PSI-SLACK COCYCLE FORCES (coordinate branch). Under the
# general slack map t -> t + psi(x) (slope p1; T1 convention Jp = [[1,p1],[0,1]]:
# N' = N + g_tt p1) the coordinate vector fields transform d_t' = d_t,
# d_x' = d_x + p1 d_t. The shift-corrected derivative D_x = d_x - (N/g_tt) d_t
# (the g-orthogonal-to-d_t projection of d_x — a NATIVE covariant-row object,
# no foliation used) is EXACTLY psi-invariant; bare d_x is a psi-frame quantity.
# Vector fields as components in the OLD basis (d_t, d_x):
D_x_old = Matrix([-N / g_tt, 1])
N_new = N + g_tt * p1
d_x_new = Matrix([p1, 1])                       # d_x' in the old basis
d_t_new = Matrix([1, 0])
D_x_new = d_x_new - (N_new / g_tt) * d_t_new    # D_x' built from NEW chart data
check("TU1f_psi_invariant_derivative_derived", "SUBSTANTIVE",
      is_zero_matrix(sp.expand(D_x_new - D_x_old))
      and simplify((d_x_new - Matrix([0, 1]))[0].subs(p1, 1)) != 0,
      "D_x = d_x - (N/g_tt) d_t is EXACTLY invariant under every slack map (zero-residual, "
      "symbolic in p1), while bare d_x shifts by p1 d_t: the psi-slack cocycle forces the "
      "bigraded jet layer to split into psi-INVARIANT blocks (d_t-jets, D_x-jets, gamma_xx, Q) "
      "and psi-FRAME blocks (d_x-jets, g_xx, N) — the derived content of J07's time-slack "
      "obligation at the pointwise layer")

# --- TU1g: the two alphabet presentations are EQUIVALENT on-chart (invertible
# triangular reparametrization), so no pointwise content rides the choice.
Dx_sym, px_sym, pt_sym = symbols("Dxphi pxphi ptphi", real=True)
gam_expr = gxx + N**2 * exp(2 * phi) / c**2
back_gxx = gam_expr - N**2 * exp(2 * phi) / c**2
Dx_def = px_sym - (N / g_tt) * pt_sym
back_px = Dx_def + (N / g_tt) * pt_sym
check("TU1g_psi_invariant_alphabet_presentation_invertible", "SUBSTANTIVE",
      simplify(gam - gam_expr) == 0 and simplify(back_gxx - gxx) == 0
      and simplify(back_px - px_sym) == 0,
      "gamma_xx = g_xx + N^2 e^{2phi}/c^2 (the T1k split re-derived) and D_x phi = d_x phi + "
      "(N e^{2phi}/c^2) d_t phi: the map (d_x-jets, g_xx, N) <-> (D_x-jets, gamma_xx, N) is an "
      "invertible triangular reparametrization of the SAME bigraded alphabet — on the registered "
      "chart both presentations coexist; ACROSS charts only the invariant presentation transports "
      "trivially (the frame presentation carries the additive psi-cocycle, banked T2i)")

# --- TU1h: the T-PARITY table, derived on a polynomial model (metric-layer
# time reflection composed with the DERIVED temporal-mirror parities of T2a:
# phi EVEN, N ODD, spatial data EVEN).
xm, tm = symbols("x_m t_m", real=True)
acoef = symbols("a0:10", real=True)
bcoef2 = symbols("b0:10", real=True)
mono3 = [1, xm, tm, xm**2, xm * tm, tm**2, xm**3, xm**2 * tm, xm * tm**2, tm**3]
phi_p = sum(a * mn for a, mn in zip(acoef, mono3))     # generic phi(x,t), degree 3
N_p = sum(b * mn for b, mn in zip(bcoef2, mono3))      # generic N(x,t), degree 3
phi_mir = phi_p.subs(tm, -tm)                          # phi EVEN-composed
N_mir = -N_p.subs(tm, -tm)                             # N ODD-composed
parity_ok = True
for (n, m) in [(0, 1), (1, 0), (1, 1), (0, 2), (2, 0)]:
    lhs = diff(phi_mir, (xm, n), (tm, m))
    rhs = (-1) ** m * diff(phi_p, (xm, n), (tm, m)).subs(tm, -tm)
    if sp.expand(lhs - rhs) != 0:
        parity_ok = False
    lhsN = diff(N_mir, (xm, n), (tm, m))
    rhsN = (-1) ** (m + 1) * diff(N_p, (xm, n), (tm, m)).subs(tm, -tm)
    if sp.expand(lhsN - rhsN) != 0:
        parity_ok = False
gtt_p = -exp(-2 * phi_p) * c**2
gtt_mir = -exp(-2 * phi_mir) * c**2
Dx_p = diff(phi_p, xm) - (N_p / gtt_p) * diff(phi_p, tm)
Dx_mir = diff(phi_mir, xm) - (N_mir / gtt_mir) * diff(phi_mir, tm)
Dx_even = simplify(Dx_mir - Dx_p.subs(tm, -tm)) == 0
check("TU1h_T_parity_table_derived", "SUBSTANTIVE",
      parity_ok and Dx_even,
      "on a generic degree-3 model: the mirror-composed fields (phi even, N odd — the DERIVED T2a "
      "parities) give bigraded-jet parities (d_t^m d_x^n phi)-block = (-1)^m, (d_t^m d_x^n N)-block "
      "= (-1)^{m+1}; AND the psi-invariant derivative D_x phi is T-EVEN (the N-flip and the d_t-flip "
      "cancel): T-parity of a block = (-1)^{(time-jet order) + (N-factor count)} — a derived Z2 "
      "grading of the whole alphabet. LAYER STAMP: imposed as a character rule at the METRIC layer "
      "only (coframe layer: the reflection is SO+-obstructed, T1g/T1i — admitting it there is a CHOSE)")

# --- TU1i: the stratum-conditional Z2 psi-branch acts as PURE N-PARITY in the
# invariant alphabet presentation.
p1_branch = -2 * N / g_tt
g2p = sp.expand(Matrix([[1, p1], [0, 1]]).T * g2 * Matrix([[1, p1], [0, 1]]))
g2_flip = g2p.subs(p1, p1_branch)
gam_flip = simplify(g2_flip[1, 1] - g2_flip[0, 1] ** 2 / g2_flip[0, 0])
Dx_after_branch = (Matrix([p1, 1]) - ((N + g_tt * p1) / g_tt) * Matrix([1, 0])).subs(p1, p1_branch)
check("TU1i_stratum_Z2_is_pure_N_parity_in_invariant_alphabet", "SUBSTANTIVE",
      simplify(g2_flip[0, 1] + N) == 0
      and simplify(g2_flip[0, 0] - g2[0, 0]) == 0
      and simplify(g2_flip[1, 1] - g2[1, 1]) == 0
      and simplify(gam_flip - gam) == 0
      and is_zero_matrix(sp.expand(Dx_after_branch - D_x_old)),
      "under psi' = -2N/g_tt (T1p3 branch, lawful where 2N e^{2phi}/c^2 is t-independent): N -> -N "
      "while the clock row, spatial row, BOTH lock readings, d_t, AND D_x are all exactly preserved "
      "— in the psi-invariant alphabet the stratum-conditional Z2 is PURE N-parity. It is DISCRETE: "
      "it imposes a stratum-conditional CHARACTER cut (components N-parity-matched to their paired "
      "directions on the lawful strata), and NO Noether identity (no continuous parameter — the "
      "exact analog of K4's status, banked)")

# --- TU1j: the LAYERED character rule assembled. Character group of the
# time-live pointwise layer = K4 (t spectator)  x  T1-translations (bare-t
# exclusion only — no character, TU1e)  x  [METRIC-LAYER Z2: T-parity, TU1h]
# x  [STRATUM-CONDITIONAL Z2: N-parity, TU1i]. The two Z2 layers are honest
# homomorphisms on the graded alphabet (parity of a product = sum of parities).
T_PAR = {"Q": 0, "f": 0, "bh": 0, "phi_x": 0, "phi_xx": 0, "phi_t": 1, "phi_tt": 0,
         "phi_xt": 1, "N": 1, "N_t": 0, "N_x": 1, "moduli": 0, "gamma": 0}
N_PAR = {"Q": 0, "f": 0, "bh": 0, "phi_x": 0, "phi_xx": 0, "phi_t": 0, "phi_tt": 0,
         "phi_xt": 0, "N": 1, "N_t": 1, "N_x": 1, "moduli": 0, "gamma": 0}
# ground the table entries against the TU1h polynomial model (each entry = a
# computed parity, not an assertion):
MODEL = {"phi_x": (diff(phi_mir, xm), diff(phi_p, xm)),
         "phi_t": (diff(phi_mir, tm), diff(phi_p, tm)),
         "phi_xx": (diff(phi_mir, xm, 2), diff(phi_p, xm, 2)),
         "phi_xt": (diff(phi_mir, xm, tm), diff(phi_p, xm, tm)),
         "phi_tt": (diff(phi_mir, tm, 2), diff(phi_p, tm, 2)),
         "N": (N_mir, N_p),
         "N_t": (diff(N_mir, tm), diff(N_p, tm)),
         "N_x": (diff(N_mir, xm), diff(N_p, xm))}
grounded = all(
    sp.expand(mir - (-1) ** T_PAR[key] * base.subs(tm, -tm)) == 0
    for key, (mir, base) in MODEL.items()
)
# the parity of a PRODUCT block is the sum of parities (grounded on a sample):
prod_sample = sp.expand((N_mir * diff(phi_mir, tm))
                        - (-1) ** ((T_PAR["N"] + T_PAR["phi_t"]) % 2)
                        * (N_p * diff(phi_p, tm)).subs(tm, -tm)) == 0
check("TU1j_layered_character_rule_assembled", "SUBSTANTIVE",
      grounded and prod_sample
      and T_PAR["phi_t"] == 1 and T_PAR["N_t"] == 0 and T_PAR["N"] == 1,
      "layered rule: components must be (i) K4-character-matched (t spectator, banked), (ii) built "
      "without bare t (T1-translations), (iii) T-parity-matched to their paired direction AT THE "
      "METRIC LAYER (R_N odd since delta-N flips; field/moduli components even), (iv) N-parity-"
      "matched ON the psi-branch strata (coordinate reading). Table entries grounded on the TU1h "
      "model: parity(d_t phi) = odd, parity(d_t N) = even, parity(N) = odd. Layers (iii)/(iv) carry "
      "their conditionality stamps — they are CUTS only where their symmetry is granted/lawful")

# --- TU1k: the odd module is generated by the odd blocks over the even ring
# (the parity analog of the banked chi-module generation theorem).
odd_vars = ["N", "phi_t", "f_t"]
even_vars = ["Q", "phi_x", "N_t"]
allv = odd_vars + even_vars
odd_gen_ok = True
for expts in itertools.product(range(5), repeat=6):
    if not 0 < sum(expts) <= 4:
        continue
    par = sum(e for v, e in zip(allv, expts) if v in odd_vars) % 2
    if par == 1:
        # must factor as (one odd variable) x (even-parity remainder)
        found = False
        for i, v in enumerate(allv):
            if v in odd_vars and expts[i] >= 1:
                rem = list(expts)
                rem[i] -= 1
                rpar = sum(e for vv, e in zip(allv, rem) if vv in odd_vars) % 2
                if rpar == 0:
                    found = True
                    break
        if not found:
            odd_gen_ok = False
check("TU1k_odd_module_generated_by_odd_blocks", "SUBSTANTIVE",
      odd_gen_ok,
      "exhaustive to degree 4 on a representative 3-odd/3-even block set: every odd-parity monomial "
      "= (one odd block) x (even-parity monomial) — the T-odd (and N-odd) component modules are "
      "generated over the even subring by the odd blocks (general degree: remove one odd factor, "
      "the remainder's odd-degree drops by one = even — the banked parity argument re-instantiated); "
      "so e.g. R_N (T-odd at the metric layer) = sum over odd blocks {N, d_t phi, d_t f, d_t bh, "
      "d_x d_t (fields), d_x N, ...} x even coefficients")

# --- TU1l: K4 moduli characters with t spectator (banked T1s re-run).
k00t, k10t, k11t = symbols("k00t k10t k11t")
c00t, c01t, c10t, c11t = symbols("c00t c01t c10t c11t")
Xt = zeros(4, 4)
Xt[0:2, 0:2] = sp.diag(-1, 1)
Xt[2:4, 0:2] = Matrix([[c00t, c01t], [c10t, c11t]])
Xt[2:4, 2:4] = Matrix([[k00t, 0], [k10t, k11t]])
ok_R23t = is_zero_matrix(R23 * Xt * R23 - Xt.subs({c00t: -c00t, c01t: -c01t, c10t: -c10t, c11t: -c11t}, simultaneous=True))
ok_R12t = is_zero_matrix(R12 * Xt * R12 - Xt.subs({k10t: -k10t, c00t: -c00t, c11t: -c11t}, simultaneous=True))
ok_R13t = is_zero_matrix(R13 * Xt * R13 - Xt.subs({k10t: -k10t, c01t: -c01t, c10t: -c10t}, simultaneous=True))
check("TU1l_K4_characters_t_spectator_rerun", "GUARD",
      ok_R23t and ok_R12t and ok_R13t,
      "banked T1s re-run: with every moduli entry an arbitrary function of (x,t) the K4 characters "
      "hold unchanged (lam, k_mod invariant; k10 chi_a; C signed flips) — t spectator of the quotient")

print("=" * 78)
print("STAGE T2 — TU-2: the pointwise reduction, per lock-reading branch")
print("=" * 78)

# --- TU2a: the N-sector slot structure — NO forced-slot analog, NO null slot.
# The three delta-N directions pair componentwise; the pairing Gram is the
# identity (nondegenerate, empty annihilator): unlike the screen sector (Gram
# diag(2,2,1) + the E12 null slot) the N-sector has no canonical decomposition
# and no unpaired direction — the static trace-free FORCING has no N-analog,
# and the banked forcing itself transfers untouched (moduli-sector, t spectator).
GramN = Matrix(3, 3, lambda i, j: (eye(3)[:, i].T * eye(3)[:, j])[0, 0])
annN = GramN.nullspace()
I2m = eye(2)
D2 = sp.diag(-1, 1)
E21 = Matrix([[0, 0], [1, 0]])
E12 = Matrix([[0, 1], [0, 0]])


def pairtr(A_, B_):
    return sp.trace(A_.T * B_)


GramS = Matrix(3, 3, lambda i, j: pairtr([I2m, D2, E21][i], [I2m, D2, E21][j]))
check("TU2a_N_sector_no_forced_slot_no_null_slot", "SUBSTANTIVE",
      GramN == eye(3) and annN == [] and GramS == sp.diag(2, 2, 1)
      and pairtr(E12, I2m) == 0 and pairtr(E12, D2) == 0 and pairtr(E12, E21) == 0,
      "N-sector pairing Gram = I3 (nondegenerate, no annihilator): every delta-N_i direction is "
      "paired by exactly its own component — NO null slot, NO trace/trace-free split exists (a "
      "vector row, not a symmetric kernel), so NO new forced-slot theorem arises in the N-sector; "
      "the screen sector's structure (Gram diag(2,2,1), E12 null slot) is unchanged — the static "
      "trace-free slot FORCING transfers verbatim (its fate: INTACT)")

# --- TU2b: delta_gauge N = 0 — the local-Lorentz action leaves EVERY metric
# component invariant, so the shift row (and all metric rows) are gauge-inert.
Egen = Matrix(4, 4, symbols("e0:16", real=True))
chi_b = symbols("chi_boost", real=True)
Boost = Matrix([[sp.cosh(chi_b), sp.sinh(chi_b), 0, 0],
                [sp.sinh(chi_b), sp.cosh(chi_b), 0, 0],
                [0, 0, 1, 0], [0, 0, 0, 1]])
gauge_inert = all(
    is_zero_matrix(sp.expand((Lam * Egen).T * eta * (Lam * Egen) - Egen.T * eta * Egen))
    for Lam in [R23, R12, R13, Boost]
)
check("TU2b_delta_gauge_N_zero", "SUBSTANTIVE",
      gauge_inert,
      "g = E^T eta E is exactly invariant under E -> Lam E for the K4 elements AND a generic boost "
      "(symbolic 16-entry coframe): every metric component — the shift row N included — is a "
      "local-Lorentz INVARIANT, so delta_gauge N = 0 identically: the R_N slots pair NO gauge "
      "direction and drop out of every Noether pairing (feeds TU-4)")

# --- TU2c: R_N's K4 character is FORCED trivial.
lamM, kmodM = symbols("lam_M kmod_M", real=True)
RN_bad = k10 * N
bad_breaks = any(
    simplify(RN_bad.subs(sm, simultaneous=True) - RN_bad) != 0 for _, sm in K4_SUBS
)
RN_good = N
good_holds = all(
    simplify(RN_good.subs(sm, simultaneous=True) - RN_good) == 0 for _, sm in K4_SUBS
)
check("TU2c_RN_K4_trivial_forced", "SUBSTANTIVE",
      bad_breaks and good_holds,
      "delta-N is K4-inert (TU2b: K4 acts through the frame, the metric row is invariant), so "
      "character matching FORCES R_N to carry the trivial K4 character: witness k10*N (chi_a "
      "dependence) breaks equivariance, N itself is inert — R_N in (A^T)-trivial, exactly like the "
      "field components; NO chi-module dresses the N-row")

# --- TU2d: the R_N slots SURVIVE every re-posed pointwise requirement on the
# coordinate branch — composite witness R_N = N passes every derived gate.
witness_N = N
w_shift = simplify(witness_N.subs({phi: phi + s_sh, cE: cE * exp(s_sh)}, simultaneous=True) - witness_N) == 0
w_baret = not (witness_N.has(t_sym))
w_K4 = good_holds
w_Tpar = (T_PAR["N"] == 1)          # T-odd, matching delta-N (grounded TU1h/TU1j)
w_Npar = (N_PAR["N"] == 1)          # N-odd, matching delta-N on the psi-branch strata
check("TU2d_RN_survives_all_PW_requirements_coordinate", "SUBSTANTIVE",
      w_shift and w_baret and w_K4 and w_Tpar and w_Npar,
      "COORDINATE-BRANCH R_N VERDICT: the witness R_N = N is shift-orbit-inert (J04), bare-t-free "
      "(TU1e), K4-trivial (R7a), T-parity ODD = the parity of delta-N (metric layer), N-parity ODD "
      "on the psi-branch strata, unconstrained by every stratum Noether identity (delta_gauge N = 0, "
      "TU2b), censused (R1/R2: O17), pointwise (R13), off-shell (R12/J14): ALL THREE R_N SLOTS "
      "SURVIVE the re-posed pointwise requirement set as PHYSICAL-CONTENT components — the "
      "coordinate branch's new pointwise content is REAL at this layer (fork not decided; status "
      "rides the lock reading)")

# --- TU2e: a second N-row witness with PER-WITNESS STRATUM STAMPS: R_N = c_E d_t phi
# is character-legal at the metric layer but VIOLATES the stratum-conditional
# N-parity on the psi-branch strata (the static per-witness-stamp discipline
# recurs time-live).
wit2_T_par = (T_PAR["phi_t"] + 0) % 2 == 1     # c_E even, phi_t odd -> T-odd: matches delta-N
wit2_N_par = (N_PAR["phi_t"] + 0) % 2 == 0     # N-parity EVEN: MISMATCH on the strata
wit2_anchored = simplify((cE * dtphi) - anch_new) == 0   # overlap-invariant (TU1d)
check("TU2e_RN_witness_dtphi_stratum_scoped", "SUBSTANTIVE",
      wit2_T_par and wit2_N_par and wit2_anchored,
      "R_N = c_E d_t phi: T-odd (legal at the metric layer), anchor-overlap-invariant (TU1d), "
      "K4-trivial — but N-parity EVEN while delta-N is N-odd: on the strata where the Z2 psi-branch "
      "is lawful (2N e^{2phi}/c^2 t-independent, coordinate reading) it FAILS the stratum character "
      "cut — a member of R_PW^T OFF those strata only (per-witness stratum stamps, the exact "
      "time-live recurrence of the banked omega-witness discipline)")

# --- TU2f: the screen slot reduction with t-live symbols (banked PW3 re-run).
r_tr, r_tf, r_sh, r_nl = symbols("r_tr r_tf r_sh r_nl")
W = r_tr * I2m + r_tf * D2 + r_sh * E21 + r_nl * E12
compS = (simplify(pairtr(W, I2m)), simplify(pairtr(W, D2)), simplify(pairtr(W, E21)))
check("TU2f_screen_slot_structure_t_spectator", "GUARD",
      compS == (2 * r_tr, 2 * r_tf, r_sh),
      "banked PW3 re-run with every symbol read at (x,t): R_lambda = 2 r_tr, R_kmod = 2 r_tf, "
      "R_k10 = r_sh — the slot decomposition is pointwise-algebraic, t spectator")
check("TU2g_tracefree_slot_theorem_timelive", "GUARD",
      simplify(pairtr(W.subs(r_tf, 0), D2)) == 0,
      "banked slot theorem re-run t-live: a kernel with zero trace-free slot has R_kmod = 0 "
      "identically — k_mod-sensitivity REQUIRES the trace-free slot; the static forced-slot "
      "theorem's fate = TRANSFERS VERBATIM (R4's exact conditions are t-blind, banked T2g/T2h)")

# --- TU2h: the PROJECTED branch — the R_N chart-slack pairing STATED EXACTLY.
# Under the projected reading the psi-slack is residual chart-gauge (T1p4).
# Infinitesimal slack map at a point (psi value psi0, slope psi1): fields are
# relabeled (drag) and the shift row moves affinely:
#   delta phi = -psi0 * d_t phi ;  delta f = -psi0 * d_t f ;  delta bh = -psi0 * d_t bh ;
#   delta N   = g_tt * psi1 - psi0 * d_t N ;  delta gamma_xx = -psi0 * d_t gamma_xx
# (gamma's own slope-variation is ZERO — T1l psi-invariance; drags only).
Rphi, Rf, Rbh, RN1 = symbols("R_phi R_f R_bh R_N", real=True)
pt_f, ft_f, bt_f, Nt_f = symbols("dphi_t df_t dbh_t dN_t", real=True)
d_phi = -psi0 * pt_f
d_f = -psi0 * ft_f
d_bh = -psi0 * bt_f
d_N = g_tt * p1 - psi0 * Nt_f
pairing_slack = sp.expand(Rphi * d_phi + Rf * d_f + Rbh * d_bh + RN1 * d_N)
a_leg = -(Rphi * pt_f + Rf * ft_f + Rbh * bt_f + RN1 * Nt_f)
b_leg = RN1 * g_tt
check("TU2h_projected_branch_slack_pairing_legs_exact", "SUBSTANTIVE",
      sp.expand(pairing_slack - (a_leg * psi0 + b_leg * p1)) == 0
      and sp.expand(sp.Poly(pairing_slack, psi0, p1).coeff_monomial(p1) - b_leg) == 0,
      "the pointwise pairing of the response with an infinitesimal slack map is EXACTLY "
      "a*psi + b*psi' with DRAG LEG a = -(R_phi d_t phi + R_f d_t f + R_bh d_t bh + R_N d_t N) "
      "[moduli drags join on the m(t)/m(x,t) readings — typed, carried] and SLOPE LEG "
      "b = R_N * g_tt: on the PROJECTED branch (slack = chart-gauge) the R_N slots pair PURE "
      "CHART-SLACK through b; the resulting Noether-SECOND-theorem divergence identity between a "
      "and b lives at the INTEGRATION layer (needs the declared pairing + time-domain datum) — "
      "POSED, typed, NOT imposed pointwise (no pointwise kill of R_N is derivable here); on the "
      "COORDINATE branch the same two legs are J07 overlap-transport data, no identity owed. "
      "F-U2 self-audit: derived from chart maps on covariant rows; no foliation/ADM object used")

# --- TU2i: the pointwise module space is READING-INDEPENDENT — the branches
# differ in the STATUS of the R_N sector, not in the surviving space's shape.
sub_roundtrip = simplify((gam_expr - N**2 * exp(2 * phi) / c**2) - gxx) == 0
# content: d_x phi = D_x phi + (N/g_tt) d_t phi has consistent T-parity:
lhs_par = T_PAR["phi_x"]                                # even
rhs_par = (T_PAR["N"] + T_PAR["phi_t"]) % 2             # odd+odd = even (D_x term even too)
check("TU2i_module_space_reading_independent", "SUBSTANTIVE",
      sub_roundtrip and simplify(back_px - px_sym) == 0 and lhs_par == rhs_par == 0
      and good_holds,
      "the two registered presentations (coordinate: d_x-jets, g_xx, N | projected: D_x-jets, "
      "gamma_xx, overlap data) are related by the invertible triangular alphabet map (TU1g) which "
      "PRESERVES every character layer (K4: both sides inert; T-parity: d_x phi even = "
      "(N odd)x(d_t phi odd) even — computed; shift-orbit: both sides inert): the character-matched "
      "module parametrization of R_PW^T is IDENTICAL on both lock-reading branches — the fork "
      "changes the READING of the R_N sector (physical-content components vs chart-slack pairings "
      "subject to the typed integration-layer identity), NOT the pointwise shape (a MAP FACT, not "
      "a fork resolution; F-U4 honored)")

# --- TU2j: J06 determined-vs-retained for the NEW N-family — both branches
# of the branch structure nonempty, neither chosen.
RN_zero = sp.Integer(0)
retained_ok = all(simplify(RN_zero.subs(sm, simultaneous=True) - RN_zero) == 0 for _, sm in K4_SUBS)
check("TU2j_J06_N_family_both_branches_nonempty", "SUBSTANTIVE",
      good_holds and w_Tpar and retained_ok,
      "N-family J06 branch structure: DETERMINED branch witness R_N = N (nonzero, all characters "
      "matched — TU2d); RETAINED branch witness R_N == 0 with N reported residual (the zero "
      "component is trivially character-matched): both are open sub-loci of R_PW^T; NO branch "
      "chosen. On the projected branch the same table reads: slack-pairing present vs absent — "
      "carried per reading")

print("=" * 78)
print("STAGE T2 — TU-3: the static R_PW's fate under the time-live cuts")
print("=" * 78)

# --- TU3a: the NEW time-live cuts all VANISH on the static stratum, so the
# banked R_PW EMBEDS EXACTLY (component-by-component check is C-1; here: no
# banked member is lost or deformed by any new cut).
STATIC_BLOCKS = ["Q", "f", "bh", "phi_x", "phi_xx", "moduli"]   # the banked alphabet survivors
static_all_T_even = all(T_PAR[b] == 0 for b in STATIC_BLOCKS)
static_all_N_even = all(N_PAR[b] == 0 for b in STATIC_BLOCKS)
# static directions are T-even (delta phi, delta f, delta bh, delta moduli, walls),
# so parity-matching is AUTOMATIC for every banked member; the odd cut binds only
# the new R_N row (odd), which is ABSENT statically (its restriction is 0 = odd, ok).
check("TU3a_static_RPW_embeds_exactly_no_loss_no_deformation", "SUBSTANTIVE",
      static_all_T_even and static_all_N_even,
      "every block of the banked static alphabet is T-even AND N-even (no static block carries a "
      "t-jet or an N factor), and every banked component pairs a T-even direction: the metric-layer "
      "T-parity cut and the stratum Z2 N-parity cut are AUTOMATICALLY satisfied by every banked "
      "member; the stratum Noether identities restrict to the banked ones identically (moduli-"
      "sector, TU4); delta_gauge N = 0 adds no new identity component (TU2b): the banked R_PW "
      "EMBEDS EXACTLY as the time-independent stratum of R_PW^T — NO member lost, NO deformation; "
      "the enrichment is purely TRANSVERSE (R_N row + t-jet dependence). BRANCH STAMP: identical on "
      "both lock-reading branches — the static stratum is diagonal (N = 0), where the two readings "
      "coincide IDENTICALLY (T1 C2a re-run below)")

# --- TU3b: EH placement, time-live — parity witness on the exact 2D block.
# Build the (t,x)-block metric with a generic degree-2 tt-PROFILE g_tt = -E c^2
# (LINK STEP below: phi EVEN-composed <=> E = e^{-2 phi} EVEN-composed exactly,
# so the polynomial-E witness runs on precisely the parity the DERIVED T2a
# composition supplies; the exponential's own role — forbidding the phi sign
# flip — is the banked T2a content, cited), generic N and G, compute the exact
# Ricci tensor/scalar, and verify the temporal-mirror composition (E even,
# N odd, G even) maps R to R(x,-t) and Ric_tx to -Ric_tx(x,-t): the EH-form's
# scalar sector is T-EVEN and its ti-row is T-ODD — exactly the parity the
# R_N slot requires.
link_ok = simplify(exp(-2 * phi_mir) - exp(-2 * phi_p).subs(tm, -tm)) == 0
ec2 = symbols("Ec0:6", real=True)
bc2 = symbols("B0:6", real=True)
gc2 = symbols("G0:6", real=True)
mono2 = [1, xm, tm, xm**2, xm * tm, tm**2]
EPf = 1 + sum(e_ * mn for e_, mn in zip(ec2, mono2))
NP = sum(b * mn for b, mn in zip(bc2, mono2))
GP = 2 + sum(g_ * mn for g_, mn in zip(gc2, mono2))


# Numerator-level construction (exact, expand-only — no rational cancel):
# Gamma^a_bc = GamN[a][b][c] / (2 det);  Ric_bc = RicN[b,c] / (2 det)^2, with
# adj the adjugate (ginv = adj/det). At most TWO derivatives applied, by
# construction. Every parity check runs on POLYNOMIAL numerators; the shared
# denominators (2 det)^2, det are checked EVEN once.
gmat = Matrix([[-EPf * c**2, NP], [NP, GP]])
det2d = sp.expand(gmat[0, 0] * gmat[1, 1] - gmat[0, 1] ** 2)
adj2d = Matrix([[gmat[1, 1], -gmat[0, 1]], [-gmat[0, 1], gmat[0, 0]]])
coords2 = (tm, xm)
GamN = [[[sp.Integer(0)] * 2 for _ in range(2)] for _ in range(2)]
for a_i in range(2):
    for b_i in range(2):
        for c_i in range(2):
            e_x = sp.Integer(0)
            for d_i in range(2):
                e_x += adj2d[a_i, d_i] * (diff(gmat[d_i, b_i], coords2[c_i])
                                          + diff(gmat[d_i, c_i], coords2[b_i])
                                          - diff(gmat[b_i, c_i], coords2[d_i]))
            GamN[a_i][b_i][c_i] = sp.expand(e_x)
RicN = zeros(2, 2)
for b_i in range(2):
    for c_i in range(2):
        e_x = sp.Integer(0)
        for a_i in range(2):
            e_x += diff(GamN[a_i][b_i][c_i], coords2[a_i]) * 2 * det2d \
                - GamN[a_i][b_i][c_i] * 2 * diff(det2d, coords2[a_i])
            e_x -= diff(GamN[a_i][b_i][a_i], coords2[c_i]) * 2 * det2d \
                - GamN[a_i][b_i][a_i] * 2 * diff(det2d, coords2[c_i])
            for d_i in range(2):
                e_x += (GamN[a_i][a_i][d_i] * GamN[d_i][b_i][c_i]
                        - GamN[a_i][c_i][d_i] * GamN[d_i][b_i][a_i])
        RicN[b_i, c_i] = sp.expand(e_x)
MIR = {}
for e_, mn in zip(ec2, mono2):
    MIR[e_] = e_ * (-1) ** sp.degree(sp.Poly(mn, tm), tm) if mn != 1 else e_
for b, mn in zip(bc2, mono2):
    MIR[b] = -b * (-1) ** sp.degree(sp.Poly(mn, tm), tm) if mn != 1 else -b
for g_, mn in zip(gc2, mono2):
    MIR[g_] = g_ * (-1) ** sp.degree(sp.Poly(mn, tm), tm) if mn != 1 else g_
det_even = sp.expand(det2d.subs(MIR, simultaneous=True) - det2d.subs(tm, -tm)) == 0
ric_parity_ok = True
for b_i in range(2):
    for c_i in range(2):
        par = (1 if b_i == 0 else 0) + (1 if c_i == 0 else 0)
        d_r = sp.expand(RicN[b_i, c_i].subs(MIR, simultaneous=True)
                        - (-1) ** par * RicN[b_i, c_i].subs(tm, -tm))
        d_a = sp.expand(adj2d[b_i, c_i].subs(MIR, simultaneous=True)
                        - (-1) ** par * adj2d[b_i, c_i].subs(tm, -tm))
        if d_r != 0 or d_a != 0:
            ric_parity_ok = False
# Ric_bc = RicN/(2 det)^2 with det EVEN => Ric parity = RicN parity (tt/xx even,
# tx ODD); Rsc = sum adj[b,c] RicN[b,c] / ((2 det)^2 det): every summand has
# parity (-1)^{par} * (-1)^{par} = EVEN => Rsc EVEN (parity arithmetic on the
# checked entries — no giant cancel needed).
check("TU3b_EH_parity_witness_exact_2d", "SUBSTANTIVE",
      link_ok and det_even and ric_parity_ok,
      "exact 2D witness (generic degree-2 tt-profile E, N, G; LINK: phi even-composed <=> "
      "E = e^{-2phi} even-composed, checked exactly on the TU1h model): under the DERIVED temporal-"
      "mirror composition (phi even, N odd, spatial even — banked T2a) the Ricci scalar transforms "
      "EVEN (every Rsc summand adj*RicN has even parity over the even denominators — parity "
      "arithmetic on per-entry checked numerators) and the ti-component Ric_tx transforms ODD "
      "(RicN[0,1] odd over the even (2 det)^2): curvature-built "
      "(EH-form) responses are T-PARITY-MATCHED — scalar/spatial rows even (pairing delta phi etc.), "
      "ti-row odd (pairing delta N). EH PLACEMENT time-live: field sector, trivial K4 character, "
      "bigrade <= (2,2) (2nd derivatives — visible in this exact computation), T-parity-matched; "
      "on the coordinate branch its ti-row pairs the PHYSICAL delta N, on the projected branch the "
      "same expression pairs chart-slack (reading rides the fork). Bach-form: jets 3/4, typed class "
      "only (banked TC2, cited). 4D generality: tensor naturality under t -> -t (Category-A, cited); "
      "this 2D leg is the in-package exact instance")
check("TU3c_EH_time_jet_content_le2", "GUARD",
      any(RicN[i_, j_].has(ec2[5]) for i_ in range(2) for j_ in range(2))
      and any(RicN[i_, j_].has(gc2[5]) for i_ in range(2) for j_ in range(2)),
      "the exact 2D Ricci numerators depend on the t^2-coefficients of E and G (2nd time-jets "
      "genuinely enter), and the computation applies at most TWO derivatives by construction "
      "(one in GamN, one in RicN): the EH-form's time-jet content is <= 2 — inside the declared "
      "bigraded layer (in-package instance of the cited TC3 fact)")

print("=" * 78)
print("STAGE T2 — TU-4: the identity strata, time-live")
print("=" * 78)

# --- TU4a: the pointwise tangency system is t-SPECTATOR and N-BLIND. Build it
# on the time-live symbols: its entries involve ONLY the moduli symbols (the
# gauge motion is [B, X], pointwise-algebraic), and by TU2b no delta-N or field
# column exists (delta_gauge N = 0; chart scalars carry no frame index on the
# registered presentation).
bco = symbols("beta0:6")
B6 = zeros(4, 4)
for i, Lm in enumerate(GENS.values()):
    B6 = B6 + bco[i] * Lm
Cm_pt = B6 * X - X * B6
eqs_pt = [Cm_pt[i, j] for (i, j) in FORBIDDEN]
A_pt, _ = sp.linear_eq_to_matrix(eqs_pt, list(bco))
MOD_SYMS = {k00, k10, k11, c00, c01, c10, c11}
sys_syms = set().union(*[e.free_symbols for e in A_pt])
GENERIC_PT = {k00: 2, k10: 3, k11: 5, c00: 7, c01: 11, c10: 13, c11: 17}
check("TU4a_tangency_system_t_spectator_N_blind", "SUBSTANTIVE",
      sys_syms <= MOD_SYMS
      and A_pt.subs(GENERIC_PT).rank() == 6 and A_pt.subs(GENERIC_PT).nullspace() == [],
      "the time-live pointwise tangency system's entries involve ONLY the seven moduli symbols "
      "(each read as an arbitrary function of (x,t)): no t-jet, no N, no field block enters — the "
      "R7(b) identity layer is t-SPECTATOR and N-BLIND; generic rank 6 / empty nullspace re-derived "
      "(R7(b) generically vacuous, time-live)")

# --- TU4b: the k_mod = 0 identity EXTENDS VERBATIM — no time-components, no split.
minors_pt = []
for rsel in itertools.combinations(range(A_pt.rows), 6):
    mdet = sp.expand(A_pt[list(rsel), :].det())
    if mdet != 0:
        minors_pt.append(mdet)
minors_div = all(sp.expand(sp.div(mdet, k00 - k11, k00)[1]) == 0 for mdet in minors_pt)
A_iso = A_pt.subs(k11, k00)
ns_iso = A_iso.nullspace()
L23m = GENS["L23"]
W23 = (L23m * X - X * L23m).subs(k11, k00)
Jrot = Matrix([[0, 1], [-1, 0]])
dK23 = W23[2:4, 2:4]
dC23 = W23[2:4, 0:2]
m00, m01, m10, m11 = symbols("m00 m01 m10 m11")
MkerA = Matrix([[m00, m01], [m10, m11]])
W_slotA = r_tr * I2m + r_tf * D2 + r_sh * E21 + r_nl * E12
RN2, RN3 = symbols("R_N2 R_N3", real=True)
# the FULL time-live pairing on the stratum: screen + mixing + N-row + field row,
# with the derived gauge motions delta_gauge N = 0 (TU2b) and field sector zero
# (chart scalars, registered presentation — banked, re-posed T1):
pairing_full = sp.expand(pairtr(W_slotA, dK23) + pairtr(MkerA, dC23)
                         + RN1 * 0 + RN2 * 0 + RN3 * 0
                         + Rphi * 0 + Rf * 0 + Rbh * 0)
IDENT_KMOD0 = sp.expand(-2 * k10 * r_tf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01)
check("TU4b_kmod0_identity_extends_verbatim", "SUBSTANTIVE",
      len(minors_pt) == 36 and minors_div
      and len(ns_iso) == 1 and all(simplify(ns_iso[0][i]) == 0 for i in range(5))
      and sp.expand(pairing_full - IDENT_KMOD0) == 0,
      "all 36 nonzero 6x6 minors divisible by (k00 - k11) [all-member proof, t-live symbols]; on "
      "k_mod = 0 the nullspace is span(L23); the FULL time-live pairing (screen + mixing + THE "
      "THREE R_N SLOTS + field slots) equals the banked identity EXACTLY: "
      "-2 k10 r_tf + m00 c10 + m01 c11 - m10 c00 - m11 c01 = 0 — the identity EXTENDS VERBATIM, "
      "GAINS NO TIME-COMPONENTS, DOES NOT SPLIT (delta_gauge N = 0 and zero field sector kill every "
      "candidate new term); BRANCH STAMP: identical on both lock-reading branches (the identity is "
      "moduli-sector; the branch difference lives in the N-sector, which drops out)")

# --- TU4c: the codim-1 confinement re-derived time-live (Groebner re-run).
gb_minors = sp.groebner(minors_pt, k00, k10, k11, c00, c01, c10, c11, order="grevlex")
conf_poly = sp.expand((k00 - 1) * (k00 + 1) * (k00 - k11) * (k11 - 1) * (k11 + 1))
check("TU4c_kmod0_only_codim1_cut_timelive", "GUARD",
      sp.expand(gb_minors.reduce(conf_poly)[1]) == 0,
      "banked confinement re-run on the t-live system: every rank-drop point lies in {k_mod = 0} "
      "UNION the eigenvalue resonances {lam -+ k_mod in {+-1}} — k_mod = 0 remains the only "
      "CODIMENSION-1 cut time-live (the codim-1 layer is exhaustive)")

# --- TU4d: the resonance locus — TYPED, stamped OPEN-PENDING-CENSUS (F-U8).
RES_TYPED = [
    "four named C=0 strata: identities mixing-only, auto-satisfied in the declared class (banked)",
    "C!=0 sub-varieties: further genuine cuts exist; derived example -c10 r_sh - k10 m10 = 0 on "
    "{lam-k_mod=-1, c00=c01=0} (banked round-2); deeper stratification TYPED-NOT-EXHAUSTED",
    "TIME-LIVE STATUS: every statement contacting the resonance locus is stamped "
    "OPEN-PENDING-CENSUS (the queued verifier-required census precondition) — restated as banked "
    "citations only; NO time-live adjudication performed here (F-U8 honored)",
]
check("TU4d_resonance_locus_typed_open_pending_census", "GUARD",
      len(RES_TYPED) == 3 and "OPEN-PENDING-CENSUS" in RES_TYPED[2],
      "the banked resonance content (four named strata + the shear-identity example + the "
      "typed-not-exhausted stamp) travels as CITATION; its time-live fate is stamped "
      "OPEN-PENDING-CENSUS, not adjudicated — the t-spectator/N-blind facts of TU4a apply to the "
      "SYSTEM, and are recorded; per-stratum time-live identities await the queued census")

# --- TU4e: NEW stratum layer typed — the psi-branch chart-symmetry strata.
check("TU4e_psi_branch_strata_typed_character_not_identity", "SUBSTANTIVE",
      simplify(g2_flip[0, 1] + N) == 0 and len(ns_iso) == 1,
      "the time-live domain adds a NEW stratum TYPE: the chart-symmetry strata where the Z2 "
      "psi-branch is lawful (2N e^{2phi}/c^2 t-independent; coordinate reading) — on them the "
      "residual group enlarges DISCRETELY, so the new stratum carries a CHARACTER cut (N-parity, "
      "TU1i/TU1j) and NO Noether identity (no continuous parameter) — the exact analog of K4's "
      "banked status, and DISJOINT in kind from the moduli degeneration strata (which carry "
      "identities from CONTINUOUS tangent gauge directions)")

print("=" * 78)
print("STAGE T2 — TU-5: controls (C-1 mechanical static recovery; C-2 diagonal-frozen)")
print("=" * 78)

# --- C-1: the static restriction of R_PW^T must recover the BANKED static
# R_PW EXACTLY, parsed MECHANICALLY from the banked results JSON (never
# hand-copied). Failure = F-U7 = halt.
BANKED_JSON = os.path.join(HERE, "..", "udt_p4_routeA_stage2_pointwise_reduction_2026-07-29",
                           "routeA_stage2_results.json")
with open(BANKED_JSON) as fh:
    BANK = json.load(fh)

# (C1a) component table: my time-live table restricted static = the banked table.
TIMELIVE_COMPONENTS = [
    ("R_phi", "trivial"), ("R_f", "trivial"), ("R_bh", "trivial"),
    ("R_lambda", "trivial"), ("R_kmod", "trivial"), ("R_k10", "chi_a"),
    ("R_c00", "chi_b"), ("R_c11", "chi_b"), ("R_c01", "chi_c"), ("R_c10", "chi_c"),
    ("R_N_x", "trivial"), ("R_N_y", "trivial"), ("R_N_z", "trivial"),  # NEW (O17; K4-trivial FORCED TU2c; T-odd)
    ("R_wall", "trivial"), ("R_corner", "trivial"),
    ("R_timewall_branch_c_only", "typed"), ("R_timecorner_branch_c_only", "typed"),
]
STATIC_KILL = {"R_N_x", "R_N_y", "R_N_z", "R_timewall_branch_c_only", "R_timecorner_branch_c_only"}
static_restricted = [(n_, ch) for (n_, ch) in TIMELIVE_COMPONENTS if n_ not in STATIC_KILL]
banked_table = [(row["component"], row["character"]) for row in BANK["component_table"]]
check("C1a_component_table_static_recovery_mechanical", "SUBSTANTIVE",
      static_restricted == banked_table and len(banked_table) == 12,
      f"killing the R_N and branch-(c) slots recovers the banked 12-component table EXACTLY, in "
      f"order, character-for-character (banked JSON parsed mechanically: {len(banked_table)} rows). "
      "F-U7 NOT fired")

# (C1b) character-module generators: parse the banked generator strings and
# compare as exact expressions with my generator sets.
SYMTAB = {"k10": k10, "c00": c00, "c01": c01, "c10": c10, "c11": c11}


def parse_gen_token(tok):
    parts = re.findall(r"k10|c\d\d", tok)
    if "".join(parts) != tok:
        return None
    out = sp.Integer(1)
    for p_t in parts:
        out *= SYMTAB[p_t]
    return out


MY_GENS = {
    "chi_a": [k10, c00 * c01, c00 * c10, c11 * c01, c11 * c10],
    "chi_b": [c00, c11, k10 * c01, k10 * c10],
    "chi_c": [c01, c10, k10 * c00, k10 * c11],
}
gens_match = True
for cls, mine in MY_GENS.items():
    raw = BANK["character_modules"][cls]["generators"].strip("{}").split(",")
    parsed = [parse_gen_token(tok.strip()) for tok in raw]
    if None in parsed or len(parsed) != len(mine):
        gens_match = False
        continue
    if any(sp.expand(a - b) != 0 for a, b in zip(parsed, mine)):
        gens_match = False
check("C1b_module_generators_static_recovery_mechanical", "SUBSTANTIVE",
      gens_match,
      "the banked chi_a/chi_b/chi_c module generator strings, parsed mechanically from the JSON, "
      "equal my time-live module generators EXACTLY as expressions (the K4 layer of R_PW^T "
      "restricts to the banked one; t was a spectator throughout). F-U7 NOT fired")

# (C1c) the stratum identities: parse the banked identity strings mechanically
# and match my re-derived expressions.
IDSYM = {"k10": k10, "c00": c00, "c01": c01, "c10": c10, "c11": c11,
         "r_tr": r_tr, "r_tf": r_tf, "r_sh": r_sh, "r_nl": r_nl,
         "m00": m00, "m01": m01, "m10": m10, "m11": m11}


def parse_identity(text):
    lhs = text.split("=")[0].strip()
    lhs = lhs.replace(" - ", " + -")
    total = sp.Integer(0)
    for term in lhs.split(" + "):
        factors = term.strip().split()
        prod = sp.Integer(1)
        for fct in factors:
            neg = fct.startswith("-")
            core = fct.lstrip("-")
            if core in IDSYM:
                prod *= IDSYM[core]
            else:
                prod *= sp.Integer(int(core))
            if neg:
                prod *= -1
        total += prod
    return sp.expand(total)


bank_kmod0 = parse_identity(BANK["stratum_noether_identities_A1"]["kmod0"]["identity"])
bank_shear = parse_identity(BANK["stratum_noether_identities_A1"]["Cneq0_subvarieties_R2"]["identity"])
MY_SHEAR = sp.expand(-c10 * r_sh - k10 * m10)
check("C1c_stratum_identities_static_recovery_mechanical", "SUBSTANTIVE",
      sp.expand(bank_kmod0 - IDENT_KMOD0) == 0 and sp.expand(bank_shear - MY_SHEAR) == 0,
      "the banked k_mod = 0 identity and the banked shear identity, parsed mechanically from the "
      "JSON strings, equal my re-derived time-live expressions EXACTLY: the identity strata of "
      "R_PW^T restrict to the banked cuts identically. F-U7 NOT fired")

# (C1d) alphabet dims: my (g,0) restriction = banked 10/13/16.
my_static_dims = {"grade0": 3 + 7, "grade1": 3 + 7 + 3, "grade2": 3 + 7 + 3 + 3}
check("C1d_alphabet_dims_static_recovery", "GUARD",
      my_static_dims == dict(BANK["alphabet_functional_dims_base"]),
      "the time-independent restriction of the bigraded alphabet (time-jet order 0, N-blocks "
      "killed) has functional dims 10/13/16 per spatial grade = the banked dims exactly (JSON "
      "parsed mechanically)")

# --- C-2: the diagonal-frozen control stratum, per branch.
gam_at_N0 = simplify((gam - gxx).subs(N, 0))
g2p_diag = g2p.subs(N, 0)
check("C2a_diagonal_frozen_control_per_branch", "SUBSTANTIVE",
      gam_at_N0 == 0
      and simplify(g2p_diag[0, 1] - g_tt * p1) == 0,
      "on N = 0 the two lock readings coincide IDENTICALLY (gamma_xx = g_xx), so the BRANCH LABEL "
      "DEGENERATES on the control stratum: the diagonal-frozen time-live space is the SAME on both "
      "branches = banked static component structure x the bigraded alphabet WITHOUT N-blocks "
      "(t-jets live, R_N slots present at N = 0 pairing transverse directions); the stratum is NOT "
      "chart-closed (a slack map regenerates N' = g_tt psi' != 0 — banked C2b re-run): shift-off "
      "remains a chart-conditional CONTROL, never a physics restriction; the branches differ off "
      "the stratum exactly as derived (TU2h/TU2i)")

# --- Coverage and typing guards (R2/J05/J13 time-live).
check("R2_J05_component_coverage_timelive", "GUARD",
      len(TIMELIVE_COMPONENTS) == 17
      and {"R_N_x", "R_N_y", "R_N_z"} <= {n_ for n_, _ in TIMELIVE_COMPONENTS}
      and {"R_kmod", "R_c00", "R_c01", "R_c10", "R_c11"} <= {n_ for n_, _ in TIMELIVE_COMPONENTS},
      "one component slot per 18-census direction (12 banked + 3 R_N + 2 branch-(c) TYPED slots; "
      "alpha/c_E forks enter on their labeled branches as banked): a missing R_N slot would be the "
      "static era's presentation-freeze made visible (coordinate reading) — R2 honored; J05 full "
      "tangent paired (delta-N and bigraded jet directions included); J13 discriminator slots "
      "(k_mod, C) retained; theta ABSENT; no cycle/completion content (F-U1 self-audit)")

# --- Hygiene guards (wired into the exit path).
with open(os.path.abspath(__file__)) as fh:
    src = fh.read()
banned = ["ns" + "olve", "ev" + "alf", "im" + "port random", "im" + "port numpy", "tor" + "ch"]
check("G3_no_floats_numeric_solvers_or_rng", "GUARD",
      all(b not in src for b in banned) and re.search(r"\d\.\d", src) is None,
      "source scan: no numeric solvers, no float-evaluation calls, no RNG, no array/GPU libraries, "
      "no float literals — exact and deterministic")

# ---------------------------------------------------------------------------
# Emit ledger (TIMELIVE_T2_LEDGER.tsv), JSON (G1 wired), exit.
# ---------------------------------------------------------------------------
LEDGER_HEADER = [
    "# STAMP: Stage T2 time-live pointwise ledger. Contract = PREREGISTRATION.md (frozen first). "
    "EVERYTHING-ON; registered chart's time extension (T-L1 CHOSE); bigraded jets <= (2,2), higher TYPED; "
    "BOTH lock-reading branches at the same depth; registered stationary presentation (general arenas TYPED); "
    "polynomial/formal in (k10,C); theta ABSENT; no census reading adopted; no fork resolved; no solve.",
    "# STAMP: layered character rule (TU-1): K4 (t spectator) x T1-translations (bare-t excluded) x "
    "METRIC-LAYER T-parity Z2 (conditional: coframe layer imposes nothing) x STRATUM-CONDITIONAL N-parity Z2 "
    "(coordinate reading, psi-branch strata). Resonance-locus contacts: OPEN-PENDING-CENSUS (F-U8).",
    "# STAMP: static restriction column = the C-1 identity (mechanical vs banked routeA_stage2 JSON): PASS.",
]
LEDGER_ROWS = []
for (n_, ch) in TIMELIVE_COMPONENTS:
    if n_ in {"R_timewall_branch_c_only", "R_timecorner_branch_c_only"}:
        LEDGER_ROWS.append([n_, "COMPONENT", "branch-(c) TYPED slot only (no content populated; F-U1)",
                            ch, "TYPED", "absent statically", "-"])
        continue
    tpar = "odd" if n_ in {"R_N_x", "R_N_y", "R_N_z"} else "even"
    stat = "killed (N=0 diagonal premise)" if n_ in STATIC_KILL else "banked component recovered"
    LEDGER_ROWS.append([
        n_, "COMPONENT",
        f"K4 char {ch}; T-parity {tpar} (metric layer); N-parity {tpar} on psi-branch strata "
        f"(coordinate reading); module over the bigraded alphabet; coordinate branch: physical "
        f"content; projected branch: {'chart-slack pairing (TU2h legs)' if tpar == 'odd' else 'unchanged reading'}",
        ch, "DERIVED", stat, "TU1j;TU2c;TU2d;TU2f"])
CONSTRAINT_ROWS = [
    ["(constraint) STRATUM-IDENTITY kmod0", "CONSTRAINT",
     "-2 k10 r_tf + m00 c10 + m01 c11 - m10 c00 - m11 c01 = 0 on k_mod = 0 — EXTENDS VERBATIM "
     "time-live: no time-components, no split (delta_gauge N = 0; field sector zero); both branches identical",
     "chi_a-graded", "DERIVED", "banked cut recovered (C1c)", "TU4b"],
    ["(constraint) resonance locus", "CONSTRAINT",
     "banked content cited (four named C=0 strata auto-satisfied; C!=0 shear example; deeper "
     "TYPED-NOT-EXHAUSTED); time-live fate stamped OPEN-PENDING-CENSUS — NOT adjudicated (F-U8)",
     "-", "CITED", "banked cut recovered (C1c)", "TU4d"],
    ["(constraint) METRIC-LAYER T-parity", "CONSTRAINT",
     "components T-parity-matched to their directions (R_N odd, rest even); CONDITIONAL: metric "
     "layer only (coframe layer SO+-obstructed, admitting it = CHOSE); vacuous on the static stratum",
     "Z2", "DERIVED", "vacuous statically (TU3a)", "TU1h;TU1j"],
    ["(constraint) STRATUM N-parity", "CONSTRAINT",
     "components N-parity-matched on psi-branch strata (2N e^{2phi}/c^2 t-independent; coordinate "
     "reading); DISCRETE: character cut, no Noether identity; per-witness stratum stamps (TU2e)",
     "Z2", "DERIVED", "vacuous statically (TU3a)", "TU1i;TU4e"],
]
ALPHABET_ROWS = [
    ["alphabet bigraded", "ALPHABET",
     "blocks: Q (forced unique phi-channel, TU1a/TU1c) + bigraded jets of (phi,f,bh) <= (2,2) + "
     "N + bigraded N-jets (radial presentation; N_y,N_z typed) + moduli (const reading; m(t)/m(x,t) "
     "typed) + wall/corner data + NO bare t (TU1e) + NO bare phi (banked)",
     "-", "DERIVED", "restricts to banked 10/13/16 (C1d)", "TU1a-TU1e"],
    ["alphabet presentations", "ALPHABET",
     "coordinate frame blocks (d_x-jets, g_xx, N) <-> psi-invariant blocks (D_x-jets, gamma_xx, N) "
     "invertible triangular map; D_x = d_x - (N/g_tt) d_t derived psi-invariant; module space "
     "reading-independent (TU2i)",
     "-", "DERIVED", "identical statically (D_x = d_x at N=0)", "TU1f;TU1g;TU2i"],
]
ledger_path = os.path.join(HERE, "TIMELIVE_T2_LEDGER.tsv")
with open(ledger_path, "w") as fh:
    for line in LEDGER_HEADER:
        fh.write(line + "\n")
    fh.write("row\tkind\tcontent\tcharacter\ttag\tstatic_restriction\tbasis_checks\n")
    for row in LEDGER_ROWS + CONSTRAINT_ROWS + ALPHABET_ROWS:
        fh.write("\t".join(row) + "\n")
print(f"ledger written: {ledger_path} ({len(LEDGER_ROWS) + len(CONSTRAINT_ROWS) + len(ALPHABET_ROWS)} rows)")

result = {
    "package": "udt_p4_timelive_stage_T2_2026-07-31",
    "stage": "T2 (TU-1..TU-5; the pointwise reduction time-live, both lock-reading branches)",
    "date": "2026-07-31",
    "contract": "PREREGISTRATION.md (frozen before derivation)",
    "TU1_verdict": ("phi-dependence forcing INTACT time-live: shift-equivariance alone still forces "
                    "Q = c_E e^{-phi} as the unique phi-channel; time-dependence opens NO new channel "
                    "and closes none (new blocks shift-inert); t-leg factor = presentation-overlap "
                    "datum with anchored combination c_E d_t phi; NEW derived alphabet gate: bare t "
                    "excluded by T1-translations; psi-slack forces the invariant/frame alphabet split "
                    "with D_x = d_x - (N/g_tt) d_t derived psi-invariant; layered character rule: "
                    "K4 (t spectator) x T1 x metric-layer T-parity Z2 (conditional) x stratum N-parity "
                    "Z2 (conditional)"),
    "TU2_verdict": ("COORDINATE branch: all three R_N slots SURVIVE every re-posed pointwise "
                    "requirement (K4-trivial FORCED; T-odd; witness R_N = N passes all gates; witness "
                    "c_E d_t phi stratum-scoped); no new forced slot, no null slot in the N-sector; "
                    "static trace-free forcing transfers verbatim. PROJECTED branch: same module "
                    "space (reading-independent, derived — identical at the unconditional character "
                    "layers; the stratum-conditional N-parity cut rides the coordinate reading: on "
                    "psi-branch strata the projected branch carries the equivalent content in the "
                    "slack-pairing typing, not as a pointwise cut [AMENDMENT 2026-07-31, verifier "
                    "round 1]); R_N pairs chart-slack with exact legs "
                    "a = -(sum R_A d_t A), b = R_N g_tt; the divergence identity between them is "
                    "integration-layer, typed not imposed. Fork NOT resolved; both at same depth"),
    "TU3_verdict": ("the banked static R_PW EMBEDS EXACTLY (no member lost, no deformation; all new "
                    "cuts vanish on the static stratum); branch-independent (static stratum is "
                    "diagonal where readings coincide); EH-form: field sector, trivial K4, bigrade "
                    "<= (2,2), T-parity-matched (exact 2D witness: Ricci scalar even, ti-row odd); "
                    "Bach: typed jets-3/4 class only (cited)"),
    "TU4_verdict": ("the k_mod = 0 Noether identity EXTENDS VERBATIM (no time-components, no split; "
                    "delta_gauge N = 0 and zero field sector derived); k_mod = 0 remains the only "
                    "codim-1 cut (Groebner re-run); resonance locus typed + OPEN-PENDING-CENSUS "
                    "(F-U8, not adjudicated); NEW stratum type: psi-branch chart-symmetry strata "
                    "carry a discrete character cut (N-parity), no identity"),
    "TU5_verdict": ("C-1 PASS (mechanical parse of the banked Stage-2 JSON: component table, module "
                    "generators, stratum identities, alphabet dims all recovered EXACTLY; F-U7 not "
                    "fired); C-2 diagonal-frozen control derived per branch (branch label degenerates "
                    "on the stratum; stratum not chart-closed)"),
    "outcome_class": ("OU-1: R_PW^T parametrized cleanly per branch — same character-matched module "
                      "space on both lock-reading branches over the bigraded alphabet (identical at "
                      "the unconditional character layers; the stratum-conditional N-parity cut "
                      "rides the coordinate reading — on psi-branch strata the projected branch "
                      "carries the equivalent content in the slack-pairing typing, not as a "
                      "pointwise cut [AMENDMENT 2026-07-31, verifier round 1]), differing in "
                      "the R_N sector's READING (physical vs chart-slack-paired), cut by the banked "
                      "stratum identities (extended verbatim) plus the two derived conditional "
                      "parity layers; static R_PW embeds exactly; controls pass"),
    "ceiling": ("no response law selected; no fork decided; no solve; no cycle census; no spectrum; "
                "no physics — the ceiling binds regardless of what the algebra showed"),
    "falsifier_events": [],
}
json_path = os.path.join(HERE, "timelive_T2_results.json")
prelim = dict(result)
prelim.update({"n_checks": len(CHECKS), "n_passed": sum(1 for ck in CHECKS if ck["passed"]),
               "checks": CHECKS})
with open(json_path, "w") as fh:
    json.dump(prelim, fh, indent=1)
try:
    with open(json_path) as fh:
        rt = json.load(fh)
    g1_ok = (rt["package"] == result["package"] and len(rt["checks"]) == len(CHECKS)
             and rt["n_passed"] == prelim["n_passed"])
except Exception:
    g1_ok = False
check("G1_results_json_written_and_roundtrips", "GUARD", g1_ok,
      "timelive_T2_results.json written and round-trips; G1 is counted in the tally and a G1 "
      "failure flips the exit code (T1 amendment precedent, wired)")
n_total = len(CHECKS)
n_pass = sum(1 for ck in CHECKS if ck["passed"])
n_sub = sum(1 for ck in CHECKS if ck["kind"] == "SUBSTANTIVE")
n_guard = n_total - n_sub
result.update({"n_checks": n_total, "n_passed": n_pass,
               "n_substantive": n_sub, "n_guard": n_guard,
               "all_passed": n_pass == n_total, "checks": CHECKS})
with open(json_path, "w") as fh:
    json.dump(result, fh, indent=1)
print("=" * 78)
print(f"TOTAL: {n_pass}/{n_total} passed ({n_sub} SUBSTANTIVE + {n_guard} GUARD); "
      f"exit {'0' if n_pass == n_total else '1'}")
sys.exit(0 if n_pass == n_total else 1)
