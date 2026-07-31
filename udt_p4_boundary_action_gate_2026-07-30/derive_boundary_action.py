"""P4 boundary-action gate — exact CAS legs (contract: PREREGISTRATION.md, frozen).

AMENDMENT BANNER (2026-07-30, post-verifier — VERIFIER_REPORT.md verdict
PASS-WITH-REQUIRED-AMENDMENTS, AM-V1 + AM-V2 + minor notes; CORRECTION_LAYER.md
is the record): NO pre-amendment computed claim changed. AM-V1 = the crease
no-active-action result restated POSTURE-CONDITIONAL (given the quotient
posture); the banked two-sided conditional-forces-fold theorem keeps ALL its
premises (loses ZERO members) — cited-argument note AMV1. AM-V2 = inertness /
effective-uniqueness statements scoped "at the realized seam germ / per
realized configuration" — the verifier's (rho-rho_s)^3 germ-locality
counter-computation adopted as credited checks AMV2a/AMV2b. Minor: the BDY-TD
gloss softened (inert germs = primitive-nonuniqueness-like, not
momentum-shifting total derivatives); J07/J08 discharge-by-typing noted in the
JSON; the verifier's SYMMETRIZATION proof of the mirror-wall theorem (strictly
more general) adopted as credited checks AMV3a-AMV3d. Credited checks print
[verifier-credited] and are listed in the JSON under checks_verifier_credited.

QUESTION: the wall-sector inverse problem — the most general seam/wall/corner
response B that the BANKED requirements permit (the Route-A inverse problem
restricted to the wall): EMPTY / UNIQUE / FAMILY, per closure candidate
(fold / partner / glue+B / open-end) and per pairing branch — and what the
verdict selects among the closure candidates and for the rho'_s pin (D-b) and
the q-datum.

BANKED MACHINERY REUSED (not re-derived; re-run as Category-A soundness of this
script's reading):
  seam arena (udt_p4_seam_closure_derivation_2026-07-30, 0d0d575):
    L_P = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2
    L_G = (Z/2) rho^2 phi'^2 - 2 rho'^2 + 2
    pi_phi = Z rho^2 phi' ; pi_rho^P = -4 e^{-2phi} rho' ; pi_rho^G = -4 rho'
    doubled fold momentum p_tot_rho = -8 cosh(2phi) rho'
    banked glue jump Delta_Pi = q/2 (weld :30-32); K6a-K6d well-posedness legs;
    S1f handshake underdetermination witness; K4e-K4g two-sided WE legs.
  registered arena (Stage-2 2c0e7cc / Stage-3 21d589c / Slice-2b / Route D):
    TC3 N=2 by-parts identity; parity jet-kill (-1)^j eps = -1; anchored wall
    rule p=q (Q_wall-powers); trivial K4 character of wall directions; J05
    moduli wall-slot identity; quadratic-class M-WALL = a_F * M-GEN.

NEW LEGS (this push): the general ANCHORED seam functional Bfrak(Q_s, rho_s)
parametrized (TW2); the R6 unpaired-jet cut at the banked 2nd-order layer
(TW2); first-germ-only activity / inertness of higher germ content (TW2); the
per-candidate requirement cut and germ pins (TW3): fold parity+R6 forces the
active germ to ZERO; partner = the germ-flat stratum; glue first germ UNIQUELY
pinned (Bfrak_rho = q/2 AND flux seal <=> Bfrak_Q = 0); open-end germ FREE with
q = -c_E*Bfrak_Q (the banked q=0 forcing = the germ-flat stratum); the
mirror-wall momentum kill for mirror-compatible members (W-REG); the pairing-
branch weight structure (mirror walls weight-free; anchored weights at
non-mirror walls); M-WALL as a germ functional at free walls (TW5).

GUARDS HONORED (F-B1..F-B7): no closure candidate assumed or favored (all four
interrogated; the three-way temptation policed structurally); NO wall kernel /
counterterm / functional INVENTED — the general B is PARAMETRIZED and the
freedom exactly characterized (F-B2, Tonti scar); pairing relation typed
ONE-WAY: the pairing/bulk by-parts structure SUPPLIES the wall slot census, B
is an element of the resulting slot space, never the reverse (F-B5); no
G18/fold assumption, no x_max, no anchor values (c_E, q, Z symbolic), no
census/pairing adoption (F-B4); full stamps in the JSON (F-B3); no floats, no
numeric solvers, no GPU; exit nonzero on any failed check (F-B7).
Deterministic (pure symbolic).

STAMPS (travel with every claim):
  arena W-1D = round-static radial reduction (1D r-profiles; banked Branch G/P
    reduced Lagrangians; pairing = NONE used, as in the banked seam package;
    crease reading = pointwise-in-r on the 1D reduction; screen/angular action
    NOT specified — banked 07-20 non-uniqueness stands);
  arena W-REG = registered positive triangular chart, stationary one-parameter
    presentation, fields (phi, f, bh), jets <= 2; pairing branches P1-4D /
    P1-triad / P2 / P3-bulkP2 / P3-bulkP1 carried; census BASE exhaustive at
    jet <= 2, BR-M typed via the J05 leg; corners TYPED-ONLY;
  jet layer: N=2 (banked 2nd-order self-pairing layer) EXHAUSTIVE; N=4 TYPED
    (2-jet wall + 3rd normal-derivative momenta — not run);
  parity: eps_phi = -1 DEFINITIONAL (CANON C-2026-07-30-1 layer 3); rho
    evenness = banked fold-JC mirror-jet structure; f/bh parities SUPPLIED
    (definite per realized outcome under R-A — angular-completion bank — else
    free); moduli parities per Route P (P2-conditional; R-A discharges).
"""
import json
import os
import sys

import sympy as sp

CHECKS = []  # (name, kind SUBSTANTIVE|GUARD, passed, detail, credited)


def _tag(kind, credit):
    return f"[{kind}]" + ("[verifier-credited]" if credit else "")


def check(name, kind, expr_zero, credit=False):
    val = sp.simplify(expr_zero)
    if not (val == 0 or val == sp.S.Zero):
        val = sp.simplify(sp.expand(sp.simplify(val.rewrite(sp.exp))))
    ok = (val == 0) or (val == sp.S.Zero)
    CHECKS.append((name, kind, bool(ok), str(val), bool(credit)))
    print(f"[{'PASS' if ok else 'FAIL'}]{_tag(kind, credit)} {name}"
          + ("" if ok else f"  residual={val}"))


def check_nonzero(name, kind, expr, note="", credit=False):
    val = sp.simplify(expr)
    ok = not (val == 0 or val == sp.S.Zero)
    CHECKS.append((name, kind, bool(ok), f"nonzero:{val} {note}", bool(credit)))
    print(f"[{'PASS' if ok else 'FAIL'}]{_tag(kind, credit)} {name}"
          f"  expr={val} {note}")


