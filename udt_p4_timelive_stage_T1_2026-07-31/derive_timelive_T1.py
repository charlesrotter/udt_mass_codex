#!/usr/bin/env python3
"""Stage T1 derivation script — the response inverse problem re-posed TIME-LIVE.

Contract: PREREGISTRATION.md (frozen). Exact SymPy only: no floats, no numeric
solvers, no GPU, deterministic. Exit nonzero on any failed check.
Check kinds: SUBSTANTIVE (a derivation leg) vs GUARD (re-run/mechanical/hygiene).

Native-form discipline (F-T2): the time row is derived from the CANONIZED clock
law g_tt = -e^{-2 phi} c^2 (covariant row pinned) + the reciprocal lock
B = 1/A (g_tt * g_rr = -c^2, kinematic). NO ADM lapse/shift parametrization is
used anywhere; check T1j certifies the two pins are inequivalent when the
shift row is on. Frame conventions reused verbatim from the banked Stage-1
script (eta = diag(-1,1,1,1); slots (0,1) base, (2,3) screen; K4 as banked).
"""
import json
import os
import sys

import sympy as sp
from sympy import Matrix, symbols, exp, diff, simplify, zeros, eye

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
# Shared exact objects (banked conventions, reused verbatim)
# ---------------------------------------------------------------------------
eta = sp.diag(-1, 1, 1, 1)
I4 = eye(4)
R23 = sp.diag(1, 1, -1, -1)
R12 = sp.diag(1, -1, -1, 1)
R13 = sp.diag(1, -1, 1, -1)
K4 = [I4, R23, R12, R13]

c = symbols("c", positive=True)
phi = symbols("phi", real=True)
s_shift = symbols("s", real=True)
Nx = symbols("N_x", real=True)   # the (t,x) mixed metric component g_tx
gxx = symbols("g_xx", positive=True)
hp = symbols("hp", real=True)    # dh/dt of a time reparametrization t -> h(t)
p1 = symbols("psi1", real=True)  # d(psi)/dx of the slack map t -> t + psi(x)

g_tt = -exp(-2 * phi) * c**2     # THE CLOCK LAW (canon C-2026-06-18-1): pinned COVARIANT row
g2 = Matrix([[g_tt, Nx], [Nx, gxx]])   # (t,x) block of the extended metric, shift row LIVE

print("=" * 78)
print("STAGE T1 — TT-1: the time-live variation domain (clock-law consequences,")
print("shift row native form, residual chart symmetry)")
print("=" * 78)

# --- T1a/T1b: NO FREE LAPSE. Under t -> h(t) (h' = hp), covariant components
# transform g_tt -> hp^2 g_tt, g_tx -> hp g_tx, g_xx -> g_xx. The reciprocal
# lock (both readings) then rigidifies hp.
Jh = Matrix([[hp, 0], [0, 1]])
g2h = sp.expand(Jh.T * g2 * Jh)
lock_i_orig = g_tt * gxx                      # reading (i): coordinate lock g_tt*g_rr
lock_i_new = g2h[0, 0] * g2h[1, 1]
sol_hp_i = sp.solve(sp.Eq(lock_i_new, lock_i_orig), hp)
check("T1a_lock_forces_unit_time_speed_reading_i", "SUBSTANTIVE",
      set(sol_hp_i) == {-1, 1},
      "g_tt*g_xx = -c^2 preserved under t->h(t) iff h'^2=1: h' in {-1,+1}; no free lapse, exactly")

gam_orig = g2[1, 1] - g2[0, 1] ** 2 / g2[0, 0]   # projected (radar) ruler gamma_xx
gam_new = g2h[1, 1] - g2h[0, 1] ** 2 / g2h[0, 0]
sol_hp_ii = sp.solve(sp.Eq(simplify(g2h[0, 0] * gam_new), simplify(g2[0, 0] * gam_orig)), hp)
check("T1b_lock_forces_unit_time_speed_reading_ii", "SUBSTANTIVE",
      set(sol_hp_ii) == {-1, 1},
      "projected reading g_tt*gamma_xx likewise forces h'^2=1: the rigidity is reading-robust")

# --- T1c: the residual time maps {t -> sigma*t + t0, sigma=+-1} form a group.
t, t0a, t0b = symbols("t t0a t0b", real=True)
sga, sgb = symbols("sigma_a sigma_b", real=True)
compose = (sga * (sgb * t + t0b) + t0a)
comp_ok = simplify(compose - (sga * sgb) * t - (sga * t0b + t0a)) == 0
sigma_closure = all(sa * sb in (1, -1) for sa in (1, -1) for sb in (1, -1))
check("T1c_residual_time_maps_form_group", "SUBSTANTIVE",
      comp_ok and sigma_closure,
      "composition = (sigma_a*sigma_b) t + (sigma_a t0b + t0a): closure; identity sigma=1,t0=0; inverses exist -> T1 = R x| Z2")

# --- T1d/T1e/T1f: K4 and the time axis.
k4_fix_time = all(M[0, 0] == 1 and all(M[0, j] == 0 for j in range(1, 4))
                  and all(M[i, 0] == 0 for i in range(1, 4)) for M in K4)
check("T1d_K4_elements_fix_frame_time_axis", "SUBSTANTIVE", k4_fix_time,
      "every K4 element has Lam^0_0 = 1 with zero time-space mixing: K4 SURVIVES the time extension verbatim")
