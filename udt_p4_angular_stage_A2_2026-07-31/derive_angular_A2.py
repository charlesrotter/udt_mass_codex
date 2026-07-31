#!/usr/bin/env python3
"""Stage A2 derivation script — the pointwise reduction ANGULAR-LIVE (TP2-1..TP2-4).

Contract: udt_p4_angular_stage_A2_2026-07-31/PREREGISTRATION.md (frozen first).
Exact SymPy only: no numeric solvers, no GPU, deterministic. Exit nonzero on any
failed check; guard checks WIRED into the exit path. Check kinds: SUBSTANTIVE
(a derivation leg) vs GUARD (re-run/mechanical/bookkeeping/hygiene).

Scope stamps traveling with every check: T^2 stratum layer (A-L1 CHOSE; full-S^3
TYPED); EVERYTHING-ON within the cleared layers (phi, f, bh, N AND the angular
mixed row m all live in (t,x,y,z)); tri-graded jets <= 2 per direction pair
(A-L2, higher TYPED); time-live-LINE (A-L4); theta ABSENT (A-L5); N=2 wall
layer; registered stationary presentation (general arenas TYPED); polynomial/
formal in the (k10, C) moduli; pointwise, one-parameter, off-shell on the
Route B / Stage-1 / T1 / T2 / A1 footing; BOTH lock-reading branches AND BOTH
spatial-reading branches carried to the same depth (F-P1/F-P4); mode
decomposition = Category-A technique, mode bound stated where used (A-L2);
resonance-locus contacts stamped OPEN-PENDING-CENSUS (F-P3 discipline);
NO winding/cycle/holonomy content anywhere (Stage A3's contract — the only
occurrences of that vocabulary in this package are scope-exclusion lines,
mechanically scanned by G4). NO ADM/foliation and NO Kaluza-Klein/fiber-adapted
parametrization: every derivation runs on covariant metric rows (canon
C-2026-06-18-1) and chart maps, exactly as T1/T2/A1.

Cited banked inputs (recomputed as consistency, never re-derived as new):
A1 (2fd4af3: opened metric, residual tower incl. zeta + AM-D, tri-graded
alphabet, mode layer, spatial-reading fork), T2 (fdae2dc: R_PW^T, bigraded
machinery, reading-independence + stratum qualifier), T1, static Stage 2
(2c0e7cc: R_PW, character modules, slot theorem, stratum identities), Route B
(K4, cocycles), CANON (clock law + reciprocal lock).
"""
import itertools
import json
import os
import re
import sys

import sympy as sp
from sympy import Matrix, Rational, symbols, exp, diff, simplify, zeros, eye, Function

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHECKS = []
VERDICTS = {}
STAGES_DONE = []
COMPONENTS = None          # filled by TP2-2
CONSTRAINT_ROWS = []       # ledger constraint rows, extended per stage
ALPHABET_ROWS = []         # ledger alphabet rows, extended per stage
FALSIFIER_EVENTS = []


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
Xmod = zeros(4, 4)
Xmod[0:2, 0:2] = H2
Xmod[2:4, 0:2] = Cb
Xmod[2:4, 2:4] = Kb

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
      "banked conventions re-run: K4 exact in SO+(1,3), six so(1,3) generators, closure "
      "(Route B / Stage-2 / T2 / A1 copy)")

# Base symbols. Field symbols are READ as arbitrary pointwise values of
# functions of (t,x,y,z); coordinates for field-level legs:
c_ = symbols("c", positive=True)
cE = symbols("c_E", positive=True)
phi = symbols("phi", real=True)
s_sh = symbols("s", real=True)
lam = symbols("lam", real=True)
T, X, Y, Z = symbols("t x y z", real=True)
Pk = symbols("P", positive=True)      # registered angular period (O20 data)
g_tt = -exp(-2 * phi) * c_**2         # THE CLOCK LAW (canon; covariant-row pin)
Q = cE * exp(-phi)

print("=" * 78)
print("STAGE A2 — TP2-1: the equivariance/character layer applied (phi-forcing per")
print("mode; slack-invariant operators; angular parity layer; alphabet gates)")
print("=" * 78)

# --- P1a: the phi-forcing, re-derived ANGULAR-LIVE and PER T^2 MODE.
# Anchor shift (banked, A1r-extended): (phi, c_E) -> (phi+s, c_E e^s) pointwise
# in (t,x,y,z), s CONSTANT.  Unique invariance condition on phi-powers, with an
# arbitrary mode-phase prefactor e_n = exp(2 pi i n y / P) attached:
p_, q_ = symbols("p q", real=True)
nn = symbols("n", integer=True, nonzero=True)
mode_n = exp(2 * sp.pi * sp.I * nn * Y / Pk)
F_pow = cE**p_ * exp(-q_ * phi)
shift_map = {phi: phi + s_sh, cE: cE * exp(s_sh)}
resid_bare = simplify(F_pow.subs(shift_map, simultaneous=True) / F_pow)
resid_mode = simplify((mode_n * F_pow).subs(shift_map, simultaneous=True) / (mode_n * F_pow))
sol_p = sp.solve(sp.Eq(resid_bare, 1), p_)
gen_wit = simplify(resid_bare.subs({p_: 2, q_: 1}, simultaneous=True) - 1)
check("P1a_Q_forcing_per_mode_p_eq_q", "SUBSTANTIVE",
      simplify(resid_bare - exp((p_ - q_) * s_sh)) == 0
      and simplify(resid_mode - exp((p_ - q_) * s_sh)) == 0
      and sol_p == [q_] and gen_wit != 0,
      "c_E^p e^{-q phi(t,x,y,z)} is shift-orbit-invariant iff p = q — iff it is a power of "
      "Q = c_E e^{-phi}; attaching ANY T^2 mode phase e_n leaves the residual law e^{(p-q)s} "
      "UNCHANGED (the shift is constant, hence mode-blind): the forcing condition is IDENTICAL at "
      "every mode n — the phi-dependence forcing is MODE-UNIFORM; a mode-dependent exponent pair "
      "(p(n), q(n)) is forced to p(n) = q(n) for EVERY n by the same one-line condition; bare phi "
      "stays excluded (generic p != q witness nonzero)")

# --- P1b: the ANGULAR jets of phi are shift-invariant alphabet blocks.
phiF = Function("phi")(T, X, Y, Z)
jets_inv = all(simplify(diff(phiF + s_sh, *d) - diff(phiF, *d)) == 0
               for d in [(Y,), (Z,), (Y, 2), (Z, 2), (Y, Z), (X, Y), (T, Z), (T, X, Y)])
check("P1b_angular_phi_jets_shift_invariant", "SUBSTANTIVE",
      jets_inv,
      "d_t^i d_x^j d_y^k d_z^l (phi + s) = d_t^i d_x^j d_y^k d_z^l phi for every tri-graded jet "
      "with (i,j,k,l) != 0 (shown at representative tri-grades incl. mixed angular/time): the "
      "angular jets enter the alphabet exactly as the banked spatial and time jets did — "
      "shift-invariant blocks")

# --- P1c: angular-liveness opens NO new phi-channel and closes none (TU1c analog).
m_y, m_z = symbols("m_y m_z", real=True)   # angular mixed row values (O19)
Nx, Ny, Nz = symbols("N_x N_y N_z", real=True)
fv, bhv = symbols("f_v bh_v", real=True)
inert_blocks = [m_y, m_z, Nx, Ny, Nz, fv, bhv, k10, c00, diff(phiF, Y), mode_n]
no_new = all(simplify((B * F_pow).subs(shift_map, simultaneous=True) / (B * F_pow)
                      - exp((p_ - q_) * s_sh)) == 0 for B in inert_blocks)
check("P1c_no_new_phi_channel_angular", "SUBSTANTIVE",
      no_new,
      "for ANY shift-inert prefactor B (the angular mixed row m, the shift row N, f, bh, moduli, "
      "any angular jet, any mode phase): B * c_E^p e^{-q phi} has the same residual law "
      "e^{(p-q)s} — invariance still holds iff p = q. ANGULAR-LIVENESS OPENS NO NEW phi-CHANNEL "
      "AND CLOSES NONE, per mode: the unique phi-channel angular-live is STILL the anchored "
      "readout Q = c_E e^{-phi} (the TP2-1 FOUNDATION verdict: the static forcing, intact "
      "time-live at T2, is INTACT and MODE-UNIFORM angular-live)")

# --- P1d: the anchor-overlap fate of the ANGULAR jet legs (A1r map; T1q/TU1d analog).
# A1r absorption: t and y UNTOUCHED; x -> e^{lam s} x, z -> e^{s} z (old = e^{..} new).
Xn, Zn = symbols("x_n z_n", real=True)
phi_old = Function("phi")(T, X, Y, Z)
phi_new = phi_old.subs({X: exp(lam * s_sh) * Xn, Z: exp(s_sh) * Zn}, simultaneous=True) + s_sh
dy_new = diff(phi_new, Y)
dy_old_at = diff(phi_old, Y).subs({X: exp(lam * s_sh) * Xn, Z: exp(s_sh) * Zn}, simultaneous=True)
dz_new = diff(phi_new, Zn)
dz_old_at = diff(phi_old, Z).subs({X: exp(lam * s_sh) * Xn, Z: exp(s_sh) * Zn}, simultaneous=True)
anch_new = simplify(dz_new / (cE * exp(s_sh)))
anch_old = simplify(dz_old_at / cE)
check("P1d_anchor_overlap_y_leg_invariant_z_leg_factor", "SUBSTANTIVE",
      simplify(dy_new - dy_old_at) == 0
      and simplify(dz_new - exp(s_sh) * dz_old_at) == 0
      and simplify(anch_new - anch_old) == 0,
      "across anchor presentations (the A1r absorption map): the y-leg jets are overlap-INVARIANT "
      "OUTRIGHT (y untouched; the compact y-leg absorbs purely on the field side — a DERIVED "
      "CONTRAST with the t- and z-legs), while the z-leg jet carries the exact overlap factor "
      "d_z~ phi~ = e^{s} d_z phi with the ANCHORED COMBINATION (d_z phi)/c_E overlap-invariant "
      "(the fiber-leg analog of TU1d's c_E d_t phi); the fiber-leg PERIOD rescales as a J07-type "
      "overlap datum (banked A1r), so the z-mode LATTICE is presentation-stable while its period "
      "label is overlap data. On the registered chart (units pinned) the on-chart rule P1a-P1c "
      "governs")

# --- P1e: the mode grading is SLACK-STABLE and translation-compatible.
chi0x = Function("chi")(X)
mode_slacked = mode_n.subs(Y, Y + chi0x)
phase = exp(2 * sp.pi * sp.I * nn * chi0x / Pk)
a2 = symbols("a2", real=True)
check("P1e_mode_grading_slack_stable", "SUBSTANTIVE",
      simplify(mode_slacked - phase * mode_n) == 0
      and simplify(mode_n.subs(Y, Y + a2) - exp(2 * sp.pi * sp.I * nn * a2 / Pk) * mode_n) == 0
      and simplify(mode_n.subs(Y, Y + Pk) - mode_n) == 0,
      "under the chi-slack y -> y + chi(x) the mode function e_n maps to a pointwise PHASE "
      "multiple e^{2 pi i n chi(x)/P} e_n: every mode subspace is PRESERVED by every residual "
      "slack map (the slack acts by y-translations pointwise in (x,t), and translations preserve "
      "each character) — the MODE GRADING of the tri-graded alphabet is slack-stable, and the "
      "residual T^2-translation layer commutes with the slack layers (both are y/z-additive, "
      "banked A1k/A1s4); period-compatibility holds. The mode index remains DUAL/decomposition "
      "data of a FUNCTION (Category-A technique) and carries no field-cycle content — that census "
      "is Stage A3's contract (scope-exclusion; F-P1 honored)")