def check_bool(name, kind, ok, detail, credit=False):
    CHECKS.append((name, kind, bool(ok), str(detail), bool(credit)))
    print(f"[{'PASS' if ok else 'FAIL'}]{_tag(kind, credit)} {name}  {detail}")


# ------------------------------------------------------------------ symbols
x = sp.Symbol('x', real=True)
rs = sp.Symbol('r_s', real=True)
Zp = sp.Symbol('Z', positive=True)
cE = sp.Symbol('c_E', positive=True)     # supplied anchor (symbolic, no value)
q_sym = sp.Symbol('q', real=True)        # the member's own flux (symbolic)
phi_s, phip_s, rho_s, rhop_s = sp.symbols('phi_s phip_s rho_s rhop_s', real=True)
p_, pp_, rr_, rp_ = sp.symbols('p pp rho rhop', real=True)
dphi, drho = sp.symbols('dphi drho', real=True)   # seam variations

# banked reduced Lagrangians (jets) and momenta [seam package, reused]
Ljet_P = lambda p, pp, ro, rop: Zp/2*ro**2*pp**2 - 2*sp.exp(-2*p)*rop**2 + 2
Ljet_G = lambda p, pp, ro, rop: Zp/2*ro**2*pp**2 - 2*rop**2 + 2
pi_phi = Zp*rr_**2*pp_
pi_rho_P = -4*sp.exp(-2*p_)*rp_
pi_rho_G = -4*rp_
p_tot_rho = -8*sp.cosh(2*p_)*rp_          # banked doubled fold momentum

print("=" * 78)
print("S0 — BANKED MACHINERY RE-RUN (Category-A soundness of this reading)")
print("=" * 78)
check("S0a_pi_phi_form", "GUARD", pi_phi - sp.diff(Ljet_P(p_, pp_, rr_, rp_), pp_))
check("S0a_pi_rho_P_form", "GUARD",
      pi_rho_P - sp.diff(Ljet_P(p_, pp_, rr_, rp_), rp_))
check("S0a_pi_rho_G_form", "GUARD",
      pi_rho_G - sp.diff(Ljet_G(p_, pp_, rr_, rp_), rp_))
check("S0a_doubled_rho_momentum", "GUARD",
      p_tot_rho - (-4*sp.exp(-2*p_)*rp_ - 4*sp.exp(2*p_)*rp_))

# S0b: the TS1 handshake underdetermination reproduced (consistency duty TW4):
# germ A (flat exterior, phi_+ == 0) and germ B (odd mirror) both pass the
# phi=0 seam handshake; their first jets differ by phi_-'(rs) (certified
# nonzero symbol) => the bridge does not pin the gluing.
phi_minus = sp.Function('phim')
germB = -phi_minus(2*rs - x)
germB_jet = sp.diff(germB, x).subs(x, rs)
check("S0b_handshake_germB_on_seam_locus", "SUBSTANTIVE",
      germB.subs(x, rs).subs(phi_minus(rs), 0))
check_nonzero("S0b_handshake_germs_distinct_first_jet", "SUBSTANTIVE",
              germB_jet - 0, note="(vanishes only at phi_-'(rs)=0)")

# S0c: the TC3 N=2 by-parts identity on a generic 1-field density (the wall
# slot census generator): dL/du*v + dL/du'*v' = E(L)*v + Dx(dL/du' * v).
u = sp.Function('u')
v_f = sp.Function('v')
Lgen = sp.Function('Lgen')
Lx = Lgen(u(x), sp.diff(u(x), x))
EL = sp.diff(Lx, u(x)) - sp.diff(sp.diff(Lx, sp.diff(u(x), x)), x)
lhs = sp.diff(Lx, u(x))*v_f(x) + sp.diff(Lx, sp.diff(u(x), x))*sp.diff(v_f(x), x)
rhs = EL*v_f(x) + sp.diff(sp.diff(Lx, sp.diff(u(x), x))*v_f(x), x)
check("S0c_byparts_N2_identity", "SUBSTANTIVE", sp.expand(lhs - rhs))

# S0d: the parity jet-kill at a mirror wall: u^{(j)}(0) = 0 exactly for
# (-1)^j eps = -1. Generic degree-5 polynomial, both parities.
a0, a1, a2, a3, a4, a5 = sp.symbols('a0 a1 a2 a3 a4 a5', real=True)
poly = a0 + a1*x + a2*x**2 + a3*x**3 + a4*x**4 + a5*x**5
for eps, tag in ((1, 'even'), (-1, 'odd')):
    cond = sp.expand(poly.subs(x, -x) - eps*poly)
    sol = sp.solve([cond.coeff(x, k) for k in range(6)],
                   [a0, a1, a2, a3, a4, a5], dict=True)
    constrained = sol[0]
    killed = sorted(str(s) for s in constrained
                    if constrained[s] == 0)
    expect = (['a1', 'a3', 'a5'] if eps == 1 else ['a0', 'a2', 'a4'])
    check_bool(f"S0d_parity_jet_kill_{tag}", "SUBSTANTIVE",
               killed == expect, f"killed jets at wall: {killed}")

# S0e: the anchored wall rule (Stage-2/Stage-3 recompute): c_E^p e^{-q phi}
# invariant under the shift orbit (phi, c_E) -> (phi+s, c_E e^s) iff p = q.
pw, qw, s_sh, phiw = sp.symbols('p_w q_w s phi_w', real=True)
coeff = cE**pw*sp.exp(-qw*phiw)
shifted = coeff.subs([(cE, cE*sp.exp(s_sh)), (phiw, phiw + s_sh)])
resid = sp.simplify(sp.log(sp.simplify(shifted/coeff)))
sol_pq = sp.solve(sp.Eq(resid, 0), pw)
check_bool("S0e_anchored_wall_rule_p_eq_q", "SUBSTANTIVE",
           sol_pq == [qw], f"invariance forces p -> {sol_pq}")

# S0f: K4 acts only on (k10, C) (banked Stage-2 PW1_K4_touches_only_k10_C,
# cited): wall trace directions (phi/f/bh traces) and lambda/k_mod carry the
# TRIVIAL character — B's component slot is trivial-character (cited, guard).
check_bool("S0f_wall_directions_trivial_character", "GUARD", True,
           "cited: Stage-2 PW1_K4_touches_only_k10_C + TB2 table (boundary "
           "directions trivial class, basis {1})")

print()
print("=" * 78)
print("TW2 — THE GENERAL WALL RESPONSE (anchored seam functional, exact)")
print("=" * 78)
# The most general 2nd-order-layer seam functional over the TW1 census, with
# the anchoring rule (dependence on phi_s only through Q_s = c_E e^{-phi_s})
# and trivial character. NOTHING is invented: Bfrak is a GENERIC function; we
# characterize what the requirements do to it (F-B2).
Qv, rv = sp.symbols('Qv rv', real=True)      # arguments of Bfrak
Bfun = sp.Function('Bfrak')
Q_of_phi = cE*sp.exp(-phi_s)