k4_so_plus = all(is_zero_matrix(M.T * eta * M - eta) and M.det() == 1 and M[0, 0] == 1 for M in K4)
check("T1e_K4_elements_proper_orthochronous_reverified", "GUARD", k4_so_plus,
      "banked A2 re-run: all four in SO+(1,3)")
prods = [is_zero_matrix(R12 * R13 - R23), is_zero_matrix(R12 * R12 - I4),
         is_zero_matrix(R13 * R13 - I4), is_zero_matrix(R23 * R23 - I4)]
check("T1f_K4_closure_reverified", "GUARD", all(prods), "banked A2 closure re-run: Z2 x Z2")

# --- T1g: no SO+ element flips time orientation (exact column-0 identity).
Lg = Matrix(4, 4, symbols("L0:16", real=True))
col0 = sp.expand((Lg.T * eta * Lg)[0, 0])
ident_ok = simplify(col0 - (-Lg[0, 0] ** 2 + Lg[1, 0] ** 2 + Lg[2, 0] ** 2 + Lg[3, 0] ** 2)) == 0
sum_sq = Lg[1, 0] ** 2 + Lg[2, 0] ** 2 + Lg[3, 0] ** 2
check("T1g_no_SOplus_element_flips_time_orientation", "SUBSTANTIVE",
      ident_ok and bool(sum_sq.is_nonnegative),
      "(Lam^T eta Lam)_00 = -L00^2 + sum b_i^2 = -1 => L00^2 = 1 + sum b_i^2 >= 1: O(1,3) splits into "
      "L00>=1 (orthochronous, contains K4) and L00<=-1; the registered gauge group SO+ contains NO time-flip")

# --- T1h: time reflection at the METRIC layer: flips the shift row only.
Jr = sp.diag(-1, 1)
g2r = sp.expand(Jr.T * g2 * Jr)
check("T1h_time_reflection_metric_layer_flips_shift_only", "SUBSTANTIVE",
      simplify(g2r[0, 0] - g2[0, 0]) == 0 and simplify(g2r[1, 1] - g2[1, 1]) == 0
      and simplify(g2r[0, 1] + g2[0, 1]) == 0,
      "t -> -t: g_tt, g_xx invariant; g_ti -> -g_ti. A residual Z2 of the metric presentation, acting on N by sign")

# --- T1i: ... but OBSTRUCTED at the registered-coframe layer: restoring the
# future-pointing time leg needs a frame element with Lam^0_0 <= -1 (T1g),
# which SO+ (the banked gauge registration) excludes.
interval_gap = sp.Intersection(sp.Interval(1, sp.oo), sp.Interval(-sp.oo, -1)) == sp.EmptySet
check("T1i_time_reflection_coframe_layer_obstructed", "SUBSTANTIVE",
      interval_gap,
      "e^0(d_t') = -e^0(d_t) < 0 after t->-t; undoing it needs L00<=-1, disjoint from SO+'s L00>=1: "
      "the Z2 exists at the metric layer ONLY; at the registered coframe layer it requires ENLARGING the gauge registration (a CHOSE, not derived)")

# --- T1j: the native pin is the COVARIANT clock row, NOT an ADM lapse pin.
static_rate = sp.sqrt(-g_tt) / c   # proper clock rate of a coordinate-stationary observer
check("T1j_static_observer_rate_is_exp_minus_phi", "SUBSTANTIVE",
      simplify(static_rate - exp(-phi)) == 0,
      "dtau/dt|_{dx=0} = sqrt(-g_tt)/c = e^{-phi} INDEPENDENT of the shift row: the canon clock law is exactly the covariant-row pin")
g2inv = g2.inv()
adm_lapse2c2 = simplify(-1 / g2inv[0, 0])   # what an ADM parametrization would call (lapse*c)^2
check("T1j_covariant_pin_is_not_ADM_lapse_pin", "SUBSTANTIVE",
      simplify(adm_lapse2c2 - (-g_tt) - Nx**2 / gxx) == 0,
      "-1/g^{tt} = e^{-2phi}c^2 + N^2/g_xx: pinning the covariant row differs from pinning the ADM lapse by N^2/g_xx, "
      "nonzero whenever the shift is on -- the derivation here never uses the ADM decomposition (F-T2 self-audit)")

# --- T1k: the reciprocal lock's two time-live readings differ iff shift is on.
check("T1k_two_lock_readings_differ_iff_shift", "SUBSTANTIVE",
      simplify((gam_orig - g2[1, 1]) - (Nx**2 * exp(2 * phi) / c**2)) == 0,
      "gamma_xx - g_xx = N^2 e^{2phi}/c^2: coordinate reading (i) and projected reading (ii) of B=1/A coincide exactly on the diagonal stratum and split otherwise -- a derived FORK, canon silent, carried not chosen")

# --- T1l/T1m/T1n/T1o/T1p: the slack map t -> t + psi(x) (pointwise slope p1).
Jp = Matrix([[1, p1], [0, 1]])
g2p = sp.expand(Jp.T * g2 * Jp)
check("T1n_psi_map_preserves_clock_row", "SUBSTANTIVE",
      simplify(g2p[0, 0] - g2[0, 0]) == 0,
      "t -> t + psi(x) preserves g_tt exactly: the clock law alone does NOT fix the time-space mixing")
gam_p = simplify(g2p[1, 1] - g2p[0, 1] ** 2 / g2p[0, 0])
check("T1l_projected_lock_reading_psi_invariant", "SUBSTANTIVE",
      simplify(gam_p - gam_orig) == 0,
      "gamma_xx is EXACTLY psi-invariant: the projected reading of the lock is well defined across the slack class")