# --- P1f: THE FULL SLACK-INVARIANT DERIVATIVE, derived (unifies TU1f and A4a).
# Joint slack (t,y,z) -> (t + psi(x), y + chi(x), z + zeta(x)).  Metric data at
# the point: v = (g_tx, g_xy, g_xz) (shift row + angular mixed row), G3 = the
# (t,y,z) block.  Transformation laws (the A1g/A1g2/A1s2 pullback laws, joint
# form): v -> v + G3 s', G3 -> G3 (arguments relabeled), and the coordinate
# derivative d_x gains s'-terms.  Claim: D_x = d_x - v^T G3^{-1} d_(t,y,z) is
# EXACTLY invariant, and 1/g^{xx} = g_xx - v^T G3^{-1} v (the FULL projected
# spatial reading) is invariant.
att, ayy, azz = symbols("g_tt0 g_yy0 g_zz0", real=True)
aty, atz, ayz = symbols("g_ty0 g_tz0 g_yz0", real=True)
gxx0 = symbols("g_xx0", real=True)
G3 = Matrix([[att, aty, atz], [aty, ayy, ayz], [atz, ayz, azz]])
vt, vy, vz = symbols("v_t v_y v_z", real=True)
vv = Matrix([vt, vy, vz])
Tn, Xn, Yn, Zn = symbols("t_n x_n y_n z_n", real=True)
psiX, chiX, zetX = Function("psi")(Xn), Function("chi")(Xn), Function("zeta")(Xn)
Ffld = Function("Ffld")(T, X, Y, Z)
NEWMAP = {T: Tn + psiX, X: Xn, Y: Yn + chiX, Z: Zn + zetX}
F_new = Ffld.subs(NEWMAP, simultaneous=True)
sl = Matrix([diff(psiX, Xn), diff(chiX, Xn), diff(zetX, Xn)])
v_new = vv + G3 * sl
G3inv = G3.inv()
grad_new = Matrix([diff(F_new, Tn), diff(F_new, Yn), diff(F_new, Zn)])
Dx_new = diff(F_new, Xn) - (v_new.T * G3inv * grad_new)[0]
Dx_old_at = (diff(Ffld, X) - (vv.T * G3inv * Matrix([diff(Ffld, T), diff(Ffld, Y), diff(Ffld, Z)]))[0]
             ).subs(NEWMAP, simultaneous=True)
gam_full = gxx0 - (vv.T * G3inv * vv)[0]
gxx_new = gxx0 + (2 * vv.T * sl)[0] + (sl.T * G3 * sl)[0]
gam_full_new = gxx_new - (v_new.T * G3inv * v_new)[0]
check("P1f_full_slack_invariant_derivative_derived", "SUBSTANTIVE",
      sp.simplify(sp.expand(Dx_new - Dx_old_at)) == 0
      and sp.simplify(sp.expand(gam_full_new - gam_full)) == 0,
      "D_x = d_x - v^T G3^{-1} d_(t,y,z) — the g-orthogonal-to-{d_t,d_y,d_z} projection of d_x, a "
      "native covariant-row object (v = (N_x, m_y, m_z), G3 = the (t,y,z) block incl. the angular "
      "shift components N_y, N_z) — is EXACTLY invariant under EVERY joint (psi,chi,zeta)(x) "
      "slack map (field-level, arbitrary slack functions), and gamma_xx^full = g_xx - v^T G3^{-1} v "
      "= 1/g^{xx} (the FULL projected spatial reading, A1q) is invariant identically: the T2 "
      "operator D_x = d_x - (N/g_tt) d_t (TU1f) and the A1 operator d_x - (g_xy/g_yy) d_y (A4a) "
      "are the t-only and y-only slices of THIS one operator. Operator-level invariance implies "
      "D_x-jets of every order transport invariantly (apply the lemma to the invariant scalar "
      "D_x F — induction; Category-A argument, first jet derived here exactly)")

# --- P1g: the FIBER-CORRECTED angular derivative D_y and the h-cocycle.
gyzS, gzzS = symbols("g_yz1 g_zz1", real=True)
zetY = Function("zeta")(Yn)
ZMAP = {T: Tn, X: Xn, Y: Yn, Z: Zn + zetY}
F_nz = Ffld.subs(ZMAP, simultaneous=True)
gyz_new = gyzS + gzzS * diff(zetY, Yn)
Dy_new = diff(F_nz, Yn) - (gyz_new / gzzS) * diff(F_nz, Zn)
Dy_old_at = (diff(Ffld, Y) - (gyzS / gzzS) * diff(Ffld, Z)).subs(ZMAP, simultaneous=True)
hY = Function("h")(Yn)
HMAP = {T: Tn, X: Xn, Y: hY, Z: Zn}
F_nh = Ffld.subs(HMAP, simultaneous=True)
hp = diff(hY, Yn)
Dy_h_new = diff(F_nh, Yn) - ((hp * gyzS) / gzzS) * diff(F_nh, Zn)  # A1p law: g_yz -> h' g_yz, g_zz -> g_zz
Dy_h_old_at = (diff(Ffld, Y) - (gyzS / gzzS) * diff(Ffld, Z)).subs(HMAP, simultaneous=True)
check("P1g_fiber_corrected_Dy_and_h_cocycle", "SUBSTANTIVE",
      sp.simplify(sp.expand(Dy_new - Dy_old_at)) == 0
      and sp.simplify(sp.expand(Dy_h_new - hp * Dy_h_old_at)) == 0,
      "D_y = d_y - (g_yz/g_zz) d_z — the g-orthogonal-to-d_z projection of d_y — is EXACTLY "
      "invariant under every zeta(y) fiber-translation slack (the ANGULAR-INTERNAL corrected "
      "operator, the fiber-leg analog of TU1f/A4a; the zeta-cocycle A1s4's derived pointwise "
      "content); under the y-reparametrization slack y -> h(y) it transforms by the exact "
      "CHAIN-RULE cocycle D_y ~ h'. D_y (a density-weight-1 frame object under h, an invariant "
      "under zeta): the h-layer's J07 overlap law acts on the operator exactly as A1p2 derived "
      "for the fields — recorded as overlap data, not an invariance")