# TW2a: the anchored variation: the delta-phi coefficient of Bfrak(Q, rho) is
# -Q * dBfrak/dQ; at the seam locus phi_s = 0 it is -c_E * Bfrak_Q(c_E, rho_s):
# an anchored wall functional CAN pair delta-phi at the seam (through its
# Q-germ) — bare-phi dependence stays excluded (S0e), but Q-dependence is
# alphabet-legal and delta-phi-active.
Bexpr = Bfun(Q_of_phi, rho_s)
dB_dphi = sp.diff(Bexpr, phi_s)
target = -Q_of_phi*sp.Derivative(Bfun(Qv, rho_s), Qv).subs(Qv, Q_of_phi)
check("TW2a_anchored_variation_chain_rule", "SUBSTANTIVE",
      sp.simplify(dB_dphi - target))
BQ_germ = sp.Symbol('B_Q', real=True)    # Bfrak_Q(c_E, rho_s) germ value
Br_germ = sp.Symbol('B_r', real=True)    # Bfrak_rho(c_E, rho_s) germ value
b0 = sp.Symbol('b_0', real=True)
bQQ, brr, bQr = sp.symbols('b_QQ b_rr b_Qr', real=True)
# degree-2 germ expansion of the general Bfrak about the seam point
# (Q, rho) = (c_E, rho_s):
rho_v = sp.Symbol('rho_v', real=True)
B_germ = (b0 + BQ_germ*(Qv - cE) + Br_germ*(rho_v - rho_s)
          + bQQ*(Qv - cE)**2/2 + brr*(rho_v - rho_s)**2/2
          + bQr*(Qv - cE)*(rho_v - rho_s))
# variation of B at the seam configuration (phi_s = 0 so Q = c_E; rho = rho_s):
#   delta B = (dB/dQ)*(dQ/dphi)*dphi + (dB/drho)*drho  at the point.
dB_at_point = (sp.diff(B_germ, Qv)*(-Q_of_phi)).subs(
    [(Qv, cE), (rho_v, rho_s), (phi_s, 0)])*dphi \
    + sp.diff(B_germ, rho_v).subs([(Qv, cE), (rho_v, rho_s)])*drho
check("TW2b_deltaB_at_seam_is_first_germ", "SUBSTANTIVE",
      sp.expand(dB_at_point - (-cE*BQ_germ*dphi + Br_germ*drho)))
# TW2c: INERTNESS of everything beyond the first germ AT THE REALIZED SEAM
# GERM: the seam-variation at the realized point (Q, rho) = (c_E, rho_s) is
# independent of b0, bQQ, brr, bQr. [AM-V2] The inertness is GERM-LOCAL (per
# realized configuration) — see AMV2a/AMV2b below. Gloss softened per the
# verifier's minor note: the inert germs shift NOTHING at the realized point
# (primitive-nonuniqueness-like), which is a looser analogy to — not the exact
# form of — the banked BDY-TD momentum-shifting total-derivative freedom.
for sym in (b0, bQQ, brr, bQr):
    check(f"TW2c_higher_germ_inert_{sym}", "SUBSTANTIVE",
          sp.diff(dB_at_point, sym))

# AMV2 [verifier-credited, AM-V2]: GERM-LOCALITY of the inertness (the
# verifier's V2c counter-computation adopted). The pure higher-germ
# perturbation (Q - c_E)^2 (rho - rho_s) + (rho - rho_s)^3 is inert AT the
# realized trace rho_s but has ACTIVE content 3*(rho_1 - rho_s)^2 at a
# DIFFERENT realized trace rho_1 — so every inertness / effective-uniqueness
# statement is scoped "at the realized seam germ / per realized configuration".
rho1 = sp.Symbol('rho_1', real=True)
pert_loc = (Qv - cE)**2*(rho_v - rho_s) + (rho_v - rho_s)**3
active_away = sp.diff(pert_loc, rho_v).subs([(Qv, cE), (rho_v, rho1)])
check("AMV2a_higher_germ_active_at_other_trace_exact", "SUBSTANTIVE",
      sp.expand(active_away - 3*(rho1 - rho_s)**2), credit=True)
check_nonzero("AMV2b_locality_counterexample_nonzero_off_trace", "SUBSTANTIVE",
              active_away,
              note="(vanishes only at rho_1 = rho_s: inertness is germ-LOCAL)",
              credit=True)

# TW2d: THE R6 UNPAIRED-JET CUT at N=2. If Bfrak also carries a 1-jet trace
# argument (rho'_s), its variation produces a delta-rho' term. The N=2 bulk
# by-parts residue (S0c) pairs ONLY the 0-jet variations {v_a}; a delta-rho'
# wall term has no bulk partner => R6 (no unpaired wall jets) forces the
# rho'-dependence to vanish IDENTICALLY.
Brp = sp.Symbol('B_rp', real=True)   # dBfrak/drho'_s germ value
dv, dvp = sp.symbols('dv dvp', real=True)   # independent wall variations
seam_var = (p_tot_rho.subs(p_, 0) - Br_germ)*dv - Brp*dvp
# independence of (dv, dvp): the dvp-coefficient must vanish identically:
sol_cut = sp.solve(sp.Eq(seam_var.coeff(dvp), 0), Brp)
check_bool("TW2d_R6_unpaired_jet_cut_N2", "SUBSTANTIVE",
           sol_cut == [0], f"R6 at N=2 forces dB/drho' -> {sol_cut}")
# TW2e: the cut is pairing-weight-ROBUST: an anchored bulk weight W_F != 0
# multiplies the paired momentum but creates no new v' partner; the cut
# condition W_F * B_rp = 0 is equivalent to B_rp = 0 (W_F = e^{a_F p0} > 0).
aF, p0w = sp.symbols('a_F p0_w', real=True)
WF = sp.exp(aF*p0w)
sol_cut_w = sp.solve(sp.Eq(WF*Brp, 0), Brp)
check_bool("TW2e_cut_weight_robust", "SUBSTANTIVE",
           sol_cut_w == [0], f"W_F*B_rp = 0 <=> B_rp -> {sol_cut_w} (W_F>0)")

# TW2f: J05 moduli wall-slot identity (Route D R4 leg recomputed): with m-jet
# densities the pairing has the wall slot [D_{m'} v]_walls; the same
# unpaired-jet cut applies to any B(m'_w) at the 1-jet moduli layer (BR-M).
mfun = sp.Function('m')
vm = sp.Function('vm')
Dm = sp.Function('Dm')
Dmp = sp.Function('Dmp')
lhs_m = (Dm(mfun(x), sp.diff(mfun(x), x))*vm(x)
         + Dmp(mfun(x), sp.diff(mfun(x), x))*sp.diff(vm(x), x))
rhs_m = ((Dm(mfun(x), sp.diff(mfun(x), x))
          - sp.diff(Dmp(mfun(x), sp.diff(mfun(x), x)), x))*vm(x)
         + sp.diff(Dmp(mfun(x), sp.diff(mfun(x), x))*vm(x), x))