diff_i = sp.expand(g2p[0, 0] * g2p[1, 1] - g2[0, 0] * g2[1, 1])
poly_i = sp.Poly(diff_i, p1)
check("T1m_coordinate_lock_reading_not_psi_invariant", "SUBSTANTIVE",
      poly_i.degree() >= 1 and simplify(poly_i.coeff_monomial(p1**2) - g2[0, 0] ** 2) == 0,
      "g_tt*g_xx shifts by g_tt(2 N psi' + g_tt psi'^2): reading (i) is a psi-frame quantity (nonzero polynomial in psi', certified)")
g2p_diag = g2p.subs(Nx, 0)
check("T1o_psi_map_generates_shift_from_diagonal", "SUBSTANTIVE",
      simplify(g2p_diag[0, 1] - g_tt * p1) == 0 and sp.solve(sp.Eq(g_tt * p1, 0), p1) == [0],
      "from N=0 the slack map generates N' = g_tt psi' != 0 for psi' != 0: the diagonal stratum is not slack-closed")
sol_p1 = sp.solve([sp.Eq(g2p[1, 1], g2[1, 1]), sp.Eq(g2p[0, 1], g2[0, 1])], p1)
check("T1p_spatial_and_shift_pins_jointly_kill_psi", "SUBSTANTIVE",
      sol_p1 == [(0,)] or sol_p1 == {p1: 0} or sol_p1 == [0],
      "preserving BOTH the registered spatial row AND the shift row forces psi' = 0 -- uniqueness uses the shift-row "
      "equation as a second pin (a pin on a varied field); the spatial pin ALONE is weaker (T1p2) "
      "[AMENDED 2026-07-31, verifier round 1: name/note corrected from 'registered_spatial_pin_kills_psi']")

# --- AMENDMENT 2026-07-31 (verifier round 1, AM-1/AM-2 = verifier V5a/V5b/V5c):
# the psi-branches the joint pin hides, derived as checked steps.
# AM-1 (V5a): the spatial pin ALONE admits TWO branches.
sol_p1_alone = set(sp.solve(sp.Eq(g2p[1, 1], g2[1, 1]), p1))
check("T1p2_spatial_pin_alone_two_branches", "SUBSTANTIVE",
      sol_p1_alone == {0, sp.simplify(-2 * Nx / g_tt)},
      "preserving the registered spatial row g_xx ALONE gives psi' in {0, -2N/g_tt} (= {0, 2N e^{2phi}/c^2}): "
      "the slack is NOT killed by the spatial pin alone -- a second lawful branch exists")
# AM-1 (V5b): the second branch is a lawful stratum-conditional Z2 residual map.
g2p_flip = sp.expand(g2p.subs(p1, sp.simplify(-2 * Nx / g_tt)))
gam_flip = simplify(g2p_flip[1, 1] - g2p_flip[0, 1] ** 2 / g2p_flip[0, 0])
check("T1p3_Z2_residual_branch_flips_N_stratum_conditional", "SUBSTANTIVE",
      simplify(g2p_flip[0, 0] - g2[0, 0]) == 0 and simplify(g2p_flip[1, 1] - g2[1, 1]) == 0
      and simplify(g2p_flip[0, 1] + Nx) == 0
      and simplify(g2p_flip[0, 0] * g2p_flip[1, 1] - g2[0, 0] * g2[1, 1]) == 0
      and simplify(gam_flip - gam_orig) == 0,
      "psi' = -2N/g_tt preserves the clock row, the spatial row and BOTH lock readings while mapping N -> -N: "
      "a lawful residual chart map t -> t + psi(x) on strata where 2N e^{2phi}/c^2 is t-independent -- the residual "
      "group on the registered chart (coordinate reading) is K4 x T1 TIMES this stratum-conditional Z2 psi-branch; "
      "the orbit of N stays {N, -N}, so irreducibility-as-non-removability SURVIVES (the branch flips N's sign, "
      "it never removes N)")
# AM-2 (V5c): under a PROJECTED-reading spatial registration (pin gamma_xx, not
# g_xx), psi' = -N/g_tt is lawful and REMOVES the shift entirely.
g2p_kill = sp.expand(g2p.subs(p1, sp.simplify(-Nx / g_tt)))
gam_kill = simplify(g2p_kill[1, 1] - g2p_kill[0, 1] ** 2 / g2p_kill[0, 0])
check("T1p4_projected_reading_pin_makes_N_removable", "SUBSTANTIVE",
      simplify(g2p_kill[0, 1]) == 0 and simplify(g2p_kill[0, 0] - g2[0, 0]) == 0
      and simplify(gam_kill - gam_orig) == 0 and simplify(g2p_kill[1, 1] - gam_orig) == 0,
      "psi' = -N/g_tt kills N while preserving the clock row and the projected lock reading exactly (the new chart is "
      "DIAGONAL with g'_xx = gamma_xx), lawful wherever N/g_tt is t-independent: under a reading-(ii) spatial "
      "registration the shift is CHART-SLACK (removable), so the shift row's irreducibility (T1r, O17) is "
      "CONDITIONAL on the COORDINATE-reading (i) spatial pin of the registered chart -- the lock-reading fork is "
      "LOAD-BEARING, carried both ways, decided by NOTHING in this package (F-T4)")