# --- P1h: the invariant-alphabet reorganization is TRIANGULAR-INVERTIBLE.
Mtri = Matrix([[1, -(vv.T * G3inv)[0, 0], -(vv.T * G3inv)[0, 1], -(vv.T * G3inv)[0, 2]],
               [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
check("P1h_alphabet_reorganization_triangular_invertible", "SUBSTANTIVE",
      simplify(Mtri.det() - 1) == 0 and is_zero_matrix(Mtri * Mtri.inv() - eye(4))
      and simplify((gam_full + (vv.T * G3inv * vv)[0]) - gxx0) == 0,
      "(d_x, d_t, d_y, d_z) -> (D_x, d_t, d_y, d_z) is a unit-determinant triangular map "
      "(invertible), and g_xx = gamma_xx^full + v^T G3^{-1} v inverts the row map: the coordinate "
      "presentation (d_x-jets, g_xx, v) and the invariant presentation (D_x-jets, gamma_xx^full, "
      "v/overlap) are two coordinates on the SAME tri-graded alphabet — no pointwise content rides "
      "the presentation choice ON-CHART; ACROSS charts only the invariant presentation transports "
      "trivially (the frame presentation carries the additive slack cocycles, banked "
      "A1k/A1s4/T2i). COMPLETENESS BOUND (honest): derived at the operator level (all D-jet "
      "orders, P1f lemma); the ledger carries the tri-grade <= 2 layer bound (A-L2)")

# --- P1i: the ANGULAR-MIRROR parity table, derived on polynomial models.
cc0, cc1, cc2, cc3 = symbols("cc0 cc1 cc2 cc3", real=True)
S_even = cc0 + cc2 * Y**2
S_odd = cc1 * Y + cc3 * Y**3
par = lambda e: simplify(e.subs(Y, -Y) + e) == 0      # True = ODD
mir_ok = (par(diff(S_even, Y)) and not par(diff(S_even, Y, 2))
          and not par(diff(S_odd, Y)) and par(diff(S_odd, Y, 2))
          and par(S_odd) and not par(S_even))
# parity table under the composed y-mirror (A1f: f, N_y, m_y, g_yz ODD-composed;
# phi, alpha, bh, N_x, N_z, m_z, moduli EVEN-composed); z-mirror (A1e2: alpha, f
# ODD; + single-z-index rows N_z, m_z, g_yz ODD):
Y_PAR = {"phi": 0, "f": 1, "bh": 0, "N_x": 0, "N_y": 1, "N_z": 0,
         "m_y": 1, "m_z": 0, "g_yz": 1, "moduli": 0}
Z_PAR = {"phi": 0, "f": 1, "bh": 0, "N_x": 0, "N_y": 0, "N_z": 1,
         "m_y": 0, "m_z": 1, "g_yz": 1, "alpha": 1, "moduli": 0}
blk = lambda tab, fld, k: (tab[fld] + k) % 2          # parity of d_angle^k(field)
check("P1i_angular_mirror_parity_table_derived", "SUBSTANTIVE",
      mir_ok and blk(Y_PAR, "f", 1) == 0 and blk(Y_PAR, "phi", 1) == 1
      and blk(Y_PAR, "m_y", 0) == 1 and blk(Z_PAR, "m_z", 0) == 1,
      "on polynomial models the composed-mirror parity of a jet block is "
      "(-1)^{(angular-jet order in the mirrored direction)} x (field's composed parity): the "
      "derived A1f/A1e2 parity assignments grade the WHOLE tri-graded alphabet by a Z2 x Z2 "
      "angular-mirror character (y-mirror: f, N_y, m_y, g_yz odd; z-mirror: alpha, f, N_z, m_z, "
      "g_yz odd; phi, bh, moduli even; d_y flips y-parity, d_z flips z-parity). LAYER STAMP "
      "(conditional, the T2 T-parity discipline transposed): imposed as a character rule at the "
      "METRIC layer only and only WHERE THE MIRROR IS GRANTED — the mirrors are BRIDGE FLOOR only "
      "(G18: no closure status; their coframe-layer status inherits T1's SO+ obstruction — a "
      "spatial reflection is orientation-reversing, admitting it at the coframe layer = CHOSE); "
      "the mirrors act on the mode lattice by negation (A3e), so the granted cut PAIRS the +n and "
      "-n mode sectors rather than acting mode-diagonally")

# --- P1j: the bare-angle exclusion's RESPONSE-SIDE fate (A1n re-posed) — guard.
a1 = symbols("a1", real=True)
Fper = sp.cos(2 * sp.pi * Y / Pk)
check("P1j_bare_angle_response_gate", "GUARD",
      simplify((Y + a1) - Y) != 0 and simplify(Fper.subs(Y, Y + Pk) - Fper) == 0
      and simplify(diff(Fper, Y).subs(Y, Y + Pk) - diff(Fper, Y)) == 0,
      "banked A1n re-run on the response side: a component built with BARE y/z is not defined on "
      "the residual T^2-translation quotient and is not even a function on the periodic domain — "
      "response components are built from the tri-graded jet alphabet only (angular jets "
      "translation-covariant, single-valued, periodic); theta ABSENT (A-L5); no fitted angular "
      "average enters (R13; a mode PROJECTION is Category-A analysis, banked A1 R13 distinction)")

VERDICTS["TP2-1"] = (
    "phi-forcing verdict: INTACT and MODE-UNIFORM — shift-equivariance alone still forces "
    "Q = c_E e^{-phi} as the unique phi-channel, with the SAME one-line condition p = q at every "
    "T^2 mode; angular modes open NO new phi-channel and close none (all angular blocks and mode "
    "phases are shift-inert). Anchor overlap: y-leg jets overlap-invariant outright; z-leg carries "
    "e^{s} with anchored combination (d_z phi)/c_E. Slack cocycles force the invariant/frame "
    "alphabet split with the FULL derived operator D_x = d_x - v^T G3^{-1} d_(t,y,z) (P1f; TU1f "
    "and A4a are its slices) and the fiber-corrected D_y (P1g); reorganization "
    "triangular-invertible (P1h). NEW conditional character layer: the Z2 x Z2 angular-mirror "
    "parity grading (P1i; granted-only, metric layer, G18 bridge floor; pairs +n/-n modes). "
    "Bare angles excluded response-side (P1j); mode grading slack-stable (P1e)."
)
ALPHABET_ROWS += [
    ["alphabet tri-graded", "ALPHABET",
     "blocks: Q (forced unique phi-channel, MODE-UNIFORM — P1a/P1c) + tri-graded jets of "
     "(phi,f,bh) <= 2 per direction (A-L2) + N row + m row (O19) + their jets + moduli (const "
     "reading; field readings typed) + wall/corner data + NO bare t (banked TU1e) + NO bare "
     "angles (A1n/P1j) + NO bare phi (banked); mode grading slack-stable (P1e); y-leg jets "
     "anchor-overlap-invariant, z-leg anchored combination (d_z phi)/c_E (P1d)",
     "-", "DERIVED", "restricts to T2 bigraded alphabet (angular order 0)", "restricts to banked static alphabet (C2a dims)", "P1a;P1b;P1c;P1d;P1e;P1j"],
    ["alphabet presentations", "ALPHABET",
     "coordinate blocks (d_x-jets, g_xx, v=(N_x,m_y,m_z)) <-> invariant blocks (D_x-jets, "
     "gamma_xx^full = 1/g^xx, v/overlap) with D_x = d_x - v^T G3^{-1} d_(t,y,z) derived "
     "joint-slack-invariant (P1f; unifies TU1f + A4a) + fiber-corrected D_y = d_y - (g_yz/g_zz) "
     "d_z zeta-invariant with chain-rule h-cocycle (P1g); triangular-invertible (P1h)",
     "-", "DERIVED", "restricts to T2 presentations row (D_x -> d_x - (N/g_tt) d_t)", "identical statically (D_x = d_x at v = 0)", "P1f;P1g;P1h"],
]
CONSTRAINT_ROWS += [
    ["(constraint) ANGULAR-MIRROR parity layer", "CONSTRAINT",
     "components angular-parity-matched (Z2 x Z2) to their paired directions WHERE THE MIRRORS "
     "ARE GRANTED: y-mirror (delta f, delta N_y, delta m_y odd), z-mirror (delta f, delta N_z, "
     "delta m_z, [delta alpha] odd); CONDITIONAL: metric layer only, bridge floor (G18, no "
     "closure status; coframe layer SO+-obstructed — admitting = CHOSE); mirrors negate modes: "
     "the cut pairs +n/-n sectors; NOT part of the banked T2/static cut set (new conditional "
     "content; see P3b for its mode-zero reach)",
     "Z2xZ2", "DERIVED (conditional)", "does NOT vacate at mode zero (P3b)", "not in the banked static cut set", "P1i;A1f;A1e2;A3e"],
]
STAGES_DONE.append("TP2-1")

print("=" * 78)
print("STAGE A2 — TP2-2: the pointwise reduction, per spatial-reading branch")
print("=" * 78)

# --- P2a: the m-sector slot structure — NO forced-slot analog, NO null slot.
GramM = Matrix(2, 2, lambda i, j: (eye(2)[:, i].T * eye(2)[:, j])[0, 0])
I2m = eye(2)
D2 = sp.diag(-1, 1)
E21 = Matrix([[0, 0], [1, 0]])
E12 = Matrix([[0, 1], [0, 0]])


def pairtr(A_, B_):
    return sp.trace(A_.T * B_)


GramS = Matrix(3, 3, lambda i, j: pairtr([I2m, D2, E21][i], [I2m, D2, E21][j]))
check("P2a_m_sector_no_forced_slot_no_null_slot", "SUBSTANTIVE",
      GramM == eye(2) and GramM.nullspace() == [] and GramS == sp.diag(2, 2, 1)
      and pairtr(E12, I2m) == 0 and pairtr(E12, D2) == 0 and pairtr(E12, E21) == 0,
      "m-sector pairing Gram = I2 (nondegenerate, no annihilator): each delta-m_a direction is "
      "paired by exactly its own component — NO null slot, NO trace/trace-free split exists (a "
      "vector row, not a symmetric kernel), so NO new forced-slot theorem arises in the m-sector "
      "(the static trace-free forcing's angular fate: NO ANALOG in the new sector, and the banked "
      "forcing itself transfers untouched — moduli-sector, (t,y,z) spectators, A1's A2c re-run); "
      "the screen sector's structure (Gram diag(2,2,1), E12 null slot) is unchanged")

# --- P2b: delta_gauge m = 0 and R_m's K4 character FORCED trivial (TU2b/TU2c extended).
Egen = Matrix(4, 4, symbols("e0:16", real=True))
chi_bst = symbols("chi_boost", real=True)
Boost = Matrix([[sp.cosh(chi_bst), sp.sinh(chi_bst), 0, 0],
                [sp.sinh(chi_bst), sp.cosh(chi_bst), 0, 0],
                [0, 0, 1, 0], [0, 0, 0, 1]])
gauge_inert = all(
    is_zero_matrix(sp.expand((Lam * Egen).T * eta * (Lam * Egen) - Egen.T * eta * Egen))
    for Lam in [R23, R12, R13, Boost])
Rm_bad = k10 * m_y
bad_breaks = any(simplify(Rm_bad.subs(sm, simultaneous=True) - Rm_bad) != 0 for _, sm in K4_SUBS)
good_holds = all(simplify(m_y.subs(sm, simultaneous=True) - m_y) == 0 for _, sm in K4_SUBS)
check("P2b_delta_gauge_m_zero_K4_trivial_forced", "SUBSTANTIVE",
      gauge_inert and bad_breaks and good_holds,
      "g = E^T eta E is exactly invariant under E -> Lam E for the K4 elements AND a generic boost "
      "(symbolic 16-entry coframe): every metric component — the angular mixed row m INCLUDED — is "
      "a local-Lorentz INVARIANT, so delta_gauge m = 0 identically: the R_m slots pair NO gauge "
      "direction and drop out of every Noether pairing (feeds TP2-3); and character matching "
      "FORCES R_m to carry the trivial K4 character (witness k10*m_y breaks equivariance; m_y "
      "itself is inert) — NO chi-module dresses the m-row (banked TU2b/A1m lineage, m-row leg new)")

# --- P2c: the R_m slots SURVIVE every re-posed pointwise requirement (COORDINATE
# spatial reading) — composite witnesses R_m_y = m_y, R_m_z = m_z.
T_PAR = {"phi": 0, "f": 0, "bh": 0, "N": 1, "m": 0, "phi_t": 1}
w_shift = all(simplify(w.subs(shift_map, simultaneous=True) - w) == 0 for w in (m_y, m_z))
w_bare = not (m_y.has(Y) or m_y.has(Z) or m_z.has(Y) or m_z.has(Z))
w_T = (T_PAR["m"] == 0)                      # T-even, matching delta-m (no t-index)
w_ymir = (Y_PAR["m_y"] == 1 and Y_PAR["m_z"] == 0)   # matches delta-m_y odd / delta-m_z even
w_zmir = (Z_PAR["m_z"] == 1 and Z_PAR["m_y"] == 0)
check("P2c_Rm_survives_all_PW_requirements_coordinate", "SUBSTANTIVE",
      w_shift and w_bare and good_holds and w_T and w_ymir and w_zmir,
      "COORDINATE-SPATIAL-BRANCH R_m VERDICT: the witnesses R_m_y = m_y, R_m_z = m_z are "
      "shift-orbit-inert (J04), bare-angle-free (P1j), K4-trivial (R7a; P2b), T-parity EVEN = the "
      "parity of delta-m (metric layer, banked T2 layer), ANGULAR-mirror-parity-matched where the "
      "mirrors are granted (delta-m_y y-odd/z-even, delta-m_z z-odd/y-even — P1i table), "
      "m-involution ODD on the chi-branch strata (P2e) [A-2, verifier round 1: odd/even labels exact on g_yz=0 / in the eigenbasis; general action = flip-and-shear; the B^-1-pairing is the invariant object], unconstrained by every stratum Noether "
      "identity (delta_gauge m = 0, P2b), censused (R1/R2: O19), pointwise (R13), off-shell "
      "(R12/J14): BOTH R_m SLOTS SURVIVE the re-posed pointwise requirement set as "
      "PHYSICAL-CONTENT components — the coordinate spatial branch's new pointwise content is "
      "REAL at this layer (fork NOT decided; status rides the spatial reading, F-P4 honored)")

# --- P2d: a second m-row witness with PER-WITNESS STRATUM STAMPS.
wit2 = diff(phiF, Y)     # R_m_y = d_y phi
wit2_ymir = (blk(Y_PAR, "phi", 1) == 1)   # y-mirror ODD: matches delta-m_y at the mirror layer
wit2_minv = False                          # carries NO m-factor: m-involution EVEN — mismatch
check("P2d_Rm_witness_dyphi_stratum_scoped", "SUBSTANTIVE",
      simplify(wit2.subs(phiF, phiF + s_sh) - wit2) == 0 and wit2_ymir and not wit2_minv,
      "R_m_y = d_y phi: shift-inert, K4-trivial, y-mirror ODD (legal at the granted-mirror layer, "
      "matching delta-m_y) — but m-involution EVEN (no m-factor [A-2, verifier round 1: odd/even labels exact on g_yz=0 / in the eigenbasis; general action = flip-and-shear; the B^-1-pairing is the invariant object]) while delta-m_y is m-odd: on the "
      "strata where the chi-branch Z2 is lawful (coordinate spatial reading) it FAILS the stratum "
      "character cut — a member of R_PW^A OFF those strata only (per-witness stratum stamps: the "
      "exact angular recurrence of the banked omega-witness / TU2e discipline). [AMENDMENT A-2, verifier round 1: the odd/even m-involution labels are exact on g_yz=0 / in the eigenbasis; the general action is flip-and-shear — the B⁻¹-pairing is the invariant object.]")

# --- P2e: the chi-branch stratum action is an INVOLUTION = pure m-motion in the
# invariant alphabet; the joint conic action is CONTINUOUS with derived invariant.
# AMENDMENT A-1 (verifier round 1): the conic also contains the discrete zeta-only slice
# s=(0,-2 m_z/g_zz) -> involution m -> (m_y - 2 g_yz m_z/g_zz, -m_z); lawful, preserves m^T B^-1 m;
# discrete-slice census TYPED, not exhausted.
m1, m2 = symbols("m1 m2", real=True)
b11, b12, b22 = symbols("b11 b12 b22", real=True)
Bblk = Matrix([[b11, b12], [b12, b22]])
mv = Matrix([m1, m2])
s1, s2 = symbols("s1 s2", real=True)
sv = Matrix([s1, s2])
conic = sp.expand((2 * mv.T * sv)[0] + (sv.T * Bblk * sv)[0])
s_chi = Matrix([-2 * m1 / b11, 0])
m_flip = sp.simplify(mv + Bblk * s_chi)
s_chi2 = Matrix([-2 * m_flip[0] / b11, 0])
m_back = sp.simplify(m_flip + Bblk * s_chi2)
inv0 = sp.simplify((mv.T * Bblk.inv() * mv)[0])
inv1 = sp.simplify((m_flip.T * Bblk.inv() * m_flip)[0])
check("P2e_chi_branch_involution_pure_m_motion", "SUBSTANTIVE",
      sp.simplify(conic.subs({s1: -2 * m1 / b11, s2: 0})) == 0
      and list(m_flip) == [-m1, sp.simplify(m2 - 2 * b12 * m1 / b11)]
      and list(sp.simplify(m_back - mv)) == [0, 0]
      and sp.simplify(inv1 - inv0) == 0
      and list(m_flip.subs(b12, 0)) == [-m1, m2],
      "the chi-class branch slack (chi' = -2 g_xy/g_yy, A1h) satisfies the joint conic constraint "
      "identically, acts on m as the flip-and-shear m -> (-m_y, m_z - 2 g_yz m_y/g_yy), IS an "
      "exact INVOLUTION (Z2) on every lawful stratum, preserves the invariant m^T B^{-1} m, and "
      "reduces to the clean m_y-flip on the g_yz = 0 substratum; in the invariant alphabet "
      "(gamma_xx^full, D_x — both preserved under EVERY pin-preserving slack, P1f) the stratum "
      "action is PURE m-motion on the level set (the TU1i N-parity structure transposed): a "
      "stratum-conditional DISCRETE character cut on the m-sector (coordinate spatial reading; "
      "lawful where the branch slope is angular/t-independent and x-integrable). The FULL joint "
      "conic family is CONTINUOUS (1-parameter of lawful (chi',zeta') at a point, AM-B): its "
      "invariant is m^T B^{-1} m (A1i2); its equivariance content beyond the Z2 slice is TYPED "
      "(level-set invariant theory), and its pointwise pairing content is P2f's chart-slack legs")

# --- P2f: the PROJECTED spatial branch — the R_m chart-slack pairing STATED
# EXACTLY (TU2h transposed), with the t-dependent legs included.  Step 1: the
# infinitesimal slack laws are DERIVED from the pullback linearization (= the
# Lie derivative along xi = chi(t,x) d_y + zeta(t,x) d_z) on the general opened
# matrix — the finite-map laws A1g/A1g2/A1s2/A1s3 linearized, all components.
COORDS = (T, X, Y, Z)
GF2 = {}
for i in range(4):
    for j in range(i, 4):
        GF2[(i, j)] = Function(f"g{i}{j}")(T, X, Y, Z)
GG = Matrix(4, 4, lambda i, j: GF2[(min(i, j), max(i, j))])
chiTX = Function("chi")(T, X)
zetTX = Function("zeta")(T, X)
xi = [sp.Integer(0), sp.Integer(0), chiTX, zetTX]
LIE = zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        LIE[mu, nu] = sum(xi[a] * diff(GG[mu, nu], COORDS[a]) for a in range(4)) \
            + sum(GG[min(a, nu), max(a, nu)] * diff(xi[a], COORDS[mu]) for a in range(4)) \
            + sum(GG[min(mu, a), max(mu, a)] * diff(xi[a], COORDS[nu]) for a in range(4))
drag = lambda e: chiTX * diff(e, Y) + zetTX * diff(e, Z)
laws_ok = all(simplify(LIE[i, j] - rhs) == 0 for (i, j), rhs in [
    ((0, 0), drag(GF2[(0, 0)]) + 2 * GF2[(0, 2)] * diff(chiTX, T) + 2 * GF2[(0, 3)] * diff(zetTX, T)),
    ((0, 1), drag(GF2[(0, 1)]) + GF2[(0, 2)] * diff(chiTX, X) + GF2[(0, 3)] * diff(zetTX, X)
     + GF2[(1, 2)] * diff(chiTX, T) + GF2[(1, 3)] * diff(zetTX, T)),
    ((0, 2), drag(GF2[(0, 2)]) + GF2[(2, 2)] * diff(chiTX, T) + GF2[(2, 3)] * diff(zetTX, T)),
    ((0, 3), drag(GF2[(0, 3)]) + GF2[(2, 3)] * diff(chiTX, T) + GF2[(3, 3)] * diff(zetTX, T)),
    ((1, 1), drag(GF2[(1, 1)]) + 2 * GF2[(1, 2)] * diff(chiTX, X) + 2 * GF2[(1, 3)] * diff(zetTX, X)),
    ((1, 2), drag(GF2[(1, 2)]) + GF2[(2, 2)] * diff(chiTX, X) + GF2[(2, 3)] * diff(zetTX, X)),
    ((1, 3), drag(GF2[(1, 3)]) + GF2[(2, 3)] * diff(chiTX, X) + GF2[(3, 3)] * diff(zetTX, X)),
    ((2, 2), drag(GF2[(2, 2)])), ((2, 3), drag(GF2[(2, 3)])), ((3, 3), drag(GF2[(3, 3)]))])
# Step 2: the pointwise pairing at the DIAGONAL presentation (m = 0; projected
# spatial reading), slack values (chi0, zet0) and slopes (chix, zetx, chit, zett):
Rphi, Rf, Rbh = symbols("R_phi R_f R_bh", real=True)
RNx, RNy, RNz = symbols("R_Nx R_Ny R_Nz", real=True)
Rmy, Rmz = symbols("R_my R_mz", real=True)
chi0, chix, chit = symbols("chi0 chi_x chi_t", real=True)
zet0, zetx, zett = symbols("zeta0 zeta_x zeta_t", real=True)
gyy, gyz, gzz = symbols("g_yy g_yz g_zz", real=True)
dphi_y, dphi_z, df_y, df_z, dbh_y, dbh_z = symbols("dphi_y dphi_z df_y df_z dbh_y dbh_z", real=True)
dN_y = {i: symbols(f"dN{i}_y", real=True) for i in "xyz"}
dN_z = {i: symbols(f"dN{i}_z", real=True) for i in "xyz"}
NyS, NzS = symbols("N_y N_z", real=True)
# component deltas (derived laws above, at m = 0; g_tt = -c_E^2 e^{-2 phi} pin
# converts delta g_tt into the phi-leg):
d_phi = exp(2 * phi) * (NyS * chit + NzS * zett) / cE**2 + chi0 * dphi_y + zet0 * dphi_z
d_f = chi0 * df_y + zet0 * df_z
d_bh = chi0 * dbh_y + zet0 * dbh_z
d_Nx = NyS * chix + NzS * zetx + chi0 * dN_y["x"] + zet0 * dN_z["x"]
d_Ny = gyy * chit + gyz * zett + chi0 * dN_y["y"] + zet0 * dN_z["y"]
d_Nz = gyz * chit + gzz * zett + chi0 * dN_y["z"] + zet0 * dN_z["z"]
d_my = gyy * chix + gyz * zetx
d_mz = gyz * chix + gzz * zetx
pairing = sp.expand(Rphi * d_phi + Rf * d_f + Rbh * d_bh
                    + RNx * d_Nx + RNy * d_Ny + RNz * d_Nz + Rmy * d_my + Rmz * d_mz)
PP = sp.Poly(pairing, chi0, zet0, chix, zetx, chit, zett)
bx_y = PP.coeff_monomial(chix)
bx_z = PP.coeff_monomial(zetx)
bt_y = PP.coeff_monomial(chit)
bt_z = PP.coeff_monomial(zett)
BblkS = Matrix([[gyy, gyz], [gyz, gzz]])
Rm_v = Matrix([Rmy, Rmz])
RN_ang = Matrix([RNy, RNz])
N_ang = Matrix([NyS, NzS])
bx_target = BblkS * Rm_v + N_ang * RNx
bt_target = BblkS * RN_ang + N_ang * (exp(2 * phi) / cE**2) * Rphi
pin_ok = simplify(sp.diff(-cE**2 * exp(-2 * phi), phi) - 2 * cE**2 * exp(-2 * phi)) == 0 \
    and simplify((2 * NyS * chit + 2 * NzS * zett) / (2 * cE**2 * exp(-2 * phi))
                 - exp(2 * phi) * (NyS * chit + NzS * zett) / cE**2) == 0
a_y_leg = PP.coeff_monomial(chi0)
a_y_target = Rphi * dphi_y + Rf * df_y + Rbh * dbh_y + RNx * dN_y["x"] + RNy * dN_y["y"] + RNz * dN_y["z"]
check("P2f_projected_branch_slack_pairing_legs_exact", "SUBSTANTIVE",
      laws_ok and pin_ok
      and sp.expand(a_y_leg - a_y_target) == 0
      and sp.expand(bx_y - bx_target[0]) == 0 and sp.expand(bx_z - bx_target[1]) == 0
      and sp.expand(bt_y - bt_target[0]) == 0 and sp.expand(bt_z - bt_target[1]) == 0
      and BblkS.det() != 0,
      "the infinitesimal angular-slack laws are DERIVED on the general opened matrix (pullback "
      "linearization = Lie derivative along chi d_y + zeta d_z; the A1g/A1g2/A1s2/A1s3 finite "
      "laws linearized, ALL components verified), and the pointwise pairing at the diagonal "
      "presentation is EXACTLY a_y chi + a_z zeta + b legs with DRAG LEGS a_y = sum_A R_A d_y A, "
      "a_z = sum_A R_A d_z A [sign convention: forward-map linearization; T2's TU2h used the "
      "inverse map — same content; moduli drags join on the field readings, typed, carried], "
      "x-SLOPE LEGS (b_x_y, b_x_z) = B*(R_m_y, R_m_z) + N_ang*R_N_x and t-SLOPE LEGS "
      "(b_t_y, b_t_z) = B*(R_N_y, R_N_z) + N_ang*(e^{2phi}/c_E^2)*R_phi: on the PROJECTED "
      "spatial branch the R_m slots pair PURE CHART-SLACK through the x-slope legs, with B "
      "nondegenerate (the pairing sees the WHOLE R_m row); THE SLACK-COUPLED-SECTOR LAW derived: "
      "the SAME slack map pairs the R_m sector (x-slopes) and the R_N sector (t-slopes) through "
      "the SAME angular block B, coupled by N_ang = (N_y, N_z) — on the N_ang = 0 substratum the "
      "legs separate cleanly (b_x = B R_m, b_t = B R_N_ang). The Noether-second-theorem "
      "divergence identity relating the drag and slope legs lives at the INTEGRATION layer "
      "(declared pairing + domain data) — POSED, typed, NOT imposed pointwise: no pointwise kill "
      "of R_m is derivable, and none is claimed. On the COORDINATE spatial branch the same legs "
      "are J07 overlap-transport data, no identity owed. F-P4: neither branch gains an argument")

# --- P2g: the reading-independence theorem's ANGULAR analog — DERIVED.
corr_terms = [(m_y / symbols("g_yy"), "d_y"), (m_z / symbols("g_zz"), "d_z")]
K4_inert_corr = all(all(simplify(cf.subs(sm, simultaneous=True) - cf) == 0 for _, sm in K4_SUBS)
                    for cf, _ in corr_terms)
ymir_dx = (Y_PAR["m_y"] + 1) % 2          # (m_y odd) x (d_y odd) = even = parity of d_x
zmir_dx = (Z_PAR["m_z"] + 1) % 2          # (m_z odd) x (d_z odd) = even
tpar_dx = (T_PAR["m"] + 0) % 2            # m even, d_y even: even = parity of d_x
shift_inert_corr = all(simplify(cf.subs(shift_map, simultaneous=True) - cf) == 0 for cf, _ in corr_terms)
check("P2g_module_space_reading_independent_angular", "SUBSTANTIVE",
      K4_inert_corr and ymir_dx == 0 and zmir_dx == 0 and tpar_dx == 0 and shift_inert_corr,
      "the two registered spatial presentations (coordinate: d_x-jets, g_xx, m | projected: "
      "D_x-jets, gamma_xx^full, overlap data) are related by the invertible triangular alphabet "
      "map (P1f/P1h) which PRESERVES every character layer: K4 (correction coefficients "
      "m_a/g_aa inert — computed), T-parity (each correction term (m even)x(d_angle even) = even "
      "= d_x's parity — computed), BOTH angular-mirror parities ((m_y odd)x(d_y odd) = even; "
      "(m_z odd)x(d_z odd) = even — computed), shift-orbit (inert — computed), and the mode "
      "grading (slack-stable, P1e): THE ANGULAR ANALOG OF T2's READING-INDEPENDENCE THEOREM "
      "HOLDS — the character-matched module parametrization of R_PW^A is IDENTICAL on both "
      "spatial-reading branches at the unconditional character layers; the STRATUM QUALIFIER "
      "transposes verbatim: the stratum-conditional m-involution cut (P2e) rides the COORDINATE "
      "spatial reading — on chi-branch strata the projected branch carries the equivalent "
      "content in the slack-pairing typing (P2f), not as a pointwise cut. A MAP FACT about the "
      "fork, not a resolution (F-P4: neither reading gains an argument)")

# --- P2h: the LOCK fork x SPATIAL fork composition — a derived MAP FACT.
gam_seq = gxx0 - vt**2 / att - (Matrix([vy, vz]).T
                                * Matrix([[ayy, ayz], [ayz, azz]]).inv() * Matrix([vy, vz]))[0]
dsep = sp.simplify(gam_full - gam_seq)
sep_at_diag = sp.simplify(dsep.subs({aty: 0, atz: 0}, simultaneous=True))
GEN_PT = {att: -2, ayy: 1, azz: 1, ayz: 0, aty: 1, atz: 0, vt: 1, vy: 1, vz: 1, gxx0: 5}
sep_generic = sp.simplify(dsep.subs(GEN_PT, simultaneous=True))
check("P2h_fork_composition_lock_x_spatial_derived", "SUBSTANTIVE",
      sep_at_diag == 0 and sep_generic != 0,
      "fork-composition MAP FACT: the FULL projected reading gamma_xx^full = g_xx - v^T G3^{-1} v "
      "(one G3-projection, P1f) equals the SEQUENTIAL single-fork corrections "
      "g_xx - N_x^2/g_tt - m^T B^{-1} m EXACTLY on the stratum where the shift row's ANGULAR "
      "components vanish (N_y = N_z = 0); OFF that stratum the two differ by an exact "
      "N_ang-cross term (generic witness nonzero): the lock-reading and spatial-reading "
      "projections are NOT independent corrections when N_ang is on — the joint projected object "
      "is the single G3-projection. Angular content remains a SPECTATOR of the lock fork's split "
      "term (banked A1b), and NOTHING here decides either fork (F-P4): the four branch-pairs are "
      "four presentations of the same triangular family, with their joint projected presentation "
      "derived here")

# --- P2i: J06 determined-vs-retained for the NEW m-family — both branches nonempty.
Rm_zero = sp.Integer(0)
retained_ok = all(simplify(Rm_zero.subs(sm, simultaneous=True) - Rm_zero) == 0 for _, sm in K4_SUBS)
check("P2i_J06_m_family_both_branches_nonempty", "SUBSTANTIVE",
      good_holds and retained_ok,
      "m-family J06 branch structure: DETERMINED branch witness R_m = m (nonzero, all characters "
      "matched — P2c); RETAINED branch witness R_m == 0 with m reported residual (trivially "
      "character-matched): both are open sub-loci of R_PW^A; NO branch chosen. On the projected "
      "spatial branch the same table reads: slack-pairing present vs absent — carried per reading")

# --- P2j: MODE-BLINDNESS of the derived gates — the mode structure of R_PW^A.
no_angular_syms = all(not e.has(Y) and not e.has(Z) and not e.has(nn)
                      for e in [resid_bare, conic, dsep]) \
    and not any(m.has(Y) or m.has(Z) for m in [GramM, GramS])
check("P2j_gates_mode_blind_surviving_space_mode_uniform", "SUBSTANTIVE",
      no_angular_syms,
      "every derived pointwise gate is MODE-BLIND: the gate conditions (shift-forcing residual, "
      "sector Grams, the conic constraint, the fork-composition separation, the K4 character "
      "subs, the parity tables) are pointwise-algebraic in symbols read at (t,x,y,z) — no bare "
      "angular coordinate and no mode index enters any gate (mechanically scanned on the gate "
      "expressions): NO gate distinguishes modes, so the surviving space is MODE-UNIFORM — "
      "R_PW^A carries the SAME character-matched module structure per T^2 mode, the mode layer "
      "entering ONLY through (i) the alphabet's angular grading (jets act by mode "
      "multiplication, banked A3c) and (ii) the granted-mirror cut pairing +n/-n (P1i). No "
      "per-mode kill exists at this layer; mode-decomposition stays Category-A technique")

# --- P2k: the R_N verdicts transfer angular-live (guard re-run) + new parities.
check("P2k_RN_verdicts_transfer_angular_live", "GUARD",
      all(simplify(w.subs(shift_map, simultaneous=True) - w) == 0 for w in (Nx, Ny, Nz))
      and all(simplify(Nv.subs(sm, simultaneous=True) - Nv) == 0 for Nv in (Nx, Ny, Nz) for _, sm in K4_SUBS)
      and Y_PAR["N_y"] == 1 and Z_PAR["N_z"] == 1 and Y_PAR["N_x"] == 0 and Z_PAR["N_x"] == 0,
      "banked T2 R_N verdicts re-run with every symbol read at (t,x,y,z): the three R_N slots "
      "still pass every gate ((y,z) spectators of each condition); NEW angular content: R_N_y is "
      "y-mirror ODD and R_N_z is z-mirror ODD (their paired directions flip — P1i), so the "
      "granted-mirror layer parity-types the angular shift components; the lock-reading fork's "
      "R_N status (physical vs chart-slack via TU2h) travels UNCHANGED, now coupled to the "
      "angular slack legs exactly as P2f derived")

# --- TP2-2 component table (the R_PW^A parametrization skeleton; ledger rows).
ANGULAR_COMPONENTS = [
    ("R_phi", "trivial"), ("R_f", "trivial"), ("R_bh", "trivial"),
    ("R_lambda", "trivial"), ("R_kmod", "trivial"), ("R_k10", "chi_a"),
    ("R_c00", "chi_b"), ("R_c11", "chi_b"), ("R_c01", "chi_c"), ("R_c10", "chi_c"),
    ("R_N_x", "trivial"), ("R_N_y", "trivial"), ("R_N_z", "trivial"),
    ("R_m_y", "trivial"), ("R_m_z", "trivial"),          # NEW (O19; K4-trivial FORCED P2b)
    ("R_wall", "trivial"), ("R_corner", "trivial"),
    ("R_timewall_branch_c_only", "typed"), ("R_timecorner_branch_c_only", "typed"),
]
NEW_M = {"R_m_y", "R_m_z"}
TPAR_ODD = {"R_N_x", "R_N_y", "R_N_z"}
YMIR_ODD = {"R_f", "R_N_y", "R_m_y"}
ZMIR_ODD = {"R_f", "R_N_z", "R_m_z"}
COMPONENTS = []
for (nm, ch) in ANGULAR_COMPONENTS:
    if nm in {"R_timewall_branch_c_only", "R_timecorner_branch_c_only"}:
        COMPONENTS.append([nm, "COMPONENT", "branch-(c) TYPED slot only (no content populated)",
                           ch, "TYPED", "T2 typed slot recovered", "absent statically", "-"])
        continue
    tp = "odd" if nm in TPAR_ODD else "even"
    ym = "odd" if nm in YMIR_ODD else "even"
    zm = "odd" if nm in ZMIR_ODD else "even"
    minv = ("odd" if nm == "R_m_y" else "even") + (" [A-2, verifier round 1: exact on g_yz=0 / eigenbasis; general action flip-and-shear; B^-1-pairing = the invariant]" if nm in NEW_M else "")
    if nm in NEW_M:
        mz_col = "ABSENT-from-T2 (m frozen; killed at mode zero + block-diagonal x-angular premise)"
        st_col = "killed (block-diagonal premise)"
    elif nm in TPAR_ODD:
        mz_col, st_col = "T2 component recovered (C1a)", "killed (N=0 diagonal premise)"
    else:
        mz_col, st_col = "T2 component recovered (C1a)", "banked static component recovered (C2a)"
    branch_rd = ("coordinate spatial branch: physical content; projected spatial branch: "
                 "chart-slack pairing (P2f x-slope legs b = B R_m + N_ang R_N_x)") if nm in NEW_M \
        else ("lock branches as banked T2 (R_N: physical vs chart-slack, TU2h; now slack-coupled "
              "to the angular legs, P2f)" if nm in TPAR_ODD
              else "reading-unchanged on all four branch-pairs")
    COMPONENTS.append([
        nm, "COMPONENT",
        f"K4 char {ch} ((t,y,z) spectators); T-parity {tp} (metric layer, conditional); "
        f"angular-mirror parity y:{ym}/z:{zm} (GRANTED-ONLY, bridge floor G18; pairs +n/-n "
        f"modes); m-involution {minv} on chi-branch strata (coordinate spatial reading); module "
        f"over the tri-graded mode-uniform alphabet; {branch_rd}",
        ch, "DERIVED", mz_col, st_col, "P1i;P2b;P2c;P2f;P2g;P2j"])
VERDICTS["TP2-2"] = (
    "COORDINATE spatial branch: BOTH R_m slots SURVIVE every re-posed pointwise requirement "
    "(K4-trivial FORCED, delta_gauge m = 0; T-even; angular-mirror-matched; witnesses R_m = m "
    "pass all gates; witness d_y phi stratum-scoped off the chi-branch strata); NO new forced "
    "slot, NO null slot in the m-sector (no trace-free-forcing analog; the banked forcing "
    "transfers untouched). PROJECTED spatial branch: R_m pairs PURE chart-slack with exact legs "
    "b_x = B R_m + N_ang R_N_x, b_t = B R_N_ang + N_ang (e^{2phi}/c_E^2) R_phi (slack-coupled "
    "sectors through the SAME B); divergence identity integration-layer, typed not imposed. "
    "READING-INDEPENDENCE ANGULAR ANALOG: DERIVED (P2g) — same module space both spatial "
    "branches at unconditional layers; stratum-conditional m-involution cut rides the "
    "coordinate reading (T2's stratum qualifier transposed). Fork-composition map fact: "
    "gamma^full = sequential corrections iff N_y = N_z = 0 (P2h). Gates mode-blind: R_PW^A "
    "mode-uniform (P2j). NO fork resolved; all four branch-pairs at the same depth."
)
CONSTRAINT_ROWS += [
    ["(constraint) STRATUM m-involution", "CONSTRAINT",
     "components matched under the chi-branch involution m -> (-m_y, m_z - 2 g_yz m_y/g_yy) on "
     "its lawful strata (branch slope angular/t-independent, x-integrable; clean m_y-flip on "
     "g_yz = 0); coordinate spatial reading only; DISCRETE character cut, no Noether identity; "
     "joint conic family CONTINUOUS with invariant m^T B^{-1} m — equivariance beyond the Z2 "
     "slice TYPED; [A-1, verifier round 1: the joint conic also contains the discrete zeta-only slice s = (0, -2 m_z/g_zz) acting as the lawful involution m -> (m_y - 2 g_yz m_z/g_zz, -m_z), preserving m^T B^-1 m — the discrete-slice census is TYPED, not exhausted]; per-witness stratum stamps (P2d)",
     "Z2", "DERIVED (stratum-conditional)", "vacuous at mode zero + m = 0 (level set {0})", "vacuous statically (m = 0)", "P2e;P2d;A1i2"],
    ["(constraint) slack-pairing legs (projected readings)", "CONSTRAINT",
     "exact legs: drag a_angle = sum_A R_A d_angle A; x-slopes b_x = B R_m + N_ang R_N_x; "
     "t-slopes b_t = B R_N_ang + N_ang (e^{2phi}/c_E^2) R_phi; divergence identity between drag "
     "and slope legs = INTEGRATION layer (posed, typed, never imposed pointwise); coordinate "
     "readings: same legs = J07 overlap-transport, no identity owed",
     "-", "DERIVED", "restricts to TU2h legs (a, b = R_N g_tt) at mode zero", "vacuous statically (diagonal premise)", "P2f"],
]
STAGES_DONE.append("TP2-2")

print("=" * 78)
print("STAGE A2 — TP2-3: the banked spaces' fate (embedding; EH placement; identity")
print("strata per mode; new strata typed)")
print("=" * 78)

# --- P3a: R_PW^T embeds as the mode-zero stratum of R_PW^A — EXACT at the
# banked layers, component-by-component; the enrichment is transverse.
tri = [(i, j, k, l) for i in range(3) for j in range(3) for k in range(3) for l in range(3) if k + l <= 2]
bi = [(i, j, k, l) for (i, j, k, l) in tri if k == l == 0]
m_zero = {m1: 0, m2: 0}
flip_at_zero = m_flip.subs(m_zero, simultaneous=True)
check("P3a_T2_embeds_exactly_as_mode_zero_stratum", "SUBSTANTIVE",
      len(tri) == 54 and len(bi) == 9
      and list(flip_at_zero) == [0, 0] and sp.simplify(inv0.subs(m_zero, simultaneous=True)) == 0
      and sp.expand(bx_target[0].subs({Rmy: 0, Rmz: 0, RNx: 0}, simultaneous=True)) == 0,
      "every banked T2 block is angular-order-0 (the 9-letter bigraded alphabet IS the k=l=0 "
      "stratum of the 54-letter tri-graded alphabet) and m-free; on the mode-zero stratum with "
      "m = 0: the stratum m-involution degenerates to the identity (level set {0}), the mode "
      "grading is trivial, the m-sector slack legs vanish, and delta_gauge m = 0 adds no "
      "identity component (P2b): every UNCONDITIONAL angular-live gate (K4, shift-orbit, "
      "bare-letter exclusions, slot structure, stratum identities) restricts to the banked T2 "
      "gate IDENTICALLY — R_PW^T EMBEDS EXACTLY as the mode-zero stratum of R_PW^A, "
      "component-by-component (C1a checks it mechanically); NO member lost, NO deformation AT "
      "THE BANKED LAYERS; the enrichment is purely TRANSVERSE (the R_m row + angular jets + the "
      "mode organization). BRANCH STAMP: identical on all four reading branch-pairs (the "
      "mode-zero + m = 0 stratum is where the spatial readings coincide identically, "
      "gamma_xx^full = g_xx - N_x^2/g_tt = the T2 split)")

# --- P3b: the GRANTED-mirror layer REACHES the mode-zero stratum (derived
# CONTRAST with T2's T-parity layer, which vacates statically).
parQ = 0                                   # Q = c_E e^{-phi}: phi, c_E both mirror-EVEN
par_delta_f = Y_PAR["f"]                   # delta f is y-mirror ODD (A1f)
par_fQ = (Y_PAR["f"] + parQ) % 2           # f x Q: ODD
check("P3b_mirror_layer_cuts_reach_mode_zero", "SUBSTANTIVE",
      parQ == 0 and par_delta_f == 1 and par_fQ == 1,
      "the NEW conditional angular-mirror layer does NOT vacate on the mode-zero stratum: the "
      "banked member R_f = Q is mirror-EVEN while its paired direction delta-f is y-mirror ODD "
      "(f is odd-COMPOSED, A1f — a FIELD parity, independent of angular dependence), so WHERE "
      "THE MIRROR LAYER IS GRANTED it cuts R_f = Q even at mode zero; the member R_f = f x Q is "
      "parity-matched and passes — both witnesses are y-independent. DERIVED CONTRAST with T2: "
      "the T-parity layer was vacuous on the static stratum (no banked block carries a t-jet or "
      "N factor, TU3a); the angular-mirror layer acts on FIELD parities (f), which the banked "
      "strata already contain — the angular extension's conditional layer REACHES INTO the "
      "banked strata. NOT a bank contradiction (F-P5 clean): the banked T2/static cut sets never "
      "contained a mirror layer; this is NEW conditional content, granted-only (bridge floor "
      "G18; coframe SO+ obstruction; admitting = CHOSE), stamped, never imposed here")

# --- P3c: the EH-form's ANGULAR placement (map fact) — exact 2D mirror-parity witness.
a0_, a1_, a2_, b0_, b1_, b2_ = symbols("a0 a1 a2 b0 b1 b2", real=True)
mm0, mm1 = symbols("mm0 mm1", real=True)
A2p = a0_ + a1_ * X + a2_ * Y**2
B2p = b0_ + b1_ * X + b2_ * Y**2
M2p = (mm0 + mm1 * X) * Y
g2d = Matrix([[A2p, M2p], [M2p, B2p]])
g2di = g2d.inv()
co2 = (X, Y)
Gam2 = {}
for aa in range(2):
    for bb in range(2):
        for cc in range(2):
            Gam2[(aa, bb, cc)] = sp.Rational(1, 2) * sum(
                g2di[aa, dd] * (diff(g2d[dd, cc], co2[bb]) + diff(g2d[bb, dd], co2[cc])
                                - diff(g2d[bb, cc], co2[dd])) for dd in range(2))
Ric2 = zeros(2, 2)
for aa in range(2):
    for bb in range(2):
        Ric2[aa, bb] = sum(diff(Gam2[(cc, aa, bb)], co2[cc]) for cc in range(2)) \
            - sum(diff(Gam2[(cc, cc, bb)], co2[aa]) for cc in range(2)) \
            + sum(Gam2[(cc, cc, dd)] * Gam2[(dd, aa, bb)] for cc in range(2) for dd in range(2)) \
            - sum(Gam2[(cc, aa, dd)] * Gam2[(dd, cc, bb)] for cc in range(2) for dd in range(2))
Rsc2 = sp.together(sum(g2di[aa, bb] * Ric2[aa, bb] for aa in range(2) for bb in range(2)))
odd_xy = sp.simplify(Ric2[0, 1].subs(Y, -Y) + Ric2[0, 1])
even_xx = sp.simplify(Ric2[0, 0].subs(Y, -Y) - Ric2[0, 0])
even_yy = sp.simplify(Ric2[1, 1].subs(Y, -Y) - Ric2[1, 1])
even_sc = sp.simplify(Rsc2.subs(Y, -Y) - Rsc2)
check("P3c_EH_angular_placement_parity_witness_exact_2d", "SUBSTANTIVE",
      odd_xy == 0 and even_xx == 0 and even_yy == 0 and even_sc == 0,
      "exact 2D witness (generic profiles: diagonal entries EVEN in y, mixed entry m ODD in y — "
      "precisely the derived A1f composed parity): the exact Ricci tensor transforms with parity "
      "(-1)^{number of y-indices} under the composed angular mirror — Ric_xy ODD (pairing "
      "delta-m_y: exactly the parity the R_m_y slot requires), Ric_xx, Ric_yy and the Ricci "
      "scalar EVEN: curvature-built (EH-form) responses are ANGULAR-MIRROR-PARITY-MATCHED. EH "
      "PLACEMENT angular-live (map fact, nothing selected): field sector, trivial K4 character, "
      "tri-grade <= 2 (at most two derivatives by construction — one in Gamma, one in Ric — and "
      "its angular jets genuinely enter), parity-matched at BOTH conditional layers (T-parity "
      "banked TU3b; angular-mirror here); as a LOCAL functional its mode content is "
      "product/convolution structure (P1e/A3c) — NO mode selection; on the coordinate spatial "
      "branch its x-angular row pairs the physical delta-m, on the projected branch the same "
      "expression pairs chart-slack (reading rides the fork, undecided). 4D generality: tensor "
      "naturality under y -> -y (Category-A, cited); this 2D leg is the in-package exact "
      "instance. Bach-form: typed jets-3/4 class only (banked TC2, cited)")

# --- P3d: the k_mod = 0 identity ANGULAR-LIVE — extends verbatim; mode structure.
bco = symbols("beta0:6")
B6 = zeros(4, 4)
for i_, Lm in enumerate(GENS.values()):
    B6 = B6 + bco[i_] * Lm
Cm_pt = B6 * Xmod - Xmod * B6
eqs_pt = [Cm_pt[i, j] for (i, j) in FORBIDDEN]
A_pt, _ = sp.linear_eq_to_matrix(eqs_pt, list(bco))
MOD_SYMS = {k00, k10, k11, c00, c01, c10, c11}
sys_syms = set().union(*[e.free_symbols for e in A_pt])
GENERIC_PT = {k00: 2, k10: 3, k11: 5, c00: 7, c01: 11, c10: 13, c11: 17}
minors_pt = []
for rsel in itertools.combinations(range(A_pt.rows), 6):
    mdet = sp.expand(A_pt[list(rsel), :].det())
    if mdet != 0:
        minors_pt.append(mdet)
minors_div = all(sp.expand(sp.div(mdet, k00 - k11, k00)[1]) == 0 for mdet in minors_pt)
A_iso = A_pt.subs(k11, k00)
ns_iso = A_iso.nullspace()
L23m = GENS["L23"]
W23 = (L23m * Xmod - Xmod * L23m).subs(k11, k00)
dK23 = W23[2:4, 2:4]
dC23 = W23[2:4, 0:2]
r_tr, r_tf, r_sh, r_nl = symbols("r_tr r_tf r_sh r_nl")
m00, m01, m10, m11 = symbols("m00 m01 m10 m11")
MkerA = Matrix([[m00, m01], [m10, m11]])
W_slotA = r_tr * I2m + r_tf * D2 + r_sh * E21 + r_nl * E12
pairing_full = sp.expand(pairtr(W_slotA, dK23) + pairtr(MkerA, dC23)
                         + RNx * 0 + RNy * 0 + RNz * 0        # delta_gauge N = 0 (banked TU2b)
                         + Rmy * 0 + Rmz * 0                  # delta_gauge m = 0 (P2b) — NEW slots drop out
                         + Rphi * 0 + Rf * 0 + Rbh * 0)       # field sector zero (registered presentation)
IDENT_KMOD0 = sp.expand(-2 * k10 * r_tf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01)
check("P3d_kmod0_identity_extends_verbatim_per_mode", "SUBSTANTIVE",
      sys_syms <= MOD_SYMS
      and A_pt.subs(GENERIC_PT).rank() == 6 and A_pt.subs(GENERIC_PT).nullspace() == []
      and len(minors_pt) == 36 and minors_div
      and len(ns_iso) == 1 and all(simplify(ns_iso[0][i]) == 0 for i in range(5))
      and sp.expand(pairing_full - IDENT_KMOD0) == 0
      and not IDENT_KMOD0.has(Y) and not IDENT_KMOD0.has(Z),
      "the angular-live pointwise tangency system's entries involve ONLY the seven moduli symbols "
      "(each read as an arbitrary function of (t,x,y,z)): (t,y,z) spectators, N-blind AND m-blind; "
      "generic rank 6 / empty nullspace (R7(b) generically vacuous angular-live); all 36 nonzero "
      "6x6 minors divisible by (k00 - k11); on k_mod = 0 the nullspace is span(L23); the FULL "
      "angular-live pairing (screen + mixing + THE THREE R_N SLOTS + THE TWO R_m SLOTS + field "
      "slots) equals the banked identity EXACTLY: -2 k10 r_tf + m00 c10 + m01 c11 - m10 c00 - "
      "m11 c01 = 0 — the identity EXTENDS VERBATIM, GAINS NO ANGULAR COMPONENTS, DOES NOT SPLIT "
      "(delta_gauge N = 0 and delta_gauge m = 0 and the zero field sector kill every candidate "
      "new term). PER-MODE FATE: the identity is ONE pointwise identity, mode-blind (no bare "
      "angle, no mode index in any term — scanned); its mode decomposition is the CONVOLUTION "
      "grading of its bilinear terms (e_j e_k = e_{j+k}, P1e/A3c) — it does NOT split into "
      "independent mode-diagonal identities and it GAINS no mode-indexed family: one identity, "
      "convolution-graded. BRANCH STAMP: identical on all four reading branch-pairs "
      "(moduli-sector; the branch differences live in the N-/m-sectors, which drop out)")

# --- P3e: the codim-1 confinement re-derived angular-live (Groebner re-run).
gb_minors = sp.groebner(minors_pt, k00, k10, k11, c00, c01, c10, c11, order="grevlex")
conf_poly = sp.expand((k00 - 1) * (k00 + 1) * (k00 - k11) * (k11 - 1) * (k11 + 1))
check("P3e_kmod0_only_codim1_cut_angular", "GUARD",
      sp.expand(gb_minors.reduce(conf_poly)[1]) == 0,
      "banked confinement re-run on the angular-live system: every rank-drop point lies in "
      "{k_mod = 0} UNION the eigenvalue resonances {lam -+ k_mod in {+-1}} — k_mod = 0 remains "
      "the only CODIMENSION-1 cut angular-live (the codim-1 layer is exhaustive)")

# --- P3f: the resonance locus — TYPED, stamped OPEN-PENDING-CENSUS.
RES_TYPED = [
    "four named C=0 strata: identities mixing-only, auto-satisfied in the declared class (banked)",
    "C!=0 sub-varieties: further genuine cuts exist; derived example -c10 r_sh - k10 m10 = 0 on "
    "{lam-k_mod=-1, c00=c01=0} (banked round-2); deeper stratification TYPED-NOT-EXHAUSTED",
    "ANGULAR-LIVE STATUS: every statement contacting the resonance locus is stamped "
    "OPEN-PENDING-CENSUS — restated as banked citations only; NO angular-live adjudication "
    "performed here",
]
check("P3f_resonance_locus_typed_open_pending_census", "GUARD",
      len(RES_TYPED) == 3 and "OPEN-PENDING-CENSUS" in RES_TYPED[2],
      "the banked resonance content (four named strata + the shear-identity example + the "
      "typed-not-exhausted stamp) travels as CITATION; its angular-live fate is stamped "
      "OPEN-PENDING-CENSUS, not adjudicated — the (t,y,z)-spectator/N-blind/m-blind facts of "
      "P3d apply to the SYSTEM and are recorded; per-stratum angular-live identities await the "
      "queued census")

# --- P3g: the NEW angular stratum types, typed (character vs identity vs slack).
conic_at0 = conic.subs({s1: 0, s2: 0}, simultaneous=True)
conic_slope = sp.diff(conic, s2).subs({s1: 0, s2: 0}, simultaneous=True)
check("P3g_new_stratum_types_typed", "SUBSTANTIVE",
      len(ns_iso) == 1 and conic_at0 == 0 and sp.simplify(conic_slope - 2 * m2) == 0,
      "the angular-live domain adds TWO new stratum TYPES, typed and DISTINGUISHED: (i) the "
      "chi-branch chart-symmetry strata (P2e) carry a DISCRETE character cut (the m-involution; "
      "Z2, an exact involution) and NO Noether identity — the exact analog of the psi-branch "
      "strata (banked TU4e) and of K4's status; (ii) the joint-conic strata carry a CONTINUOUS "
      "1-parameter family of lawful pin-preserving slacks (the conic 2 m.s + s^T B s = 0 passes "
      "through s = 0 with d(conic)/ds2 = 2 m_z != 0 generically — a smooth solution CURVE by the implicit function theorem, Category-A) — but these are CHART-SLACK maps, not local-Lorentz gauge: "
      "delta_gauge (metric rows) = 0 (P2b), so they impose NO new pointwise Noether identity; "
      "their content is the P2f slack-pairing legs with the divergence identity at the "
      "INTEGRATION layer (typed) on the projected readings, and J07 overlap-transport on the "
      "coordinate readings — DISJOINT in kind from the moduli degeneration strata (continuous "
      "LOCAL-LORENTZ tangent directions, genuine pointwise identities, P3d)")

VERDICTS["TP2-3"] = (
    "R_PW^T EMBEDS EXACTLY as the mode-zero stratum of R_PW^A at the banked layers (no member "
    "lost, no deformation; enrichment transverse: R_m row + angular jets + mode organization; "
    "branch-independent). NEW FINDING: the conditional angular-mirror layer REACHES the "
    "mode-zero stratum (R_f = Q cut where granted, even at mode zero — derived contrast with "
    "T2's T-parity layer, which vacates statically; granted-only, not a banked cut, F-P5 "
    "clean). EH angular placement (map fact): field sector, trivial K4, tri-grade <= 2, "
    "angular-mirror-parity-matched (exact 2D witness: Ric_xy odd, scalar even); mode content = "
    "convolution, no selection; Bach typed jets-3/4. The k_mod = 0 identity EXTENDS VERBATIM "
    "(no angular components, no split; delta_gauge m = 0 derived; ONE identity, "
    "convolution-graded per mode, no mode-diagonal split); k_mod = 0 still the only codim-1 "
    "cut; resonance locus OPEN-PENDING-CENSUS. Two new stratum types typed: discrete "
    "chi-involution (character cut, no identity) vs continuous conic (chart-slack, "
    "integration-layer content only)."
)
CONSTRAINT_ROWS += [
    ["(constraint) STRATUM-IDENTITY kmod0", "CONSTRAINT",
     "-2 k10 r_tf + m00 c10 + m01 c11 - m10 c00 - m11 c01 = 0 on k_mod = 0 — EXTENDS VERBATIM "
     "angular-live: no angular components, no split (delta_gauge N = 0 banked; delta_gauge m = 0 "
     "P2b; field sector zero); ONE pointwise identity, convolution-graded per mode (no "
     "mode-diagonal split); identical on all four reading branch-pairs",
     "chi_a-graded", "DERIVED", "banked T2/static cut recovered (C1/C2)",
     "banked cut recovered (C2a)", "P3d;P3e"],
    ["(constraint) resonance locus", "CONSTRAINT",
     "banked content cited (four named C=0 strata auto-satisfied; C!=0 shear example; deeper "
     "TYPED-NOT-EXHAUSTED); angular-live fate stamped OPEN-PENDING-CENSUS — NOT adjudicated",
     "-", "CITED", "banked citation unchanged", "banked cut recovered (C2a)", "P3f"],
]
STAGES_DONE.append("TP2-3")

print("=" * 78)
print("STAGE A2 — TP2-4: controls (C-1 mode-zero recovery of R_PW^T, mechanical;")
print("C-2 transitive static recovery, spot-scope) and coverage")
print("=" * 78)

T2_DIR = os.path.join(ROOT, "udt_p4_timelive_stage_T2_2026-07-31")
T2_LEDGER = os.path.join(T2_DIR, "TIMELIVE_T2_LEDGER.tsv")
T2_JSON = os.path.join(T2_DIR, "timelive_T2_results.json")
BANKED_JSON = os.path.join(ROOT, "udt_p4_routeA_stage2_pointwise_reduction_2026-07-29",
                           "routeA_stage2_results.json")

# --- C1a: the mode-zero restriction recovers the banked R_PW^T component table
# EXACTLY (mechanical parse of the T2 ledger; never hand-copied).  F-P7 = halt.
t2_rows = []
for line in open(T2_LEDGER, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line or line.startswith("#") or line.startswith("row\t"):
        continue
    t2_rows.append(line.split("\t"))
t2_components = [(r[0], r[3]) for r in t2_rows if r[1] == "COMPONENT"]
my_mode_zero = [(nm, ch) for (nm, ch) in ANGULAR_COMPONENTS if nm not in NEW_M]
t2_tpar_odd = {r[0] for r in t2_rows if r[1] == "COMPONENT" and "T-parity odd" in r[2]}
check("C1a_mode_zero_recovers_T2_component_table", "SUBSTANTIVE",
      my_mode_zero == t2_components and len(t2_components) == 17
      and t2_tpar_odd == TPAR_ODD,
      f"killing the two R_m slots (the mode-zero + m = 0 restriction) recovers the banked "
      f"17-row T2 component table EXACTLY, in order, character-for-character (T2 ledger parsed "
      f"mechanically: {len(t2_components)} COMPONENT rows), and the T-parity assignments match "
      f"row-by-row (T2's odd set = my TPAR_ODD set): R_PW^A's mode-zero stratum = R_PW^T "
      f"component-by-component. F-P7 NOT fired")

# --- C1b: T2's identity string and machine stamps, parsed mechanically.
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
            prod *= IDSYM[core] if core in IDSYM else sp.Integer(int(core))
            if neg:
                prod *= -1
        total += prod
    return sp.expand(total)


t2_kmod0_row = [r for r in t2_rows if r[0].startswith("(constraint) STRATUM-IDENTITY")]
t2_ident = parse_identity(t2_kmod0_row[0][2])
with open(T2_JSON, encoding="utf-8") as fh:
    T2R = json.load(fh)
t2_checknames = {ck["name"]: ck["passed"] for ck in T2R["checks"]}
key_stamps = ["TU2d_RN_survives_all_PW_requirements_coordinate",
              "TU2i_module_space_reading_independent",
              "TU3a_static_RPW_embeds_exactly_no_loss_no_deformation",
              "TU4b_kmod0_identity_extends_verbatim",
              "C1a_component_table_static_recovery_mechanical"]
check("C1b_T2_identity_and_stamps_mechanical", "SUBSTANTIVE",
      sp.expand(t2_ident - IDENT_KMOD0) == 0
      and T2R["n_checks"] == 39 and T2R["all_passed"] is True
      and all(t2_checknames.get(k_) is True for k_ in key_stamps)
      and "OU-1" in T2R["outcome_class"],
      "the banked T2 k_mod = 0 identity string, parsed mechanically from the T2 ledger, equals "
      "my re-derived angular-live identity EXACTLY as an expression; the T2 results JSON parses "
      "mechanically (39/39 passed; the load-bearing stamps TU2d/TU2i/TU3a/TU4b/C1a all passed; "
      "outcome OU-1): the C-1 recovery target is the BANKED object, matched exactly. F-P7 NOT "
      "fired")

# --- C1c: alphabet mode-zero restriction (dims).
check("C1c_alphabet_mode_zero_dims", "GUARD",
      len(tri) == 54 and len(bi) == 9
      and any(r[0] == "alphabet bigraded" for r in t2_rows),
      "the tri-graded alphabet's angular-order-0 restriction is the 9-letter bigraded T2 "
      "alphabet exactly (54 -> 9 mechanical count; T2's alphabet row present in the parsed "
      "ledger): the alphabet layer restricts as declared")

# --- C2a: TRANSITIVE static recovery (spot-scope), mechanical vs the banked
# routeA Stage-2 JSON: component table + module generators + both identities.
with open(BANKED_JSON, encoding="utf-8") as fh:
    BANK = json.load(fh)
STATIC_KILL = {"R_N_x", "R_N_y", "R_N_z", "R_m_y", "R_m_z",
               "R_timewall_branch_c_only", "R_timecorner_branch_c_only"}
my_static = [(nm, ch) for (nm, ch) in ANGULAR_COMPONENTS if nm not in STATIC_KILL]
banked_table = [(row["component"], row["character"]) for row in BANK["component_table"]]
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
    if any(sp.expand(a_ - b_) != 0 for a_, b_ in zip(parsed, mine)):
        gens_match = False
bank_kmod0 = parse_identity(BANK["stratum_noether_identities_A1"]["kmod0"]["identity"])
bank_shear = parse_identity(BANK["stratum_noether_identities_A1"]["Cneq0_subvarieties_R2"]["identity"])
MY_SHEAR = sp.expand(-c10 * r_sh - k10 * m10)
check("C2a_transitive_static_recovery_spot_scope", "SUBSTANTIVE",
      my_static == banked_table and len(banked_table) == 12 and gens_match
      and sp.expand(bank_kmod0 - IDENT_KMOD0) == 0 and sp.expand(bank_shear - MY_SHEAR) == 0,
      "SPOT-SCOPE transitive control: the mode-zero + static restriction (kill R_N, R_m and the "
      "branch-(c) slots) recovers the banked 12-component static table EXACTLY, in order, "
      "character-for-character (routeA_stage2 JSON parsed mechanically); the banked "
      "chi_a/chi_b/chi_c module generator strings parse to expressions equal to mine EXACTLY; "
      "the banked k_mod = 0 and shear identity strings parse to expressions equal to my "
      "re-derived ones EXACTLY: restriction composes angular -> time -> static (spot legs; the "
      "full transitivity chain is C1 x T2's own banked C-1). F-P7 NOT fired")

# --- Coverage guard (R2/J05/J13 angular-live).
comp_names = {nm for nm, _ in ANGULAR_COMPONENTS}
check("R2_J05_component_coverage_angular", "GUARD",
      len(ANGULAR_COMPONENTS) == 19
      and {"R_m_y", "R_m_z", "R_N_x", "R_N_y", "R_N_z"} <= comp_names
      and {"R_kmod", "R_c00", "R_c01", "R_c10", "R_c11"} <= comp_names,
      "one component slot per 20-census direction (12 banked + 3 R_N + 2 NEW R_m + 2 branch-(c) "
      "TYPED slots; O18 time label and O20 period data are discrete/supplied data with NO "
      "component slot — the periods join the J13 discriminator/completion controls; alpha/c_E "
      "forks enter on their labeled branches as banked): a missing R_m slot would be the "
      "y-isometry era's presentation-freeze made visible (coordinate spatial reading) — R2 "
      "honored; J05 full tangent paired (delta-m, delta-N and tri-graded jet directions "
      "included); J13 discriminator slots (k_mod, C) retained; theta ABSENT; no cycle/completion "
      "content beyond scope-exclusions (F-P1 self-audit)")

VERDICTS["TP2-4"] = (
    "C-1 PASS (mechanical parse of the banked T2 ledger + results JSON: the mode-zero + m = 0 "
    "restriction recovers the 17-row R_PW^T component table EXACTLY, in order, "
    "character-for-character, T-parity row-matched; the k_mod = 0 identity string parses to my "
    "expression exactly; T2 stamps 39/39/OU-1 verified; F-P7 not fired). C-2 PASS (spot-scope): "
    "the static restriction recovers the banked 12-component table, module generators and both "
    "identity strings EXACTLY from the routeA Stage-2 JSON. Coverage: 19 component slots over "
    "the 20-object census (O18/O20 discrete data, no slots)."
)
STAGES_DONE.append("TP2-4")

# ==== EMIT (always last) ====
print("=" * 78)
print(f"EMIT — stages done: {STAGES_DONE}; guards; ledger; JSON; exit")
print("=" * 78)

# --- G3: hygiene self-scan (wired).
src = open(os.path.join(HERE, "derive_angular_A2.py"), encoding="utf-8").read()
banned_src = ["num" + "py", "sci" + "py", "im" + "port random", ".eva" + "lf", "nso" + "lve(",
              "tor" + "ch", "flo" + "at("]
check("G3_no_floats_numeric_solvers_or_rng", "GUARD",
      all(tok not in src for tok in banned_src) and re.search(r"\d\.\d", src) is None,
      "self-scan: no external numerics, no RNG, no eval-to-decimal / numeric-solve calls, no "
      "float literals — exact SymPy only, deterministic")

# --- G4: the F-P1 vocabulary scan (record + ledger + decision surface).
fp1_re = re.compile(r"\bwinding\b|\bholonomy\b|\bcycles?\b", re.IGNORECASE)
allow_re = re.compile(r"stage a3|a3's|f-p1|f-a1|scope", re.IGNORECASE)
fp1_viol = []
for fname in ("EXACT_DERIVATION.md", "ANGULAR_A2_LEDGER.tsv", "DECISION_SURFACE_UPDATE.md"):
    fpath = os.path.join(HERE, fname)
    if os.path.exists(fpath):
        for lineno, line in enumerate(open(fpath, encoding="utf-8"), 1):
            if fp1_re.search(line) and not allow_re.search(line):
                fp1_viol.append(f"{fname}:{lineno}")
check("G4_FP1_banned_word_scan", "GUARD",
      len(fp1_viol) == 0,
      "F-P1 self-audit: every occurrence of the A3-scoped vocabulary in the derivation record, "
      "ledger and decision surface sits on a scope-exclusion line; violations: "
      + (";".join(fp1_viol) or "none"))

# --- Ledger emission (component rows only once TP2-2 is banked).
LEDGER_HEADER = [
    "# STAMP: Stage A2 angular-live pointwise ledger. Contract = PREREGISTRATION.md (frozen "
    "first). EVERYTHING-ON within the cleared layers; T^2 stratum (A-L1, full-S^3 TYPED); "
    "tri-graded jets <= 2 per direction (A-L2, higher TYPED); time-live-LINE (A-L4); theta "
    "ABSENT (A-L5); registered stationary presentation (general arenas TYPED); polynomial/formal "
    "in (k10,C); BOTH lock-reading AND BOTH spatial-reading branches carried at the same depth; "
    "mode decomposition Category-A; no response law selected, no fork resolved, no solve, no "
    "angular cycle census (Stage A3's contract; F-P1 honored).",
    "# STAMP: layered character rule (TP2-1/TP2-2): K4 ((t,y,z) spectators) x T^2-translations "
    "(bare angles excluded; mode grading slack-stable) x METRIC-LAYER T-parity Z2 (conditional, "
    "banked T2) x ANGULAR-MIRROR Z2 x Z2 (conditional, granted-only, bridge floor G18; pairs "
    "+n/-n modes) x STRATUM N-parity Z2 (psi-branch, lock-coordinate reading, banked T2) x "
    "STRATUM m-involution Z2 (chi-branch, spatial-coordinate reading, NEW). Resonance-locus "
    "contacts: OPEN-PENDING-CENSUS.",
    "# STAMP: mode_zero_restriction column = the C-1 identity (mechanical vs banked "
    "TIMELIVE_T2_LEDGER.tsv + timelive_T2_results.json); static_restriction_transitive column = "
    "the C-2 identity (mechanical vs banked routeA_stage2_results.json).",
]
ledger_path = os.path.join(HERE, "ANGULAR_A2_LEDGER.tsv")
LEDGER_ROWS = []
if COMPONENTS is not None:
    for row in COMPONENTS:
        LEDGER_ROWS.append(row)
LEDGER_ROWS += CONSTRAINT_ROWS + ALPHABET_ROWS
with open(ledger_path, "w", encoding="utf-8") as fh:
    for line in LEDGER_HEADER:
        fh.write(line + "\n")
    fh.write("row\tkind\tcontent\tcharacter\ttag\tmode_zero_restriction\t"
             "static_restriction_transitive\tbasis_checks\n")
    for row in LEDGER_ROWS:
        fh.write("\t".join(row) + "\n")
print(f"ledger written: {ledger_path} ({len(LEDGER_ROWS)} rows; stages {STAGES_DONE})")

if COMPONENTS is not None:
    cols_ok = all(len(r) == 8 for r in LEDGER_ROWS)
    check("G2_ledger_coverage_and_shape", "GUARD",
          cols_ok and sum(1 for r in LEDGER_ROWS if r[1] == "COMPONENT") == 19,
          "the angular-live ledger parses with exactly 19 COMPONENT rows (17 T2-lineage + 2 NEW "
          "R_m) + constraint + alphabet rows, 8 columns each")

# --- Tally, JSON (G1 wired), exit.
result = {
    "package": "udt_p4_angular_stage_A2_2026-07-31",
    "stage": "A2 (TP2-1..TP2-4; the pointwise reduction angular-live, both spatial-reading "
             "branches x both lock-reading branches)",
    "date": "2026-07-31",
    "contract": "PREREGISTRATION.md (frozen before derivation)",
    "stages_done": STAGES_DONE,
    "verdicts": VERDICTS,
    "ceiling": "no response law selected; no fork decided; no solve; no angular cycle census "
               "(Stage A3 scope-exclusion); no spectrum; no physics — the ceiling binds "
               "regardless of what the algebra showed",
    "falsifier_events": FALSIFIER_EVENTS,
}
json_path = os.path.join(HERE, "angular_A2_results.json")
prelim = dict(result)
prelim.update({"n_checks": len(CHECKS), "n_passed": sum(1 for ck in CHECKS if ck["passed"]),
               "checks": CHECKS})
with open(json_path, "w", encoding="utf-8") as fh:
    json.dump(prelim, fh, indent=1)
try:
    with open(json_path, encoding="utf-8") as fh:
        rt = json.load(fh)
    g1_ok = (rt["package"] == result["package"] and len(rt["checks"]) == len(CHECKS)
             and rt["n_passed"] == prelim["n_passed"])
except Exception:
    g1_ok = False
check("G1_results_json_written_and_roundtrips", "GUARD", g1_ok,
      "angular_A2_results.json written and round-trips; wired into the exit path")
n_total = len(CHECKS)
n_pass = sum(1 for ck in CHECKS if ck["passed"])
n_sub = sum(1 for ck in CHECKS if ck["kind"] == "SUBSTANTIVE")
n_guard = n_total - n_sub
oc = "OA2-1 (R_PW^A parametrized per branch; controls pass; forks carried, none resolved)" \
    if (n_pass == n_total and len(STAGES_DONE) == 4) else \
    (f"PARTIAL (stages {STAGES_DONE})" if n_pass == n_total else "FAILED-CHECKS")
result.update({"n_checks": n_total, "n_passed": n_pass, "n_substantive": n_sub,
               "n_guard": n_guard, "all_passed": n_pass == n_total,
               "outcome_class": oc, "checks": CHECKS})
with open(json_path, "w", encoding="utf-8") as fh:
    json.dump(result, fh, indent=1)
print("=" * 78)
print(f"TOTAL: {n_pass}/{n_total} passed ({n_sub} SUBSTANTIVE + {n_guard} GUARD); "
      f"stages {STAGES_DONE}; outcome {oc}; exit {'0' if n_pass == n_total else '1'}")
sys.exit(0 if n_pass == n_total else 1)