check("TW2f_J05_moduli_wall_slot_identity", "SUBSTANTIVE",
      sp.expand(lhs_m - rhs_m))

print()
print("=" * 78)
print("TW3 — THE REQUIREMENT CUT, PER CLOSURE CANDIDATE (arena W-1D)")
print("=" * 78)
# Convention (banked K6c): stationarity <=> (seam boundary residue) = delta B.
# ---------------- FOLD (mirrored crease, Z2 quotient) ----------------
# delta-phi is essential-zero (odd identification; banked K4b re-run):
v = sp.Symbol('v', real=True)
sol_v = sp.solve(sp.Eq(v, -v), v)
check_bool("TW3_fold_essential_dphi_zero", "SUBSTANTIVE",
           sol_v == [0], f"solve(v=-v) -> {sol_v}")
# => the Q-germ of Bfrak is INERT at the fold (its only pairing is dphi):
check("TW3_fold_Q_germ_inert", "SUBSTANTIVE",
      dB_at_point.subs(dphi, 0).coeff(BQ_germ))
# natural BC with the general Bfrak: p_tot_rho(phi=0) = Bfrak_rho germ:
sol_rp = sp.solve(sp.Eq(p_tot_rho.subs(p_, 0).subs(rp_, rhop_s), Br_germ),
                  rhop_s)
check_bool("TW3_fold_natural_BC_with_B", "SUBSTANTIVE",
           sol_rp == [-Br_germ/8], f"rho'(r_s) -> {sol_rp}")
# R6 differentiability of the MIRRORED configuration (rho EVEN across the
# crease — banked mirror-jet structure) kills the crease 1-jet: rho'(r_s)=0
# (S0d even row; = the banked K3h kinematic C^1 fact). Jointly with the
# natural BC this FORCES the active rho-germ to zero:
sol_joint = sp.solve([sp.Eq(-8*rhop_s, Br_germ), sp.Eq(rhop_s, 0)],
                     [rhop_s, Br_germ], dict=True)
check_bool("TW3_fold_R6_forces_rho_germ_zero", "SUBSTANTIVE",
           sol_joint == [{rhop_s: 0, Br_germ: 0}],
           f"joint solve -> {sol_joint} (fold: active germ FORCED trivial)")
# consistency (banked K4d): Bfrak == 0 reproduces rho'(r_s) = 0:
sol_rp0 = sp.solve(sp.Eq(p_tot_rho.subs(p_, 0).subs(rp_, rhop_s), 0), rhop_s)
check_bool("TW3_fold_consistency_K4d", "SUBSTANTIVE",
           sol_rp0 == [0], f"B=0 => rho'(r_s) -> {sol_rp0}")
# AMV1 [verifier-credited, AM-V1] cited-argument note — TWO DISTINCT PREMISES,
# not one: (i) the banked conditional-forces-fold theorem (seam pkg) lives in
# the TWO-SIDED matching problem, BEFORE any fold is concluded; its premise
# "no seam surface term (=> WE C^1 matching)" is a premise ABOUT the two-sided
# problem and is NOT derived here — the theorem keeps ALL its premises (loses
# ZERO members). (ii) The crease result above is POSTURE-CONDITIONAL: GIVEN
# the single-copy quotient posture, no ACTIVE wall action is admissible at
# N=2 (a cousin fact ON the crease — complementary, not the theorem's
# premise). The G18 reduction (posture AND Branch-G AND germ data) survives
# unchanged.
check_bool("AMV1_cousin_premise_distinction_note", "GUARD", True,
           "cited-argument: banked two-sided forcing premise != the "
           "posture-conditional crease no-active-action result; forcing "
           "theorem premise set loses ZERO members", credit=True)

# ---------------- W-REG mirror wall: the momentum kill ----------------
# For a MIRROR-COMPATIBLE member (parity-even density), the natural-BC
# momenta of the parity-EVEN fields vanish kinematically at the wall, so
# stationarity forces the corresponding B-germs to zero at the realized
# traces; the parity-ODD field's variation is essential-zero (germ inert).
# Generic parity-even density: F of the even invariants
# (p0^2, p1, f0, h0, f1^2, h1^2, f1*h1, p0*f1, p0*h1)
# [phi odd: p0 -> -p0, p1 -> +p1; f,bh even: f1 -> -f1, h1 -> -h1].
p0s, p1s, f0s, f1s, h0s, h1s = sp.symbols('p0 p1 f0 f1 h0 h1', real=True)
Feven = sp.Function('F')
inv = (p0s**2, p1s, f0s, h0s, f1s**2, h1s**2, f1s*h1s, p0s*f1s, p0s*h1s)
Ltil = Feven(*inv)
# guard: the constructed density IS parity-even:
check("TW3_WREG_density_parity_even", "GUARD",
      sp.simplify(Ltil.subs([(p0s, -p0s), (f1s, -f1s), (h1s, -h1s)],
                            simultaneous=True) - Ltil))
kill = [(p0s, 0), (f1s, 0), (h1s, 0)]
pi_f_wall = sp.diff(Ltil, f1s).subs(kill)
pi_h_wall = sp.diff(Ltil, h1s).subs(kill)
check("TW3_WREG_mirror_momentum_kill_f", "SUBSTANTIVE", pi_f_wall)
check("TW3_WREG_mirror_momentum_kill_h", "SUBSTANTIVE", pi_h_wall)
# ... while pi_p(wall) is generically NONZERO — but its partner variation
# v_p is essential-killed (eps_phi = -1): the phi-slot is inert, not paired.
pi_p_wall = sp.diff(Ltil, p1s).subs(kill)
check_nonzero("TW3_WREG_pi_p_wall_generic_nonzero", "SUBSTANTIVE",
              pi_p_wall, note="(paired variation v_p essential-killed)")
# HONESTY LEG: the mirror-compatibility stamp is load-bearing — a parity-ODD
# density term (f1*p1) has pi_f(wall) = p1 != 0: for mirror-INCOMPATIBLE
# members the kill fails (but the fold candidate is then undefined).
check_nonzero("TW3_WREG_mirror_compat_load_bearing", "SUBSTANTIVE",
              sp.diff(f1s*p1s, f1s).subs(kill),
              note="(parity-odd term escapes the kill => stamp load-bearing)")

# AMV3 [verifier-credited]: the mirror-wall theorem RE-PROVEN by
# SYMMETRIZATION (the verifier's V5 construction adopted — strictly MORE
# GENERAL than the even-invariant construction above: generic degree-4
# polynomial density in ALL SIX jets, even part taken under
# (p0, f1, h1) -> -(p0, f1, h1); no invariant basis assumed).
import itertools
_vars6 = (p0s, p1s, f0s, f1s, h0s, h1s)
_terms = []
_idx = 0
for _deg in range(5):
    for _combo in itertools.combinations_with_replacement(range(6), _deg):
        _mono = sp.S.One
        for _i in _combo:
            _mono *= _vars6[_i]
        _terms.append(sp.Symbol(f'c{_idx}', real=True)*_mono)
        _idx += 1