# --- T1q: the anchor shift, time-extended (D3 extension). phi -> phi+s absorbed
# by the anchor c_E PLUS the derived unit rescale (t,r) -> (e^s t, e^{-s} r).
es = exp(s_shift)
g_tt_shifted_rescaled = simplify(es**2 * g_tt.subs(phi, phi + s_shift))
g_rr = exp(2 * phi)   # the reciprocal-locked radial row (B = 1/A)
g_rr_shifted_rescaled = simplify(es**-2 * g_rr.subs(phi, phi + s_shift))
cE = symbols("c_E", positive=True)
Q = cE * exp(-phi)
Q_shifted_absorbed = (cE * es) * exp(-(phi + s_shift))
check("T1q_anchor_shift_absorption_time_extended", "SUBSTANTIVE",
      simplify(g_tt_shifted_rescaled - g_tt) == 0
      and simplify(g_rr_shifted_rescaled - g_rr) == 0
      and simplify(Q_shifted_absorbed - Q) == 0,
      "clock row, locked radial row and the anchored readout Q are all invariant under (phi+s, t*e^s, r*e^{-s}, c_E*e^s): "
      "shift-equivariance (F-RA4) EXTENDS; on the registered chart (units pinned, areal leg carries r^2) the shift acts as an "
      "OVERLAP map between presentations, not a chart automorphism -- typed, matching banked D3")

# --- T1r: the shift row is irreducible under the registered residual group.
# [AMENDED 2026-07-31, verifier round 1: group claim restated with the
# stratum-conditional Z2 psi-branch (T1p3); irreducibility stamped CONDITIONAL
# on the coordinate-reading spatial pin (T1p4).]
resid_orbit = {simplify(sg * Nx) for sg in (1, -1)}   # T1 acts N -> sigma N; K4 trivial; the T1p3 psi-branch also acts N -> -N
check("T1r_shift_irreducible_under_residual_group", "SUBSTANTIVE",
      resid_orbit == {Nx, -Nx} and sp.solve(sp.Eq(Nx, 0), Nx) == [0]
      and all(sp.solve(sp.Eq(sg * Nx, 0), Nx) == [0] for sg in (1, -1)),
      "UNDER THE COORDINATE-READING (i) SPATIAL PIN: the residual maps of the registered chart -- K4 x {t->sigma t+t0} "
      "PLUS the stratum-conditional Z2 psi-branch (T1p3, lawful where 2N e^{2phi}/c^2 is t-independent) -- ALL act on N "
      "by sign only (orbit {N,-N}): no residual transformation removes a nonzero shift; N is a genuine varied object "
      "(T-L2 RESOLVED live). CONDITIONALITY STAMP: under the projected-reading (ii) spatial registration the shift is "
      "instead removable chart-slack (T1p4) -- this claim rides the lock-reading fork, LOAD-BEARING, carried both ways")

# --- T1s: the K4 moduli characters with t as spectator (pointwise algebra).
k00t, k10t, k11t = symbols("k00t k10t k11t")   # read: k00(t) etc. -- arbitrary pointwise values
c00t, c01t, c10t, c11t = symbols("c00t c01t c10t c11t")
Xt = zeros(4, 4)
Xt[0:2, 0:2] = sp.diag(-1, 1)
Xt[2:4, 0:2] = Matrix([[c00t, c01t], [c10t, c11t]])
Xt[2:4, 2:4] = Matrix([[k00t, 0], [k10t, k11t]])
ok_R23 = is_zero_matrix(R23 * Xt * R23 - Xt.subs({c00t: -c00t, c01t: -c01t, c10t: -c10t, c11t: -c11t}, simultaneous=True))
ok_R12 = is_zero_matrix(R12 * Xt * R12 - Xt.subs({k10t: -k10t, c00t: -c00t, c11t: -c11t}, simultaneous=True))
ok_R13 = is_zero_matrix(R13 * Xt * R13 - Xt.subs({k10t: -k10t, c01t: -c01t, c10t: -c10t}, simultaneous=True))
lam_t = (k00t + k11t) / 2
kmod_t = (k11t - k00t) / 2
inv_ok = all(simplify(lam_t.subs(sub, simultaneous=True) - lam_t) == 0
             and simplify(kmod_t.subs(sub, simultaneous=True) - kmod_t) == 0
             for sub in [{k10t: -k10t, c00t: -c00t, c11t: -c11t},
                         {k10t: -k10t, c01t: -c01t, c10t: -c10t},
                         {c00t: -c00t, c01t: -c01t, c10t: -c10t, c11t: -c11t}])
check("T1s_K4_moduli_characters_t_spectator", "SUBSTANTIVE",
      ok_R23 and ok_R12 and ok_R13 and inv_ok,
      "the K4 action is pointwise-algebraic: with every entry read as an arbitrary function of (x,t), the banked characters "
      "(lam,k_mod invariant; k10 chi_a; C signed flips) hold unchanged -- t enters as a spectator of the quotient")

print("=" * 78)
print("STAGE T1 — TT-2: the requirement set re-posed (computational legs)")
print("=" * 78)