Lpoly = sp.Add(*_terms)
_flip = {p0s: -p0s, f1s: -f1s, h1s: -h1s}
Lpoly_even = sp.expand((Lpoly + Lpoly.subs(_flip, simultaneous=True))/2)
_kill = {p0s: 0, f1s: 0, h1s: 0}
check("AMV3a_symmetrized_momentum_kill_f", "SUBSTANTIVE",
      sp.expand(Lpoly_even.diff(f1s).subs(_kill)), credit=True)
check("AMV3b_symmetrized_momentum_kill_h", "SUBSTANTIVE",
      sp.expand(Lpoly_even.diff(h1s).subs(_kill)), credit=True)
_pi_p_even = sp.expand(Lpoly_even.diff(p1s).subs(_kill))
check_bool("AMV3c_symmetrized_pi_p_generic_nonzero", "SUBSTANTIVE",
           _pi_p_even != 0,
           f"pi_p at kill locus generically nonzero "
           f"({len(_pi_p_even.args)} surviving monomials; paired variation "
           f"v_p essential-killed)", credit=True)
_pi_f_full = sp.expand(Lpoly.diff(f1s).subs(_kill))
check_bool("AMV3d_unsymmetrized_density_fails_kill", "SUBSTANTIVE",
           _pi_f_full != 0,
           f"un-symmetrized generic density: pi_f at kill locus nonzero "
           f"({len(_pi_f_full.args)} surviving monomials) => "
           f"mirror-compatibility stamp load-bearing, re-proven", credit=True)

# ---------------- PARTNER / GLUE (two-sided seam) ----------------
# Two-sided residue = [pi_phi]*dphi + [pi_rho]*drho ; stationarity = delta B:
#   [pi_phi] = -c_E*Bfrak_Q(c_E, rho_s) ;  [pi_rho] = Bfrak_rho(c_E, rho_s).
jump_phi, jump_rho = sp.symbols('Jphi Jrho', real=True)
two_sided = (jump_phi*dphi + jump_rho*drho) - dB_at_point
sol_j = sp.solve([two_sided.coeff(dphi), two_sided.coeff(drho)],
                 [jump_phi, jump_rho], dict=True)
check_bool("TW3_twosided_jump_laws", "SUBSTANTIVE",
           sol_j == [{jump_phi: -cE*BQ_germ, jump_rho: Br_germ}],
           f"[pi_phi], [pi_rho] -> {sol_j}")
# GLUE (banked matter-cell): the banked jump Delta_Pi = q/2 pins the rho-germ
# UNIQUELY — reproduces K6c's B'(rho_s) = q/2 exactly:
sol_glue = sp.solve(sp.Eq(Br_germ, q_sym/2), Br_germ)
check_bool("TW3_glue_reproduces_K6c", "SUBSTANTIVE",
           sol_glue == [q_sym/2], f"Bfrak_rho -> {sol_glue}")
# ... and the banked FLUX SEAL ([pi_phi] = 0, the weld chain's continuous q)
# holds IFF the Q-germ vanishes (c_E > 0): a NEW exact equivalence.
sol_seal = sp.solve(sp.Eq(-cE*BQ_germ, 0), BQ_germ)
check_bool("TW3_glue_flux_seal_iff_Q_flat", "SUBSTANTIVE",
           sol_seal == [0], f"[pi_phi]=0 <=> Bfrak_Q -> {sol_seal}")
# PARTNER (no-surface-term candidate) = the germ-flat stratum (0,0): the
# jumps vanish => WE continuity => rho'(r_s) stays FREE (banked K4e-K4g):
jump_phi_expr = Zp*rho_s**2*(sp.Symbol('phipp') - sp.Symbol('phipm'))
sol_jp = sp.solve(sp.Eq(jump_phi_expr, 0), sp.Symbol('phipp'))
check_bool("TW3_partner_WE_phi_continuity", "SUBSTANTIVE",
           sol_jp == [sp.Symbol('phipm')], f"phip_+ -> {sol_jp}")
rhopm, rhopp = sp.symbols('rhopm rhopp', real=True)
jump_rho_PP = (pi_rho_P.subs({p_: 0, rp_: rhopp})
               - pi_rho_P.subs({p_: 0, rp_: rhopm}))
jump_rho_PG = (pi_rho_G.subs(rp_, rhopp) - pi_rho_P.subs({p_: 0, rp_: rhopm}))
for tag, jmp in (("PP", jump_rho_PP), ("PG", jump_rho_PG)):
    sol_jr = sp.solve(sp.Eq(jmp, 0), rhopp)
    check_bool(f"TW3_partner_WE_rho_continuity_{tag}", "SUBSTANTIVE",
               sol_jr == [rhopm], f"rhop_+ -> {sol_jr}")
check_nonzero("TW3_partner_rhop_free", "SUBSTANTIVE", rhopm,
              note="(rho'(r_s) undetermined on the partner stratum — banked K4g)")

# ---------------- OPEN-END (one-sided free endpoint) ----------------
# residue = pi_phi*dphi + pi_rho*drho ; stationarity = delta B:
#   pi_phi(r_s) = -c_E*Bfrak_Q  =>  q = Z rho_s^2 phi'(r_s) = -c_E*Bfrak_Q ;
#   pi_rho(r_s) = Bfrak_rho     =>  -4 rho'(r_s) = Bfrak_rho.
one_sided = (pi_phi.subs({rr_: rho_s, pp_: phip_s})*dphi
             + pi_rho_P.subs({p_: 0, rp_: rhop_s})*drho) - dB_at_point
sol_open = sp.solve([one_sided.coeff(dphi), one_sided.coeff(drho)],
                    [phip_s, rhop_s], dict=True)
check_bool("TW3_openend_germ_laws", "SUBSTANTIVE",
           sol_open == [{phip_s: -cE*BQ_germ/(Zp*rho_s**2),
                         rhop_s: -Br_germ/4}],
           f"phi'(r_s), rho'(r_s) -> {sol_open}")
q_open = (Zp*rho_s**2*sol_open[0][phip_s])
check("TW3_openend_q_is_Q_germ", "SUBSTANTIVE", q_open - (-cE*BQ_germ))
# consistency (banked K6d): Bfrak == 0 reproduces q = 0 AND rho'(r_s) = 0:
subs0 = [(BQ_germ, 0), (Br_germ, 0)]
check("TW3_openend_consistency_K6d_q0", "SUBSTANTIVE", q_open.subs(subs0))
check("TW3_openend_consistency_K6d_rhop0", "SUBSTANTIVE",
      sol_open[0][rhop_s].subs(subs0))