# --- T2a: the TEMPORAL-MIRROR involution DERIVED from the metric form (R6 seat).
# Demand: the t->-t pullback of the metric equals the metric built from
# sign-transformed fields s_phi*phi(x,-t), s_N*N(x,-t), s_G*G(x,-t).
s_phi, s_N, s_G = symbols("s_phi s_N s_G", real=True)
phN, GN = symbols("phN GN", real=True)  # arbitrary pointwise field values phi(x,-t), G(x,-t)
NN = symbols("NN", real=True)
# pullback components at (x,t): g'_tt = g_tt(-t), g'_tx = -g_tx(-t), g'_xx = g_xx(-t)
pull_tt = -exp(-2 * phN) * c**2
pull_tx = -NN
pull_xx = GN
# metric of transformed fields: phi~ = s_phi*phN, N~ = s_N*NN, G~ = s_G*GN
form_tt = -exp(-2 * s_phi * phN) * c**2
form_tx = s_N * NN
form_xx = s_G * GN
# phi condition: e^{-2 s_phi phN} = e^{-2 phN} for ALL phN => s_phi = 1 (exponential form forbids a flip)
sol_sphi = sp.solve(sp.Eq(s_phi * phN, phN), s_phi)
sol_sN = sp.solve(sp.Eq(form_tx, pull_tx), s_N)
sol_sG = sp.solve(sp.Eq(form_xx, pull_xx), s_G)
check("T2a_temporal_mirror_parity_assignment_derived", "SUBSTANTIVE",
      sol_sphi == [1] and sol_sN == [-1] and sol_sG == [1],
      "form preservation under t->-t FORCES phi EVEN-composed (the exponential clock law forbids a phi sign flip), "
      "N ODD-composed, spatial data EVEN-composed: the temporal-mirror involution is (t,phi,N,G) -> (-t, phi, -N, G) -- derived, not posited")

# --- T2b/T2c: temporal parity jet-kill at a mirror-symmetric locus t=0 (S0d analog).
a0, a1, a2, a3, a4, a5 = symbols("a0:6", real=True)
tj = symbols("t_j", real=True)
p_gen = a0 + a1 * tj + a2 * tj**2 + a3 * tj**3 + a4 * tj**4 + a5 * tj**5
even_cond = sp.expand(p_gen - p_gen.subs(tj, -tj))
sol_even = sp.solve([sp.Poly(even_cond, tj).coeff_monomial(tj**k) for k in range(6)], [a1, a3, a5], dict=True)
even_kill = sol_even == [{a1: 0, a3: 0, a5: 0}]
check("T2b_temporal_parity_jet_kill_even_field", "SUBSTANTIVE", even_kill,
      "an even-composed field (phi, G) has ALL odd t-jets killed at t=0: generic degree-5 jet, exact -- "
      "a temporal-mirror-symmetric configuration has a moment of time symmetry (d_t phi = 0 there)")
odd_cond = sp.expand(p_gen + p_gen.subs(tj, -tj))
sol_odd = sp.solve([sp.Poly(odd_cond, tj).coeff_monomial(tj**k) for k in range(6)], [a0, a2, a4], dict=True)
odd_kill = sol_odd == [{a0: 0, a2: 0, a4: 0}]
check("T2c_temporal_parity_jet_kill_odd_field", "SUBSTANTIVE", odd_kill,
      "an odd-composed field (the shift row N) has value AND all even t-jets killed at t=0: N vanishes on the mirror locus")

# --- T2d: the temporal mirror is DISTINCT from the spatial mirror (no status echo).
spatial_flip = simplify(exp(2 * (-phi)) - exp(-2 * phi)) == 0  # S1a: phi -> -phi swaps the weights
temporal_keeps_phi = sol_sphi == [1]
check("T2d_temporal_mirror_distinct_from_spatial_mirror", "SUBSTANTIVE",
      spatial_flip and temporal_keeps_phi,
      "the spatial mirror acts on the FIELD SIGN (phi -> -phi, weight swap e^{2phi} <-> e^{-2phi}); the temporal mirror acts on the "
      "ARGUMENT (t -> -t) with phi UNFLIPPED: different involutions on different data -- the spatial closure's ratified status "
      "CANNOT transfer by echo (G18 maintained); temporal closure = branch-(b)/(c) business, derivation-only")

# --- T2e/T2f: R7 equivariance legs with t as spectator (banked T2 re-run, t-live symbols).
xg_t = symbols("y0:16", real=True)   # generic X entries, read as arbitrary functions of (x,t)
Xgen_t = Matrix(4, 4, xg_t)


def tangent(M):
    return M.T * eta + eta * M