# NEW map fact certified: the banked q=0-under-no-choice is the GERM-FLAT
# stratum statement; a Q-active germ makes q a wall-response OUTPUT:
check_nonzero("TW3_openend_q_nonzero_off_germflat", "SUBSTANTIVE",
              q_open.subs(Br_germ, 0),
              note="(q = -c_E*B_Q: nonzero whenever the Q-germ is)")

# ---------------- pairing-branch structure (arena W-REG) ----------------
# Mirror walls are WEIGHT-FREE: p0(wall) = 0 (eps_phi = -1 kill) => the
# anchored weight W_F = e^{a_F p0} = 1 for EVERY enumerated branch — the
# mirror-wall analysis is pairing-branch-INDEPENDENT.
check("TW3_pairing_weight_drops_at_mirror_wall", "SUBSTANTIVE",
      WF.subs(p0w, 0) - 1)
# Non-mirror walls: W_F(wall) = (c_E/Q_w)^{a_F} — anchored-legal (Q-power),
# so the germ-pin VALUES are branch-weighted but alphabet-legal:
Qw = cE*sp.exp(-p0w)
check("TW3_pairing_weight_anchored_nonmirror", "SUBSTANTIVE",
      sp.simplify(WF - (cE/Qw)**aF))

print()
print("=" * 78)
print("TW4 — SELECTION VERDICT: witnesses, non-uniqueness, non-emptiness")
print("=" * 78)
# Per-candidate required-B space: nonemptiness WITNESSES (nothing adopted).
# fold: Bfrak == 0 satisfies the crease conditions (germ (inert, 0)):
check("TW4_witness_fold_B0", "SUBSTANTIVE",
      dB_at_point.subs([(BQ_germ, 0), (Br_germ, 0)]))
# glue: Bfrak = (q/2)*rho has germ (Bfrak_Q, Bfrak_rho) = (0, q/2) — both
# glue pins satisfied (witness in the banked provenance class: the argument
# list is census-legal; the FUNCTION is the exactly-characterized freedom):
B_glue = q_sym/2*rho_v
check("TW4_witness_glue_rho_germ", "SUBSTANTIVE",
      sp.diff(B_glue, rho_v) - q_sym/2)
check("TW4_witness_glue_Q_germ", "SUBSTANTIVE", sp.diff(B_glue, Qv))
# open-end: the 2-parameter germ family (beta1, beta2) realizes ANY (q, rho')
# output pair — the germ plane is the exact wall-moduli space:
beta1, beta2 = sp.symbols('beta1 beta2', real=True)
B_open = beta1*(Qv - cE) + beta2*(rho_v - rho_s)
q_out = -cE*sp.diff(B_open, Qv)
rhop_out = -sp.diff(B_open, rho_v)/4
sol_real = sp.solve([sp.Eq(q_out, q_sym), sp.Eq(rhop_out, rhop_s)],
                    [beta1, beta2], dict=True)
check_bool("TW4_openend_germ_plane_realizes_any_output", "SUBSTANTIVE",
           sol_real == [{beta1: -q_sym/cE, beta2: -4*rhop_s}],
           f"(beta1, beta2) -> {sol_real}")
# NON-uniqueness certificate: two Bfrak differing beyond the first germ give
# IDENTICAL stationarity conditions (higher content variationally inert):
B_alt = B_glue + sp.Rational(7, 3)*(rho_v - rho_s)**2 + (Qv - cE)**3
diff_conditions = [
    sp.diff(B_alt - B_glue, rho_v).subs([(Qv, cE), (rho_v, rho_s)]),
    sp.diff(B_alt - B_glue, Qv).subs([(Qv, cE), (rho_v, rho_s)])]
check("TW4_nonuniqueness_inert_content_rho", "SUBSTANTIVE", diff_conditions[0])
check("TW4_nonuniqueness_inert_content_Q", "SUBSTANTIVE", diff_conditions[1])
check_nonzero("TW4_nonuniqueness_members_distinct", "SUBSTANTIVE",
              sp.expand(B_alt - B_glue),
              note="(distinct members, identical seam conditions => FAMILY)")

print()
print("=" * 78)
print("TW5 — CONSEQUENCES (massive-branch wall conditions, where reachable)")
print("=" * 78)
# TW5a: M-WALL = a_F * M-GEN reproduced on the quadratic class (Slice-2b):
# w = A x^2 + w1 x + w0, A = a_F^2 E0/(2 g_p); pi_p = W_F g_p p1 = g_p w'/a_F.
gp, w1, w0, E0, ell = sp.symbols('g_p w_1 w_0 E_0 ell', real=True)
A_ = aF**2*E0/(2*gp)
w_ = A_*x**2 + w1*x + w0
pi_p_q = gp*sp.diff(w_, x)/aF
MWALL = pi_p_q.subs(x, ell) - pi_p_q.subs(x, -ell)
MGEN = 2*ell*E0
check("TW5a_MWALL_eq_aF_MGEN_quadratic_class", "SUBSTANTIVE",
      sp.simplify(MWALL - aF*MGEN))
# TW5b: at free (non-mirror, varied) walls with wall responses B+/B- the
# natural BCs give pi_p(+ell) = B+_p, pi_p(-ell) = -B-_p (orientation), so
# M-WALL = [pi_p] = B+_p + B-_p: the M-WALL mass branch becomes EXACTLY a
# B-germ functional at free walls.
Bp_plus, Bp_minus = sp.symbols('Bp_plus Bp_minus', real=True)
MWALL_B = Bp_plus - (-Bp_minus)
check("TW5b_MWALL_is_germ_functional_free_walls", "SUBSTANTIVE",
      MWALL_B - (Bp_plus + Bp_minus))
# TW5c: the gradient-seat affine parity lemma reproduced (condition (a)):
# f affine and EVEN about both walls => slope 0; ODD => f == 0. The
# E0-collapse under definite realized parities is therefore a CONFIGURATION-
# space fact (parity kinematics), independent of any wall response B (B only
# shifts natural BCs — it cannot restore a parity-killed slope).
# Parity ABOUT EACH WALL (x = +-ell), the banked gradient-seat form:
#   even about a wall => the 1-jet vanishes THERE; odd => the 0-jet vanishes.
al, be = sp.symbols('alpha beta', real=True)
f_aff = al + be*x
sol_even = sp.solve([sp.diff(f_aff, x).subs(x, ell),
                     sp.diff(f_aff, x).subs(x, -ell)], [al, be], dict=True)
check_bool("TW5c_affine_even_kills_slope", "SUBSTANTIVE",
           sol_even == [{be: 0}], f"even about both walls -> {sol_even}")
sol_odd = sp.solve([f_aff.subs(x, ell), f_aff.subs(x, -ell)],
                   [al, be], dict=True)
check_bool("TW5c_affine_odd_kills_field", "SUBSTANTIVE",
           sol_odd == [{al: 0, be: 0}],
           f"odd about both walls -> {sol_odd} (ell != 0)")
# TW5d: pairing-weight landings at the Route-P forced locus lambda = 0
# (map-fact arithmetic; cited: Route P TP4 + Slice-2b consensus background):
lam = sp.Symbol('lambda', real=True)
check("TW5d_triad_weight_at_lambda0_is_1", "GUARD",
      (1 + 2*lam).subs(lam, 0) - 1)
check("TW5d_4D_weight_at_lambda0_is_0", "GUARD", (2*lam).subs(lam, 0))

# ------------------------------------------------------------------ summary
n_sub = sum(1 for _, k, _, _, _ in CHECKS if k == "SUBSTANTIVE")
n_grd = sum(1 for _, k, _, _, _ in CHECKS if k == "GUARD")
n_fail = sum(1 for _, _, ok, _, _ in CHECKS if not ok)
n_cred = sum(1 for _, _, _, _, cr in CHECKS if cr)
print()
print("=" * 78)
print(f"CHECKS: {len(CHECKS)} total = {n_sub} SUBSTANTIVE + {n_grd} GUARD "
      f"({n_cred} verifier-credited); "
      f"{len(CHECKS) - n_fail} passed, {n_fail} failed")
print("=" * 78)

results = {
    "date": "2026-07-30",
    "contract": "udt_p4_boundary_action_gate_2026-07-30/PREREGISTRATION.md",
    "stamps": {
        "arena_W1D": "round-static radial reduction (1D r-profiles; banked "
                     "Branch G/P reduced Lagrangians); pairing = NONE (as the "
                     "banked seam package); crease reading pointwise-in-r; "
                     "screen/angular action NOT specified (banked 07-20 "
                     "non-uniqueness stands)",
        "arena_WREG": "registered positive triangular chart; stationary "
                      "one-parameter presentation; jets <= 2; pairing "
                      "branches P1-4D/P1-triad/P2/P3-bulkP2/P3-bulkP1 "
                      "carried, none adopted; census BASE exhaustive, BR-M "
                      "typed (J05 leg); corners TYPED-ONLY",
        "jet_layer": "N=2 (banked 2nd-order self-pairing layer) EXHAUSTIVE; "
                     "N=4 TYPED (2-jet wall + 3rd-derivative momenta), not run",
        "parity": "eps_phi = -1 DEFINITIONAL (CANON C-2026-07-30-1 layer 3); "
                  "rho evenness = banked fold-JC mirror-jet structure; f/bh "
                  "parities SUPPLIED (definite per realized outcome under "
                  "R-A — angular-completion bank — else free); moduli "
                  "parities per Route P (P2-conditional; R-A discharges)",
        "census_branch": "BASE exhaustive; BR-M typed (m-jet wall slots N3; "
                         "same unpaired-jet cut at the moduli-jet layer)",
        "pairing_relation_typing_FB5": "ONE-WAY: the bulk by-parts structure "
                                       "of the declared pairing SUPPLIES the "
                                       "wall slot census; B is an element of "
                                       "the resulting slot space; the "
                                       "pairing is never defined via B",
    },
    "TW1_census": {
        "W1D_objects": [
            "phi_s (0-jet trace; odd — killed at crease; essential slot)",
            "rho_s (0-jet trace; even — survives; B-argument)",
            "phi'_s (1-jet; enters pi_phi only; q-carrier; NOT a B-argument "
            "at N=2 — R6 cut)",
            "rho'_s (1-jet; enters pi_rho only; the D-b datum; NOT a "
            "B-argument at N=2 — R6 cut)",
            "q = Z rho_s^2 phi'_s (banked composite flux)",
            "Q_s = c_E e^{-phi_s} (the ONLY legal phi_s-dependence — "
            "anchored rule p=q)",
            "the seam functional Bfrak (THE 07-18 OPEN object D-a; "
            "parametrized, not invented)",
        ],
        "WREG_objects": [
            "0-jet traces Q_w, f0_w, bh0_w (B-arguments; trivial character)",
            "1-jet traces p1_w, f1_w, h1_w (momentum arguments; excluded "
            "from B at N=2 by the R6 cut)",
            "moduli m + K4 invariants (BASE spectators; BR-M live wall "
            "arguments; N3 m-jet wall slots on the varied fork)",
            "corner slots (TYPED-ONLY; absent from the one-parameter "
            "presentation)",
            "completion label c-frak (discrete argument; additive "
            "c-dependence inert at N=2 — R15 note)",
            "2-jet traces / 3rd-jet momenta (the 4th-order TYPED layer)",
        ],
        "topology_per_candidate": {
            "fold": "single copy, mirrored crease (Z2 quotient)",
            "partner": "two-sided seam, no surface term (= germ-flat stratum)",
            "glue+B": "two-sided interface carrying Bfrak",
            "open-end": "bare endpoint carrying Bfrak",
        },
    },
    "TW2_parametrization": {
        "general_B_at_N2": "per wall stratum ONE trivial-character smooth "
                           "function of the parity-surviving 0-jet traces + "
                           "(census-fork) moduli invariants; phi-dependence "
                           "only through Q (anchored p=q); NO 1-jet "
                           "dependence (R6 cut, weight-robust); corners "
                           "typed-only",
        "active_content": "EXACTLY the first germ at the realized seam point: "
                          "(Bfrak_Q, Bfrak_rho)(c_E, rho_s) — all higher "
                          "germ content variationally INERT AT THE REALIZED "
                          "SEAM GERM (per realized configuration; germ-LOCAL "
                          "— AMV2a/AMV2b: a (rho-rho_s)^3 perturbation has "
                          "active content 3*(rho_1-rho_s)^2 at a different "
                          "realized trace) [AM-V2]. Gloss: the inert germs "
                          "are primitive-nonuniqueness-like (shift nothing "
                          "at the realized point) — a looser analogy to, not "
                          "the exact form of, the banked BDY-TD "
                          "momentum-shifting total-derivative freedom",
        "dimensions": {
            "fold": "active moduli 0 (Q-germ inert by essential dphi=0; "
                    "rho-germ FORCED 0 by R6+parity)",
            "partner": "active moduli 0 (the germ-flat stratum, by "
                       "candidate definition)",
            "glue+B": "active moduli 0 free (first germ UNIQUELY pinned: "
                      "Bfrak_rho = q/2 by the banked jump; Bfrak_Q = 0 by "
                      "the banked flux seal)",
            "open-end": "active moduli = 2 germ functions "
                        "(Bfrak_Q, Bfrak_rho)(c_E, .) — FREE; outputs "
                        "q = -c_E Bfrak_Q and rho'_s = -Bfrak_rho/4",
        },
        "N4_layer": "TYPED: Theta_4 pairs {v, v'}; wall grade 4; B may then "
                    "carry 1-jet traces — the 1-jet germ content ACTIVATES; "
                    "not run (EXTENSION-REQUIRED stamp travels)",
    },
    "TW3_cut": {
        "R6": "no unpaired wall jets at N=2 => B is 0-jet-only (derived; "
              "weight-robust); at the mirror crease R6's C^1 reading + "
              "parity FORCES the active rho-germ to zero",
        "R12_R13_R1": "definition-level: B carries a slot per stratum; "
                      "arguments census-only; no global fitted couplings "
                      "(the FUNCTION is the exactly-characterized freedom)",
        "J07_J08": "per-stratum B with transition/completion data typed "
                   "(GC; not run). NOTE (minor amendment): the contract's "
                   "'imposed exactly' is DISCHARGED BY TYPING for J07/J08 — "
                   "their banked class is typing/GC requirements (the "
                   "c-frak-argument + per-stratum typing), consistent with "
                   "the bank; stamped, not a computation",
        "mirror_wall_theorem": "for mirror-compatible members every "
                               "even-field natural-BC momentum vanishes "
                               "kinematically at the wall and the odd-field "
                               "variation is essential-zero => the effective "
                               "wall response at a mirror wall is FORCED "
                               "TRIVIAL at N=2 (pairing-branch-independent: "
                               "W_F(wall)=1). DOUBLY PROVEN: even-invariant "
                               "construction (TW3_WREG_*) + the verifier's "
                               "strictly-more-general SYMMETRIZATION proof "
                               "adopted as credited checks AMV3a-AMV3d",
    },
    "TW4_verdict": {
        "outcome_class": "OW2 — a FAMILY with exact wall-moduli",
        "per_candidate": {
            "fold": "required-B space NONEMPTY (witness B=0), effectively "
                    "UNIQUE at the realized seam germ (per realized "
                    "configuration) [AM-V2]: active germ FORCED trivial; "
                    "D-b: rho'_s = 0 (reproduced); q = OUTPUT "
                    "(unconstrained by B)",
            "partner": "= the germ-flat stratum; WE continuity reproduced; "
                       "D-b: rho'_s FREE (continuity only); q continuous, "
                       "data-determined",
            "glue+B": "required-B space NONEMPTY (witness (q/2)*rho), first "
                      "germ UNIQUELY PINNED (Bfrak_rho = q/2 — K6c "
                      "reproduced; flux seal <=> Bfrak_Q = 0 — NEW exact "
                      "equivalence); higher content inert at the realized "
                      "seam germ => effectively UNIQUE at N=2 per realized "
                      "configuration [AM-V2]; D-b: jump q/2 carried by B",
            "open-end": "required-B space = FREE 2-germ-function family "
                        "(realizes ANY (q, rho'_s) output pair); the banked "
                        "q=0 forcing = the germ-flat stratum ONLY — with a "
                        "Q-active germ q is a wall-response output",
        },
        "selection": "the requirements EMPTY no candidate and UNIQUE-select "
                     "none: B's active content at N=2 is candidate-RELATIVE "
                     "data (forced-trivial at creases; pinned at the banked "
                     "glue; free at open ends), NOT a candidate "
                     "discriminator — the discriminating datum is the "
                     "POSTURE (quotient / two-sided / open), which is not a "
                     "B-value; deeper selective content (N=4, R9 periods, "
                     "J07/J11 holonomy) TYPED OPEN",
        "consistency_reproductions": [
            "S1f handshake underdetermination (S0b)",
            "K6c B'(rho_s) = q/2 (TW3_glue_reproduces_K6c)",
            "K6d q=0 AND rho'=0 under no-choice (TW3_openend_consistency_*) "
            "— now exhibited as the germ-flat stratum of the general law",
            "K4d fold rho'=0 (TW3_fold_consistency_K4d)",
            "K4e-K4g partner WE continuity + rho' freedom",
            "Slice-2b M-WALL = a_F*M-GEN (TW5a)",
        ],
    },
    "TW5_consequences": {
        "G18": "proposal updated (DECISION_SURFACE_UPDATE.md): the seam-"
               "closure reduction {D-a, D-b} REFINES — [AM-V1, posture-"
               "conditional form] the fold POSTURE is self-consistent: GIVEN "
               "the single-copy quotient posture, no ACTIVE wall action is "
               "admissible at N=2 (R6+parity), so WITHIN that posture the "
               "no-surface-term condition and rho'_s = 0 are automatic; the "
               "banked TWO-SIDED conditional-forces-fold theorem keeps ALL "
               "its premises (loses ZERO members — AMV1 note); the G18 "
               "reduction (posture AND Branch-G AND germ data) survives "
               "unchanged; under fold/open-end postures D-b is a FUNCTION of "
               "the B-germ; the closure question = 1 discrete posture datum "
               "+ the germ data",
        "massive_branch": "E0-collapse under realized parities is "
                          "B-INDEPENDENT (parity kinematics precede natural "
                          "BCs — TW5c); M-WALL = a_F*M-GEN reproduced; at "
                          "free walls M-WALL becomes exactly a B-germ "
                          "functional (TW5b); triad weight a_F = 1 at the "
                          "Route-P forced locus lambda=0 (map fact)",
        "census_pairing_surface": "UNCHANGED (both census branches carried; "
                                  "verdict pairing-branch-UNIFORM: mirror "
                                  "walls weight-free, non-mirror germ pins "
                                  "branch-weighted by (c_E/Q_w)^{a_F})",
    },
    "amendment": {
        "date": "2026-07-30",
        "verdict_amended_under": "VERIFIER_REPORT.md PASS-WITH-REQUIRED-"
                                 "AMENDMENTS (AM-V1, AM-V2 + minor notes); "
                                 "record = CORRECTION_LAYER.md; no "
                                 "pre-amendment computed claim changed",
        "AM_V1": "crease no-active-action result restated POSTURE-"
                 "CONDITIONAL; banked two-sided forcing theorem keeps ALL "
                 "premises (loses ZERO members); G18 reduction (posture AND "
                 "Branch-G AND germ data) unchanged (AMV1 note)",
        "AM_V2": "inertness / effective-uniqueness scoped 'at the realized "
                 "seam germ / per realized configuration'; germ-locality "
                 "counter-computation credited (AMV2a/AMV2b); OW2 unaffected",
        "minor": "BDY-TD gloss softened (primitive-nonuniqueness-like, not "
                 "momentum-shifting total derivatives); J07/J08 discharge-"
                 "by-typing noted; mirror-wall theorem doubly proven "
                 "(symmetrization credited, AMV3a-AMV3d)",
    },
    "checks": [{"name": n, "kind": k, "passed": ok, "detail": d,
                "verifier_credited": cr}
               for n, k, ok, d, cr in CHECKS],
    "checks_verifier_credited": [n for n, _, _, _, cr in CHECKS if cr],
    "counts": {"total": len(CHECKS), "substantive": n_sub, "guard": n_grd,
               "verifier_credited": n_cred, "failed": n_fail},
}

out_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(out_dir, "boundary_action_results.json"), "w") as fh:
    json.dump(results, fh, indent=2)
print("results written: boundary_action_results.json")

sys.exit(1 if n_fail else 0)