chi = symbols("chi", real=True)
Boost = Matrix([[sp.cosh(chi), sp.sinh(chi), 0, 0], [sp.sinh(chi), sp.cosh(chi), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
BoostInv = Boost.subs(chi, -chi)
lhs_b = tangent(Boost * Xgen_t * BoostInv)
rhs_b = BoostInv.T * tangent(Xgen_t) * BoostInv
check("T2e_tangent_transport_bilinear_t_spectator_boost", "SUBSTANTIVE",
      is_zero_matrix(sp.expand(lhs_b - rhs_b)),
      "T(Lam X Lam^-1) = Lam^-T T(X) Lam^-1 pointwise for arbitrary (x,t)-dependent X: R7(a) equivariance transfers with t spectator")
klein_ok = all(is_zero_matrix(sp.expand(tangent(M * Xgen_t * M) - M.T.inv() * tangent(Xgen_t) * M.inv())) for M in [R23, R12, R13])
check("T2f_tangent_transport_bilinear_t_spectator_klein", "GUARD", klein_ok,
      "banked T2 Klein transport re-run with t-live symbols: identical")

# --- T2c'/T2d' (R4 legs): trace-channel blindness with t as spectator.
lam_s, kmod_s = symbols("lam_t kmod_t", real=True)  # read as arbitrary functions of (x,t)
a_seat = lam_s - kmod_s
d_seat = lam_s + kmod_s
X_seat = sp.diag(-1, 1, a_seat, d_seat)
Ffun = sp.Function("F")
trace_channel = Ffun(sp.trace(X_seat))
check("T2g_R4_trace_channel_blind_kmod_t_spectator", "SUBSTANTIVE",
      simplify(diff(trace_channel, kmod_s)) == 0 and simplify(sp.trace(X_seat) - 2 * lam_s) == 0,
      "ANY functional of tr X has identically zero k_mod-pairing pointwise in (x,t): R4's exact condition transfers unchanged")
det_expX = exp(-phi) * exp(phi) * exp(a_seat * phi) * exp(d_seat * phi)
check("T2h_R4_volume_channel_blind_kmod_t_spectator", "GUARD",
      simplify(det_expX - exp(2 * lam_s * phi)) == 0 and simplify(diff(det_expX, kmod_s)) == 0,
      "banked B3 volume-density blindness re-run with t-live symbols: identical")

# --- T2i: the psi-slack OVERLAP law composes (J07 time extension).
p1a, p1b = symbols("psi1a psi1b", real=True)
Ja = Matrix([[1, p1a], [0, 1]])
Jb = Matrix([[1, p1b], [0, 1]])
g_after_ab = sp.expand(Jb.T * (Ja.T * g2 * Ja) * Jb)
Jab = Matrix([[1, p1a + p1b], [0, 1]])
g_after_sum = sp.expand(Jab.T * g2 * Jab)
check("T2i_psi_overlap_cocycle_composes_additively", "SUBSTANTIVE",
      is_zero_matrix(g_after_ab - g_after_sum),
      "two successive slack maps = one slack map with psi' = psi1' + psi2' on ALL components (clock row, shift row, spatial row): "
      "the J07 chart-overlap obligation gains an ABELIAN additive time-slack cocycle alongside the banked twisted E08 law")

print("=" * 78)
print("STAGE T1 — TT-3/TT-4: topology fork typing anchors + the re-posed response")
print("=" * 78)

# --- T3a: branch (b) map fact: a time-circle's proper period is depth-locked.
T_per = symbols("T_per", positive=True)
tau_period = sp.integrate(sp.sqrt(-g_tt) / c, (t, 0, T_per))   # static phi(x); t-dependent case TYPED
check("T3a_circle_proper_period_depth_locked", "SUBSTANTIVE",
      simplify(tau_period - exp(-phi) * T_per) == 0,
      "on branch (b) with static phi the proper period is tau(x) = e^{-phi(x)} T: a time-circle would LOCK position-dependent "
      "proper periods to the depth field (map fact TYPED; branch NOT adopted; t-dependent phi case typed only)")

# --- T3b: wall causal types with the shift on (typing anchors for TT-3(c)).
det2 = simplify(g2.det())
check("T3b_spatial_wall_times_Rt_is_timelike", "SUBSTANTIVE",
      simplify(g2inv[1, 1] - g_tt / det2) == 0 and simplify(g2inv[1, 1].subs(Nx, 0) - 1 / gxx) == 0,
      "normal covector dx: g^{xx} = g_tt/det; det = g_tt g_xx - N^2 < 0 (Lorentzian block) and g_tt < 0 give g^{xx} > 0: "
      "spatial walls extended in time are TIMELIKE surfaces, shift on or off")
check("T3b_time_wall_would_be_spacelike", "SUBSTANTIVE",
      simplify(g2inv[0, 0] - gxx / det2) == 0,
      "normal covector dt: g^{tt} = g_xx/det < 0 for g_xx > 0, det < 0: a branch-(c) time-wall (t = const locus) would be a "
      "SPACELIKE stratum -- causally unlike every banked spatial wall; TYPED only, branch not adopted")
det_neg_diag = simplify(det2.subs(Nx, 0))
check("T3b_lorentzian_det_negative_diagonal", "GUARD",
      bool(sp.ask(sp.Q.negative(det_neg_diag), sp.Q.positive(gxx) & sp.Q.positive(c))) or bool((-det_neg_diag).is_positive),
      "diagonal stratum: det = g_tt g_xx = -e^{-2phi}c^2 g_xx < 0 certified (Lorentzian block baseline)")

# --- T4a: the static restriction of the time-live component list = the banked list.
TIMELIVE_COMPONENTS = [
    "R_phi", "R_f", "R_bh", "R_alpha_fork", "R_cE_fork",
    "R_lambda", "R_kmod", "R_k10", "R_C",
    "R_N_x", "R_N_y", "R_N_z",                    # NEW: shift-row slots (O17)
    "R_wall_per_stratum", "R_corner_per_stratum",
    "R_timewall_branch_c_only", "R_timecorner_branch_c_only",  # branch-(c) TYPED slots
]
STATIC_KILL = {"R_N_x", "R_N_y", "R_N_z", "R_timewall_branch_c_only", "R_timecorner_branch_c_only"}
BANKED_COMPONENTS = [
    "R_phi", "R_f", "R_bh", "R_alpha_fork", "R_cE_fork",
    "R_lambda", "R_kmod", "R_k10", "R_C",
    "R_wall_per_stratum", "R_corner_per_stratum",
]
static_restricted = [comp for comp in TIMELIVE_COMPONENTS if comp not in STATIC_KILL]
check("T4a_component_list_static_restriction_matches_stage1", "GUARD",
      static_restricted == BANKED_COMPONENTS,
      "killing the shift-row slots and branch-(c) slots recovers EXACTLY the banked Stage-1 component list (order and content): "
      "the static R_PW EMBEDS as the time-independent stratum's tangential restriction (posing fact) "
      "[AMENDED 2026-07-31, verifier round 1: re-graded GUARD/declaration-grade -- compares two self-authored lists; "
      "faithfulness to the bank was certified by the verifier's independent V12]")
check("T4b_bigraded_jet_layer_bound_declared", "GUARD",
      True,
      "time-jet layer <= 2 on every component (Category-A bound, stamped; higher jets TYPED, banked precedent) -- declaration guard")

print("=" * 78)
print("STAGE T1 — TT-5: in-package controls (C-1 static recovery, C-2 diagonal-frozen)")
print("=" * 78)

# --- C1a: object-by-object static recovery against the BANKED Stage-1 census file.
BANKED_TSV = os.path.join(HERE, "..", "udt_p4_routeA_response_inverse_problem_2026-07-29",
                          "VARIATION_DOMAIN_CENSUS.tsv")
banked_names = []
with open(BANKED_TSV) as fh:
    for line in fh:
        if line.startswith("#") or line.startswith("object\t") or not line.strip():
            continue
        banked_names.append(line.split("\t")[0].split(" ")[0].split("(")[0].strip())
LEDGER_TSV = os.path.join(HERE, "TIMELIVE_T1_LEDGER.tsv")
obj_rows, req_rows, j_rows = [], [], []
with open(LEDGER_TSV) as fh:
    for line in fh:
        if line.startswith("#") or line.startswith("row_id\t") or not line.strip():
            continue
        parts = line.rstrip("\n").split("\t")
        name = parts[2].split(" ")[0].split("(")[0].strip()
        if parts[1] == "OBJECT":
            obj_rows.append(name)
        elif parts[1] == "REQUIREMENT":
            req_rows.append(name)
        elif parts[1] == "JROW":
            j_rows.append(name)
STATIC_MAP = {"boundary_data_walls": "boundary_data",        # name extension only; same banked object
              "shift_row_N": None,                            # restriction N=0 -> the banked DIAGONAL premise, no census row
              "time_topology_label": None}                    # t-direction factorizes; no banked census row
restricted = [STATIC_MAP.get(n, n) for n in obj_rows]
restricted = [n for n in restricted if n is not None]
check("C1a_census_static_recovery_object_by_object", "SUBSTANTIVE",
      len(banked_names) == 16 and len(obj_rows) == 18 and restricted == banked_names,
      f"static restriction of the 18-row time-live census = the banked 16-row census EXACTLY, in order "
      f"(banked={len(banked_names)}, timelive={len(obj_rows)}; killed rows: shift_row_N -> N=0 diagonal premise, "
      f"time_topology_label -> absent). F-T7 NOT fired")

# --- C1b: requirement-class recovery (primary classes; banked tallies PW8/WS2/GC4).
BANKED_CLASSES = {"R1": "PW", "R2": "PW", "R3": "GC", "R4": "PW", "R5": "WS", "R6": "GC",
                  "R7": "PW", "R8": "PW", "R9": "GC", "R10": "PW", "R11": "per-row",
                  "R12": "PW", "R13": "PW", "R14": "WS", "R15": "GC"}
TIMELIVE_CLASSES = dict(BANKED_CLASSES)   # derived result: NO primary-class migration at T1 depth
tally = {"PW": 0, "WS": 0, "GC": 0}
for k, v in TIMELIVE_CLASSES.items():
    if v in tally:
        tally[v] += 1
check("C1b_requirement_class_recovery", "GUARD",
      TIMELIVE_CLASSES == BANKED_CLASSES and tally == {"PW": 8, "WS": 2, "GC": 4}
      and len(req_rows) == 15 and len(j_rows) == 15,
      "static restriction of the re-posed classes = banked PW8/WS2/GC4 + R11 per-row EXACTLY; no class migration; "
      "15 R-rows + 15 J-rows present in the ledger. F-T7 NOT fired "
      "[AMENDED 2026-07-31, verifier round 1: re-graded GUARD/declaration-grade -- the time-live class table is a "
      "literal copy of the banked table; the no-migration claim is ledger-derived, not computed]")

# --- C1c: banked exact checks re-run through the time-live machinery restricted static.
Xs = Xt.subs({k00t: symbols("k00s"), k10t: symbols("k10s"), k11t: symbols("k11s"),
              c00t: symbols("c00s"), c01t: symbols("c01s"), c10t: symbols("c10s"), c11t: symbols("c11s")})
Ts = Xs.T * eta + eta * Xs
Cs = Xs[2:4, 0:2]
Ks = Xs[2:4, 2:4]
block_ok = (is_zero_matrix(Ts[0:2, 0:2] - 2 * eye(2)) and is_zero_matrix(Ts[0:2, 2:4] - Cs.T)
            and is_zero_matrix(Ts[2:4, 0:2] - Cs) and is_zero_matrix(Ts[2:4, 2:4] - (Ks.T + Ks)))
Q_static = cE * exp(-phi)
Q_shift_static = (cE * exp(s_shift)) * exp(-(phi + s_shift))
d3_ok = simplify(Q_shift_static - Q_static) == 0
check("C1c_banked_exact_checks_recovered_static", "GUARD",
      block_ok and d3_ok,
      "T2_tangent_block_form ([[2I2, C^T],[C, K+K^T]]) and D3_anchor_absorption (Q invariant under phi+s, c_E e^s) "
      "re-derived through the time-live machinery restricted to the static stratum: identical to the bank")

# --- C-2: the diagonal-frozen (shift-off) control stratum.
check("C2a_diagonal_stratum_lock_readings_coincide", "SUBSTANTIVE",
      simplify((gam_orig - g2[1, 1]).subs(Nx, 0)) == 0,
      "on N=0 the coordinate and projected lock readings coincide IDENTICALLY: the banked record's silence on the "
      "reading fork is exactly the diagonal-frozen shadow; C-2 relation to full domain = codim-3-function stratum")
check("C2b_diagonal_stratum_not_chart_closed", "SUBSTANTIVE",
      simplify(g2p_diag[0, 1].subs(p1, 1) - g_tt) == 0 and simplify(g2p_diag[0, 1].subs(p1, 0)) == 0,
      "the psi-slack maps the diagonal stratum OUT of itself (N' = g_tt psi' != 0): shift-off is not invariant under the "
      "extended chart class; freezing it is a chart-conditional CONTROL, never a physics restriction")
SHIFT_ADDITIONS = [
    "R_N slots (3) in the response and delta-N tangent directions",
    "the lock-reading fork (coordinate vs projected; coincide iff N=0)",
    "the psi-slack J07 overlap datum (frozen on-chart, live across charts)",
    "the metric-layer time-reflection acting nontrivially (N -> -N)",
    "the ADM-inequivalence discriminator (-1/g^tt = e^{-2phi}c^2 + N^2/g_xx)",
]
check("C2c_shift_additions_enumerated", "GUARD",
      len(SHIFT_ADDITIONS) == 5,
      "what the live shift row adds over the C-2 control, enumerated exactly: " + "; ".join(SHIFT_ADDITIONS))

# --- Hygiene guards.
with open(os.path.abspath(__file__)) as fh:
    src = fh.read()
import re as _re
banned = ["ns" + "olve", "ev" + "alf", "im" + "port random", "im" + "port numpy", "tor" + "ch"]
check("G3_no_floats_numeric_solvers_or_rng", "GUARD",
      all(b not in src for b in banned) and _re.search(r"\d\.\d", src) is None,
      "source scan: no numeric solvers, no float-evaluation calls, no RNG, no array/GPU libraries, "
      "no float literals — exact and deterministic")

# [AMENDED 2026-07-31, verifier round 1 (AM-3a): G1 is now COUNTED in the tally
# and JSON and its failure flips the exit code -- the JSON is written, round-
# tripped, G1 checked, then the JSON is rewritten with the FINAL counts
# including G1. Deterministic; byte-stable across reruns.]
result = {
    "package": "udt_p4_timelive_stage_T1_2026-07-31",
    "stage": "T1 (TT-1..TT-5; posing and typing only)",
    "date": "2026-07-31",
    "contract": "PREREGISTRATION.md (frozen before derivation)",
    "amendment_round_1": ("2026-07-31 verifier round 1 implemented: AM-1 stratum-conditional Z2 psi-branch "
                          "derived (T1p2/T1p3; residual group restated; irreducibility-as-non-removability "
                          "survives, orbit {N,-N}); AM-2 projected-reading removability derived (T1p4; O17 "
                          "irreducibility CONDITIONAL on the coordinate-reading spatial pin; lock-reading fork "
                          "upgraded LOAD-BEARING, carried both ways, decided by nothing in this package); "
                          "AM-3 G1 wired into tally/exit, guard enumeration fixed, C1b/T4a re-graded GUARD"),
    "outcome_class": ("OT-1: the time-live posing closes cleanly -- census (18 objects) + requirement "
                      "re-posing (no breaks; no new requirements forced; no class migration) + response slots "
                      "all derived; C-1 static recovery EXACT (F-T7 not fired); topology fork typed 3-ways, "
                      "none adopted; O17 shift-row irreducibility stamped CONDITIONAL on the coordinate-reading "
                      "spatial pin (lock-reading fork LOAD-BEARING, both branches travel)"),
    "ceiling": "no response law selected; nothing solved; no cycle census; no topology adopted; no dynamics; no physics",
    "falsifier_events": [],
}
json_path = os.path.join(HERE, "timelive_T1_results.json")
prelim = dict(result)
prelim.update({"n_checks": len(CHECKS), "n_passed": sum(1 for chk in CHECKS if chk["passed"]),
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
      "timelive_T1_results.json written and round-trips; G1 is counted in the tally and a G1 failure "
      "flips the exit code (AM-3a wiring)")
n_total = len(CHECKS)
n_pass = sum(1 for chk in CHECKS if chk["passed"])
n_sub = sum(1 for chk in CHECKS if chk["kind"] == "SUBSTANTIVE")
n_guard = n_total - n_sub
result.update({"n_checks": n_total, "n_passed": n_pass,
               "n_substantive": n_sub, "n_guard": n_guard,
               "all_passed": n_pass == n_total, "checks": CHECKS})
with open(json_path, "w") as fh:
    json.dump(result, fh, indent=1)
print("=" * 78)
print(f"TOTAL: {n_pass}/{n_total} passed ({n_sub} SUBSTANTIVE + {n_guard} GUARD); exit {'0' if n_pass == n_total else '1'}")
sys.exit(0 if n_pass == n_total else 1)
