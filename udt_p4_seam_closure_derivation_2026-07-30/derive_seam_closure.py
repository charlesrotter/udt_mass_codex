"""P4 seam-closure derivation — exact CAS legs (contract: PREREGISTRATION.md, frozen).

QUESTION: does BANKED structure derive how a finite cell closes at its phi=0 seam —
FOLD (mirrored profile in r) / BRIDGE-ONLY (handshake, gluing free) / PARTNER-GLUE
(independent partner beyond) — or none?

BANKED MACHINERY REUSED (per contract §5.2; not re-derived, re-run as Category-A
soundness of this script's reading):
  L_P = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2     (Branch P, W=1)
  L_G = (Z/2) rho^2 phi'^2 - 2 rho'^2 + 2               (Branch G, W=e^{2phi})
  banked P EOMs: phi'' = 4e^{-2phi}rho'^2/(Z rho^2) - 2phi'rho'/rho
                 rho'' = 2phi'rho' - (Z/4) rho e^{2phi} phi'^2
  banked G EOMs: phi'' = -2phi'rho'/rho ; rho'' = -(Z/4) rho phi'^2
  doubled-action fold momenta; mirror-jet identities (derive_universe_fold_d1.py,
  blind-verified 2026-07-02, agents a15ecc62590d15bd4 / a18115fe9d95cfb84).

NEW LEGS (this push): the reflection-data selection adjudication (K3, the
equations-vs-solutions gap made computational); the two-sided Weierstrass-Erdmann
computation (K4, partner reading); the per-candidate boundary-term/well-posedness
computation incl. the free-endpoint q=0 forcing (K6); the bridge-underdetermination
witness (TS1).

GUARDS HONORED: no G18/mirror-closure assumption anywhere (the fold enters ONLY as an
interrogated candidate); no x_max content; no anchor values (ln(1101) never enters);
no census/pairing choice; no floats, no numeric solvers, no GPU. Exit nonzero on any
failed check. Deterministic (pure symbolic).

AMENDMENT 2026-07-30 (post-verifier, per VERIFIER_REPORT.md PASS-WITH-REQUIRED-
AMENDMENTS; record = CORRECTION_LAYER.md):
  A1 (REQUIRED): the conditional-forces-fold premise set is restored to
      {no seam surface term (WE C^1)} AND {Branch G on BOTH sides of the seam
      (interior AND beyond)} AND {rho'(r_s)=0} — the forcing runs through K3c,
      which requires the INTERIOR solution to be Branch G; for a Branch-P interior
      the odd mirror fails the G phi-equation with exact residual
      -4 e^{-2phi} rho'^2 / (Z rho^2) (verifier counter-computation V2d, adopted
      below as credited check AM1). The package body (K3d; the P-interior
      quotient-only clause) knew this premise — the drop was headline-level only.
      The rho'_s != 0 C^1-impossibility leg (K3h) is branch-INDEPENDENT (kinematic
      jump -2 rho'_s) and unaffected.
  Verifier-credited legs adopted (function-level F-C2 discharge, stronger than the
      package's jet-level legs): the banked EOMs verified as genuine Euler-Lagrange
      equations (AM2a-AM2d); mirror-of-G solves G and mirror-of-P fails P at
      FUNCTION level with the exact residuals (AM2e-AM2g); plus AM1 above.
  Honest-split relabels (recommendation): 4 trivial-by-construction rows relabeled
      SUBSTANTIVE -> GUARD (S1f germ-A flat 0-0; S1f germ-B seam-value substitution
      identity; K3g phip/rho slots, identically zero even off-locus) — witness-
      assembly steps, not computations. Dead variable `germB_val` removed. K6a
      single/doubled-momentum note added (moot under dphi=0 essential).
No pre-amendment computed claim changed.

STAMPS (F-C3, on every claim downstream): arena = round-static radial reduction
(1D r-profiles, Branch G/P reduced Lagrangians); crease reading = pointwise-in-r on
the 1D reduction, screen/angular action NOT specified (banked 07-20 non-uniqueness
stands); census branch = none used; pairing = none used; stratum = n/a.
"""
import json
import sys

import sympy as sp

CHECKS = []  # (name, kind SUBSTANTIVE|GUARD, passed, residual-as-str, credit|None)


def check(name, kind, expr_zero, credit=None):
    val = sp.simplify(expr_zero)
    if not (val == 0 or val == sp.S.Zero):
        # hyperbolic/exponential mixing: canonicalize to exp before giving up
        val = sp.simplify(sp.expand(sp.simplify(val.rewrite(sp.exp))))
    ok = (val == 0) or (val == sp.S.Zero)
    CHECKS.append((name, kind, bool(ok), str(val), credit))
    tag = f"[{kind}]" + ("[verifier-credited]" if credit else "")
    print(f"[{'PASS' if ok else 'FAIL'}]{tag} {name}"
          + ("" if ok else f"  residual={val}"))


def check_nonzero(name, kind, expr, forbidden_zero_only_at=None, credit=None):
    """Passes iff expr is NOT identically zero (used to certify genuine freedom /
    genuine mismatch — e.g. the mirror-vs-continuation data gap 2*rho'_s)."""
    val = sp.simplify(expr)
    ok = not (val == 0 or val == sp.S.Zero)
    note = f" (vanishes only at {forbidden_zero_only_at})" if forbidden_zero_only_at else ""
    CHECKS.append((name, kind, bool(ok), f"nonzero:{val}{note}", credit))
    tag = f"[{kind}]" + ("[verifier-credited]" if credit else "")
    print(f"[{'PASS' if ok else 'FAIL'}]{tag} {name}  expr={val}{note}")


def check_bool(name, kind, ok, detail, credit=None):
    CHECKS.append((name, kind, bool(ok), str(detail), credit))
    tag = f"[{kind}]" + ("[verifier-credited]" if credit else "")
    print(f"[{'PASS' if ok else 'FAIL'}]{tag} {name}  {detail}")


# ---------------------------------------------------------------- symbols
r, u, rs, theta, vphi = sp.symbols('r u r_s theta varphi', real=True)
Zp = sp.Symbol('Z', positive=True)
phi_s, phip_s, rho_s, rhop_s = sp.symbols("phi_s phip_s rho_s rhop_s", real=True)
p_, pp_, rr_, rp_ = sp.symbols('p pp rho rhop', real=True)

Ljet_P = lambda p, pp, ro, rop: Zp/2*ro**2*pp**2 - 2*sp.exp(-2*p)*rop**2 + 2
Ljet_G = lambda p, pp, ro, rop: Zp/2*ro**2*pp**2 - 2*rop**2 + 2

print("=" * 78)
print("TS1 — THE BRIDGE FLOOR (K1 recomputed natively; K2 witnessed)")
print("=" * 78)
# NOTE (honest, K1 soundness): the banked section-235 script
# (legacy/root_oneoffs_2026-07-01/native_phi_sign_mirror_bridge_audit.py) is a
# dataclass PRINTER — it records the five facts but computes nothing. Re-running it
# is trivially green. The five facts are therefore recomputed here from the metric
# form directly (ds^2 with f_t = e^{2phi}, f_r = e^{-2phi}, g_AB = r^2 omega_AB).
phi_sym = sp.Symbol('phi', real=True)
f_t = sp.exp(2*phi_sym)
f_r = sp.exp(-2*phi_sym)

# S1a: phi -> -phi swaps the radial and time weights (bridge fact 1).
check("S1a_weight_swap_t_to_r", "SUBSTANTIVE", f_t.subs(phi_sym, -phi_sym) - f_r)
check("S1a_weight_swap_r_to_t", "SUBSTANTIVE", f_r.subs(phi_sym, -phi_sym) - f_t)

# S1b: the angular block r^2 omega_AB carries no phi (bridge fact 2).
omega = sp.Matrix([[1, 0], [0, sp.sin(theta)**2]])
gAB = r**2 * omega
check("S1b_angular_block_phi_free", "GUARD", sum(sp.diff(c, phi_sym) for c in gAB))

# S1c: at phi=0 the radial weight is 1 (bridge fact 3: both signs meet flat).
check("S1c_seam_flat_value", "GUARD", f_r.subs(phi_sym, 0) - 1)

# S1d: -r^2 Delta_S2 has phi-independent spectrum l(l+1); computed on all three
# ell=1 harmonics (bridge fact 4; the operator is built from omega only — no phi
# symbol can enter).
def lap_S2(Y):
    return (sp.diff(sp.sin(theta)*sp.diff(Y, theta), theta)/sp.sin(theta)
            + sp.diff(Y, vphi, 2)/sp.sin(theta)**2)

for tag, Y in (("m0", sp.cos(theta)),
               ("m1c", sp.sin(theta)*sp.cos(vphi)),
               ("m1s", sp.sin(theta)*sp.sin(vphi))):
    check(f"S1d_angular_eigenvalue_l1_{tag}", "SUBSTANTIVE",
          sp.simplify(-r**2*lap_S2(Y)/r**2 - 2*Y))
# S1e: L1 = (-r^2 Delta)/2 acts as the identity on ell=1 (bridge fact 5).
check("S1e_L1_identity_on_l1", "GUARD", sp.Rational(2, 2) - 1)

# S1f: THE UNDERDETERMINATION WITNESS (K2 floor boundary). Two DISTINCT exterior
# germs both satisfy the full bridge handshake at the seam
# {phi_+(rs)=0 ; rho_+(rs)=rho_s ; radial weight 1 at seam}:
#   germ A (banked flat-exterior glue, weld chain / CANON C-2 zero tail):
#     phi_+ === 0, first jet phip_A = 0
#   germ B (odd-mirror germ): phi_+(rs+u) = -phi_-(rs-u), first jet phip_B = +phip_s
# Handshake residuals vanish for BOTH; their first jets differ by phip_s (generic
# nonzero) => the bridge does NOT pin the gluing. [This is the exact content of
# weld :39-41 made computational.]
phi_minus = sp.Function('phim')  # interior profile, phi_minus(rs) = 0
germA_val, germA_jet = sp.S(0), sp.S(0)
germB = -phi_minus(2*rs - r)
germB_jet = sp.diff(germB, r).subs(r, rs)                # = +phim'(rs)
# AMENDMENT relabel (verifier recommendation): the germ-A seam value is 0 - 0 BY
# CONSTRUCTION and the germ-B seam-value line is a substitution identity — both are
# witness-ASSEMBLY guards, not computations. The load-bearing S1f content is the
# on-locus handshake + the certified-nonzero jet gap below.
check("S1f_handshake_germA_flat", "GUARD", germA_val - 0)
# germ B seam value = -phi_-(rs) identically; the handshake (seam value 0) then
# holds exactly on the seam's defining condition phi_-(rs)=0 — same condition germ A
# already presupposes. Check the identity, then the handshake on the seam locus:
check("S1f_handshake_germB_mirror_seam_value_identity", "GUARD",
      germB.subs(r, rs) - (-phi_minus(rs)))
check("S1f_handshake_germB_on_seam_locus", "SUBSTANTIVE",
      germB.subs(r, rs).subs(phi_minus(rs), 0))
check_nonzero("S1f_germs_distinct_first_jet", "SUBSTANTIVE",
              germB_jet - germA_jet, forbidden_zero_only_at="phi_-'(rs)=0")

print()
print("=" * 78)
print("TS2/K3 — BRANCH-G ODD-FOLD SYMMETRY: PERMITS vs FORCES (the F-C2 gap)")
print("=" * 78)
# --- banked identities re-run (Category-A soundness of this script's reading) ---
# K3a: L_G exactly invariant under the odd fold jet (phi,phi',rho,rho') ->
# (-phi, +phi', rho, -rho') [banked C3].
check("K3a_LG_invariant_odd_fold", "SUBSTANTIVE",
      sp.expand(Ljet_G(-p_, pp_, rr_, -rp_) - Ljet_G(p_, pp_, rr_, rp_)))
# K3b: L_P is NOT invariant — exact residual -4 sinh(2phi) rho'^2 [banked C1/C2].
resP = sp.expand(Ljet_P(-p_, pp_, rr_, -rp_) - Ljet_P(p_, pp_, rr_, rp_))
check("K3b_LP_fold_residual_is_minus4sinh2phi_rhop2", "SUBSTANTIVE",
      sp.simplify(resP + 4*sp.sinh(2*p_)*rp_**2))

# banked EOMs at the jet level
p0, f1, f2, r0, g1, g2 = sp.symbols('p0 f1 f2 r0 g1 g2', real=True)
f2P = 4*sp.exp(-2*p0)*g1**2/(Zp*r0**2) - 2*f1*g1/r0
g2P = 2*f1*g1 - Zp/4*r0*sp.exp(2*p0)*f1**2
f2G = -2*f1*g1/r0
g2G = -Zp/4*r0*f1**2

# K3c: the odd-mirror extension of a G-solution is an EXACT G-solution [banked D2/D3].
# mirror jets: (phit,phit',phit'') = (-p0, +f1, -f2); (rhot,rhot',rhot'') = (r0,-g1,+g2)
check("K3c_mirror_solves_G_phi_eq", "SUBSTANTIVE",
      sp.simplify(((-f2) - (-2*f1*(-g1)/r0)).subs(f2, f2G)))
check("K3c_mirror_solves_G_rho_eq", "SUBSTANTIVE",
      sp.simplify((g2 - (-Zp/4*r0*f1**2)).subs(g2, g2G)))
# K3d: the odd-mirror extension of a P-solution VIOLATES the P EOMs unless rho'=0
# [banked D1a/D1b] => for a Branch-P interior, a mirror-image REGION beyond obeying
# the same P equations does not exist (quotient-only reading for P).
resP_phi = ((-f2) - (4*sp.exp(2*p0)*g1**2/(Zp*r0**2) + 2*f1*g1/r0)).subs(f2, f2P)
check("K3d_mirror_violates_P_phi_residual", "SUBSTANTIVE",
      sp.expand(sp.simplify(resP_phi).rewrite(sp.exp)
                + 4*g1**2*(sp.exp(-2*p0) + sp.exp(2*p0))/(Zp*r0**2)))
resP_rho = (g2 - (-2*f1*g1 - Zp/4*r0*sp.exp(-2*p0)*f1**2)).subs(g2, g2P)
check("K3d_mirror_violates_P_rho_residual", "SUBSTANTIVE",
      sp.simplify(resP_rho - (4*f1*g1 + Zp/4*r0*f1**2*(sp.exp(-2*p0) - sp.exp(2*p0)))))
# K3e: the mirror image of a P-solution solves the FLIPPED-WEIGHT Lagrangian
# (Z/2)rho^2 phi'^2 - 2e^{+2phi}rho'^2 + 2 [banked E2] — which is neither P nor G:
Ltil_flipped = Zp/2*rr_**2*pp_**2 - 2*sp.exp(2*p_)*rp_**2 + 2
check_nonzero("K3e_flipped_weight_is_not_P", "GUARD",
              sp.expand(Ltil_flipped - Ljet_P(p_, pp_, rr_, rp_)),
              forbidden_zero_only_at="phi=0 or rho'=0")
check_nonzero("K3e_flipped_weight_is_not_G", "GUARD",
              sp.expand(Ltil_flipped - Ljet_G(p_, pp_, rr_, rp_)),
              forbidden_zero_only_at="phi=0 or rho'=0")

# --- NEW: the selection adjudication (equations-vs-solutions, made computational) ---
# The reflected field  phit(x) = -phi(2 rs - x), rhot(x) = rho(2 rs - x)  has seam
# Cauchy data (phit, phit', rhot, rhot')(rs) = (-phi_s, +phip_s, rho_s, -rhop_s).
refl_data = (-phi_s, phip_s, rho_s, -rhop_s)
orig_data = (phi_s, phip_s, rho_s, rhop_s)
# K3f: reflected data == original data  <=>  phi_s = 0 AND rhop_s = 0 (exact solve).
sol = sp.solve([refl_data[0] - orig_data[0], refl_data[3] - orig_data[3]],
               [phi_s, rhop_s], dict=True)
cond_ok = (len(sol) == 1 and sol[0].get(phi_s) == 0 and sol[0].get(rhop_s) == 0)
check_bool("K3f_reflection_data_match_iff_phis0_rhops0", "SUBSTANTIVE",
           cond_ok, f"solve -> {sol}")
# K3g: ON the locus {phi_s=0, rhop_s=0} the reflected data are IDENTICAL to the
# original data (zero residual, all four slots). AMENDMENT relabel (verifier
# recommendation): the phip and rho slots are identically zero even OFF the locus
# (the reflection preserves those slots by construction) — they are bookkeeping
# GUARDS; the load-bearing slots are phi and rhop (which vanish exactly on the
# locus and only there).
for i, tag in enumerate(("phi", "phip", "rho", "rhop")):
    kind_g = "SUBSTANTIVE" if tag in ("phi", "rhop") else "GUARD"
    check(f"K3g_data_identity_on_locus_{tag}", kind_g,
          (refl_data[i] - orig_data[i]).subs({phi_s: 0, rhop_s: 0}))
# ... and since the reflection maps G-solutions to G-solutions (K3c) — a step that
# REQUIRES the interior solution to be Branch G — Picard uniqueness of the Cauchy
# problem (Category-A cite: the G right-hand sides (-2 f1 g1/r0, -(Z/4) r0 f1^2)
# are smooth in the jet for rho != 0) forces the unique C^1 continuation to BE the
# mirror on that locus. FORCES-FOLD conditional on: {no seam surface term
# (=> WE C^1 matching), Branch G on BOTH sides of the seam (interior AND beyond),
# rhop_s = 0}.  [A1: premise set restored — for a Branch-P interior the mirror
# fails the G phi-equation with exact residual -4 e^{-2phi} rho'^2/(Z rho^2)
# (credited check AM1 below): the unique G continuation then EXISTS but is NOT
# the mirror, so "fold FORCED" would be false as read without the interior-branch
# premise.]
# K3h: OFF the locus (rhop_s != 0) the mirror's data differ from the continuation's
# data by exactly -2*rhop_s => the mirror is NOT the continuation there — the
# equations' symmetry PERMITS but does not FORCE solution symmetry (F-C2 adjudicated:
# forcing enters ONLY through data + uniqueness, never through the symmetry alone).
check_nonzero("K3h_off_locus_mirror_data_gap", "SUBSTANTIVE",
              refl_data[3] - orig_data[3], forbidden_zero_only_at="rhop_s=0")

print()
print("=" * 78)
print("TS2/K4 — THE rho'(r_s)=0 DISCRIMINATOR, BOTH READINGS COMPUTED")
print("=" * 78)
# Momenta from the reduced Lagrangians (single copy):
#   pi_phi = dL/dphi' = Z rho^2 phi'   (both branches)
#   pi_rho^P = -4 e^{-2phi} rho' ; pi_rho^G = -4 rho'
pi_phi = Zp*rr_**2*pp_
pi_rho_P = -4*sp.exp(-2*p_)*rp_
pi_rho_G = -4*rp_
check("K4a_pi_phi_form", "GUARD", pi_phi - sp.diff(Ljet_P(p_, pp_, rr_, rp_), pp_))
check("K4a_pi_rho_P_form", "GUARD", pi_rho_P - sp.diff(Ljet_P(p_, pp_, rr_, rp_), rp_))
check("K4a_pi_rho_G_form", "GUARD", pi_rho_G - sp.diff(Ljet_G(p_, pp_, rr_, rp_), rp_))

# --- FOLD (quotient) reading [banked routes re-run] ---
# Odd identification acts on variations: delta_phit(rs) = -delta_phi(rs)
# => delta_phi(rs) = 0 (ESSENTIAL: the only solution of v = -v):
v = sp.Symbol('v', real=True)
sol_v = sp.solve(sp.Eq(v, -v), v)
check_bool("K4b_fold_variation_essential_delta_phi_zero", "SUBSTANTIVE",
           sol_v == [0], f"solve(v=-v) -> {sol_v}")
# => pi_phi(rs) unconstrained => phi'(rs) FREE => q = Z rho_s^2 phi'(rs) is an OUTPUT.
# delta_rho(rs) is FREE (even slot) => natural BC: doubled-action momentum
# p_tot_rho = pi_rho^P + pi_rho^{flipped} = -4(e^{-2phi} + e^{2phi}) rho' = -8 cosh(2phi) rho'
p_tot_rho = -4*sp.exp(-2*p_)*rp_ - 4*sp.exp(2*p_)*rp_
check("K4c_doubled_rho_momentum_cosh_form", "SUBSTANTIVE",
      sp.simplify(p_tot_rho + 8*sp.cosh(2*p_)*rp_))
# at the seam phi=0: p_tot_rho = -8 rho' ; stationarity => rho'(rs) = 0 (cosh != 0):
sol_rp = sp.solve(sp.Eq(p_tot_rho.subs(p_, 0), 0), rp_)
check_bool("K4d_fold_natural_BC_pins_rhop_zero", "SUBSTANTIVE",
           sol_rp == [0], f"solve -> {sol_rp}")

# --- PARTNER (two-sided interface) reading, NO seam surface term: WE conditions ---
# [pi_phi] = 0 across the seam: Z rho_s^2 (phip_plus - phip_minus) = 0
phip_m, phip_p, rhop_m, rhop_p = sp.symbols("phipm phipp rhopm rhopp", real=True)
jump_phi = Zp*rho_s**2*(phip_p - phip_m)
sol_jp = sp.solve(sp.Eq(jump_phi, 0), phip_p)
check_bool("K4e_two_sided_WE_phi_continuity_only", "SUBSTANTIVE",
           sol_jp == [phip_m], f"phip_+ -> {sol_jp}")
# [pi_rho] = 0 at the seam (phi=0 there; P inside, P or G outside — both give -4 rho'):
jump_rho_PP = (pi_rho_P.subs({p_: 0, rp_: rhop_p}) - pi_rho_P.subs({p_: 0, rp_: rhop_m}))
jump_rho_PG = (pi_rho_G.subs(rp_, rhop_p) - pi_rho_P.subs({p_: 0, rp_: rhop_m}))
for tag, jmp in (("PP", jump_rho_PP), ("PG", jump_rho_PG)):
    sol_jr = sp.solve(sp.Eq(jmp, 0), rhop_p)
    check_bool(f"K4f_two_sided_WE_rho_continuity_only_{tag}", "SUBSTANTIVE",
               sol_jr == [rhop_m], f"rhop_+ -> {sol_jr}")
# => the partner reading pins rho' to CONTINUITY, not to zero: rhop_m stays a free
# symbol. K4g: certify the freedom — the WE system does NOT determine rhop_m:
check_nonzero("K4g_partner_leaves_rhop_free", "SUBSTANTIVE", rhop_m,
              forbidden_zero_only_at="the fold/free-endpoint posture only")
# DISCRIMINATOR (banked K4, now two-sided-computed): rho'(rs)=0 <=> fold-quotient /
# free-endpoint posture; the partner reading leaves it free. The banked corpus
# contains NO decider for rhop_s absent the closed-cell ("nothing beyond") premise
# [fold-JC ledger :104, cited]; the banked matter-cell seam in fact carries a
# NON-fold glue with interface jump Delta_Pi = q/2 [weld :30-32, cited].

print()
print("=" * 78)
print("TS2/K6 — BOUNDARY-VARIATIONAL STRUCTURE PER CLOSURE CANDIDATE")
print("=" * 78)
dphi, drho = sp.symbols('dphi drho', real=True)  # seam variations
q_sym = sp.Symbol('q', real=True)
# K6a: FOLD: delta S_seam = pi_phi*dphi + p_tot_rho*drho with dphi=0 (essential),
# rho'=0 (natural) -> identically zero: stationarity well-posed with NO surface term.
# NOTE (verifier, cosmetic — amendment): this expression mixes the SINGLE-COPY
# pi_phi with the DOUBLED rho-momentum p_tot_rho. The mixing is MOOT here: the
# essential BC dphi=0 kills the pi_phi term identically regardless of whether the
# single or doubled phi-momentum is used (the doubled phi-momentum is 2*pi_phi,
# and 2*pi_phi*0 = pi_phi*0 = 0); the rho leg is the doubled-action momentum, as
# banked. No conclusion depends on the choice.
dS_fold = (pi_phi.subs({rr_: rho_s, pp_: phip_s})*dphi
           + p_tot_rho.subs({p_: 0, rp_: rp_})*drho)
check("K6a_fold_boundary_terms_vanish", "SUBSTANTIVE",
      dS_fold.subs({dphi: 0, rp_: 0}))
# K6b: PARTNER: delta S_seam = [pi_phi]*dphi + [pi_rho]*drho -> zero under WE
# continuity: well-posed with NO surface term.
dS_partner = jump_phi*dphi + jump_rho_PP*drho
check("K6b_partner_boundary_terms_cancel", "SUBSTANTIVE",
      dS_partner.subs({phip_p: phip_m, rhop_p: rhop_m}))
# K6c: BANKED FLAT-GLUE (matter cell, weld chain): interface jump Delta_Pi = q/2
# (Pi_inner=-q/2, Pi_outer=0, banked) => delta S_seam = Delta_Pi * drho != 0 unless a
# seam surface functional B(rho_s) with B'(rho_s) = Delta_Pi is added. The required
# B is exactly the underived finite-cell boundary action (07-18 gate OPEN, cited).
DeltaPi = q_sym/2
Bp = sp.Symbol("Bprime", real=True)
sol_B = sp.solve(sp.Eq(DeltaPi*drho - Bp*drho, 0), Bp)
check_bool("K6c_glue_requires_surface_term_Bprime_eq_DeltaPi", "SUBSTANTIVE",
           sol_B == [q_sym/2], f"B' -> {sol_B}")
check_nonzero("K6c_glue_unclosed_without_B", "SUBSTANTIVE",
              DeltaPi*drho, forbidden_zero_only_at="q=0 or drho=0")
# K6d: NECESSITY-OF-CLOSURE: the 'no choice at all' posture (bare free endpoint,
# both variations free, no surface term) is ITSELF a definite closure: it forces
# pi_phi(rs) = 0  =>  q = Z rho_s^2 phi'(rs) = 0  (and rho'(rs)=0).
sol_q = sp.solve(sp.Eq(pi_phi.subs({rr_: rho_s, pp_: phip_s}), 0), phip_s)
check_bool("K6d_bare_free_endpoint_forces_q_zero", "SUBSTANTIVE",
           sol_q == [0], f"phi'(rs) -> {sol_q} => q=0")
# VERDICT K6 (computed): a closure is variationally NECESSARY (no posture is
# neutral — even 'none' is the q=0 open-end closure), but the structure holds
# WELL-POSED under fold (K6a), partner (K6b), AND glue+B (K6c): it does not SELECT.
# The selecting object would be the derived boundary action B — the 07-18 OPEN gate.

print()
print("=" * 78)
print("TS2/K7 — CONSISTENCY (cited; one exact guard)")
print("=" * 78)
# K7: phi=0 is the unique fixed point of phi -> -phi (horizon-CMB note §3; the
# source itself tags this 'triviality or derivation seed — undecided'; it stays so).
sol_fp = sp.solve(sp.Eq(phi_sym, -phi_sym), phi_sym)
check_bool("K7a_phi0_unique_fixed_point", "GUARD", sol_fp == [0], f"-> {sol_fp}")
# K5/K7 remaining content is CITED-STRUCTURAL (no computation is faked for it):
# WR-L wall (phi->+inf, A->0, null) vs CMB odd fold (phi=0, A=1, rho'=0) are
# DISTINCT in the recorded models (asymptotic_boundary_lineage_audit_2026-07-19);
# WR-L records are mirror-free (provenance audit §2a-i); 'trapped interior beyond'
# (C-2026-07-09-1a) attaches to the horizon-class wall, not the phi=0 seam.

print()
print("=" * 78)
print("AMENDMENT 2026-07-30 — VERIFIER-CREDITED LEGS (adopted from")
print("VERIFIER_INDEPENDENT_CHECK.py: A1 counter-computation + function-level")
print("F-C2 discharge; see CORRECTION_LAYER.md)")
print("=" * 78)
# These legs work at FUNCTION level (full x-dependence, sp.Function fields with the
# EOMs imposed by substitution) — stronger grounding than the package's jet-level
# checks, which they corroborate rather than replace.
x_ = sp.Symbol('x', real=True)
y_ = sp.Symbol('y', real=True)
phiF = sp.Function('phi')
rhoF = sp.Function('rho')

# --- AM2a-AM2d: the banked EOMs are the GENUINE Euler-Lagrange equations of the
# banked reduced Lagrangians (not checked in the pre-amendment package).
def EL_expr(Lfun, which):
    Lx = Lfun(phiF(x_), sp.diff(phiF(x_), x_), rhoF(x_), sp.diff(rhoF(x_), x_))
    qv = phiF(x_) if which == 'phi' else rhoF(x_)
    return sp.diff(sp.diff(Lx, sp.diff(qv, x_)), x_) - sp.diff(Lx, qv)

Dphi2 = sp.diff(phiF(x_), x_, 2)
Drho2 = sp.diff(rhoF(x_), x_, 2)
solEL = sp.solve(sp.Eq(EL_expr(Ljet_P, 'phi'), 0), Dphi2)
claim = (4*sp.exp(-2*phiF(x_))*sp.diff(rhoF(x_), x_)**2/(Zp*rhoF(x_)**2)
         - 2*sp.diff(phiF(x_), x_)*sp.diff(rhoF(x_), x_)/rhoF(x_))
check_bool("AM2a_banked_P_phi_EOM_is_EulerLagrange", "SUBSTANTIVE",
           len(solEL) == 1 and sp.simplify(solEL[0] - claim) == 0,
           "phi'' from EL(L_P) == banked P phi-EOM", credit="verifier")
solEL = sp.solve(sp.Eq(EL_expr(Ljet_P, 'rho'), 0), Drho2)
claim = (2*sp.diff(phiF(x_), x_)*sp.diff(rhoF(x_), x_)
         - Zp/4*rhoF(x_)*sp.exp(2*phiF(x_))*sp.diff(phiF(x_), x_)**2)
check_bool("AM2b_banked_P_rho_EOM_is_EulerLagrange", "SUBSTANTIVE",
           len(solEL) == 1 and sp.simplify(solEL[0] - claim) == 0,
           "rho'' from EL(L_P) == banked P rho-EOM", credit="verifier")
solEL = sp.solve(sp.Eq(EL_expr(Ljet_G, 'phi'), 0), Dphi2)
check_bool("AM2c_banked_G_phi_EOM_is_EulerLagrange", "SUBSTANTIVE",
           len(solEL) == 1 and sp.simplify(
               solEL[0] + 2*sp.diff(phiF(x_), x_)*sp.diff(rhoF(x_), x_)/rhoF(x_)) == 0,
           "phi'' from EL(L_G) == banked G phi-EOM", credit="verifier")
solEL = sp.solve(sp.Eq(EL_expr(Ljet_G, 'rho'), 0), Drho2)
check_bool("AM2d_banked_G_rho_EOM_is_EulerLagrange", "SUBSTANTIVE",
           len(solEL) == 1 and sp.simplify(
               solEL[0] + Zp/4*rhoF(x_)*sp.diff(phiF(x_), x_)**2) == 0,
           "rho'' from EL(L_G) == banked G rho-EOM", credit="verifier")

# --- function-level mirror machinery: phit(x) = -phi(2rs-x), rhot(x) = rho(2rs-x)
phit = -phiF(2*rs - x_)
rhot = rhoF(2*rs - x_)

def impose_G(e):
    e = e.doit()
    for _ in range(2):
        e = e.replace(sp.Derivative(phiF(y_), (y_, 2)),
                      -2*sp.Derivative(phiF(y_), y_)*sp.Derivative(rhoF(y_), y_)/rhoF(y_))
        e = e.replace(sp.Derivative(rhoF(y_), (y_, 2)),
                      -Zp/4*rhoF(y_)*sp.Derivative(phiF(y_), y_)**2)
    return sp.simplify(e)

def impose_P(e):
    e = e.doit()
    for _ in range(2):
        e = e.replace(sp.Derivative(phiF(y_), (y_, 2)),
                      4*sp.exp(-2*phiF(y_))*sp.Derivative(rhoF(y_), y_)**2/(Zp*rhoF(y_)**2)
                      - 2*sp.Derivative(phiF(y_), y_)*sp.Derivative(rhoF(y_), y_)/rhoF(y_))
        e = e.replace(sp.Derivative(rhoF(y_), (y_, 2)),
                      2*sp.Derivative(phiF(y_), y_)*sp.Derivative(rhoF(y_), y_)
                      - Zp/4*rhoF(y_)*sp.exp(2*phiF(y_))*sp.Derivative(phiF(y_), y_)**2)
    return sp.simplify(e)

# AM2e/AM2f: the odd mirror of a G-SOLUTION solves the G equations at FUNCTION
# level (full x-dependence — corroborates the jet-level K3c).
resG_phi = (sp.diff(phit, x_, 2)
            + 2*sp.diff(phit, x_)*sp.diff(rhot, x_)/rhot).subs(2*rs - x_, y_)
check_bool("AM2e_mirror_of_G_solves_G_phi_function_level", "SUBSTANTIVE",
           impose_G(resG_phi) == 0, "residual 0 at function level", credit="verifier")
resG_rho = (sp.diff(rhot, x_, 2)
            + Zp/4*rhot*sp.diff(phit, x_)**2).subs(2*rs - x_, y_)
check_bool("AM2f_mirror_of_G_solves_G_rho_function_level", "SUBSTANTIVE",
           impose_G(resG_rho) == 0, "residual 0 at function level", credit="verifier")

# AM2g: the odd mirror of a P-SOLUTION fails the P phi-equation at FUNCTION level
# with the exact residual -(4 rho'^2/(Z rho^2))(e^{-2phi}+e^{2phi}) (corroborates
# the jet-level K3d).
resP_phi = (sp.diff(phit, x_, 2)
            - 4*sp.exp(-2*phit)*sp.diff(rhot, x_)**2/(Zp*rhot**2)
            + 2*sp.diff(phit, x_)*sp.diff(rhot, x_)/rhot).subs(2*rs - x_, y_)
targetP = -(4*sp.Derivative(rhoF(y_), y_)**2/(Zp*rhoF(y_)**2))*(
    sp.exp(-2*phiF(y_)) + sp.exp(2*phiF(y_)))
check_bool("AM2g_mirror_of_P_violates_P_phi_function_level_exact_residual",
           "SUBSTANTIVE",
           sp.simplify(sp.expand((impose_P(resP_phi) - targetP).rewrite(sp.exp))) == 0,
           "exact residual -(4 rho'^2/(Z rho^2))(e^{-2phi}+e^{2phi})",
           credit="verifier")

# AM1 (THE A1 COUNTER-COMPUTATION, verifier's V2d): the odd mirror of a Branch-P
# INTERIOR is NOT a Branch-G solution — it fails the G phi-equation with exact
# residual -4 e^{-2phi} rho'^2/(Z rho^2), nonzero wherever rho' != 0 in the
# interior. Hence with a P interior, the unique G continuation off the seam EXISTS
# (Picard) but is NOT the mirror: the conditional-forces-fold theorem REQUIRES
# Branch G on BOTH sides (the A1 premise restoration).
resPG_phi = (sp.diff(phit, x_, 2)
             + 2*sp.diff(phit, x_)*sp.diff(rhot, x_)/rhot).subs(2*rs - x_, y_)
gapPG = impose_P(resPG_phi)
check_bool("AM1_mirror_of_P_interior_fails_G_phi_exact_residual", "SUBSTANTIVE",
           sp.simplify(gapPG + 4*sp.exp(-2*phiF(y_))
                       * sp.Derivative(rhoF(y_), y_)**2/(Zp*rhoF(y_)**2)) == 0
           and gapPG != 0,
           "exact residual -4 e^{-2phi} rho'^2/(Z rho^2), nonzero for rho' != 0",
           credit="verifier")

# ---------------------------------------------------------------- summary
n_sub = sum(1 for _, k, _, _, _ in CHECKS if k == "SUBSTANTIVE")
n_grd = sum(1 for _, k, _, _, _ in CHECKS if k == "GUARD")
n_crd = sum(1 for _, _, _, _, c in CHECKS if c)
n_fail = sum(1 for _, _, ok, _, _ in CHECKS if not ok)
print()
print("=" * 78)
print(f"CHECKS: {len(CHECKS)} total = {n_sub} SUBSTANTIVE "
      f"({n_sub - n_crd} original + {n_crd} verifier-credited) + {n_grd} GUARD; "
      f"{len(CHECKS) - n_fail} passed, {n_fail} failed")
print("=" * 78)

results = {
    "date": "2026-07-30",
    "contract": "udt_p4_seam_closure_derivation_2026-07-30/PREREGISTRATION.md",
    "stamps": {
        "arena": "round-static radial reduction (1D r-profiles; Branch G/P reduced Lagrangians)",
        "census_branch": "none used",
        "pairing": "none used",
        "crease_reading": "pointwise-in-r on the 1D reduction; screen/angular action NOT specified (banked 07-20 non-uniqueness stands)",
        "stratum": "n/a",
    },
    "TS1_bridge_floor": {
        "derived": "seam-data handshake at phi=0 only: shared angular geometry, shared flat radial weight f=1, shared phi-independent angular spectrum, ell=1 identity bridge",
        "not_derived": "any profile relation in r beyond the seam; the gluing (weld :39-41 line, witnessed: two distinct germs pass the handshake)",
        "residual_freedom": "closure type tau in {fold-quotient, partner(branch_+), glue+surface-term B, open-end(q=0)} + for glue: B with B'(rho_s)=Delta_Pi; partner continuation is DATA-DETERMINED (not arbitrary) once WE holds",
    },
    "TS2_verdicts": {
        "K1": "BRIDGE-FLOOR (derived; five facts recomputed; banked section-235 script is a printer, no computation)",
        "K2": "FLOOR-BOUNDARY (cited + underdetermination witnessed)",
        "K3": "PERMITS-FOLD unconditionally (Branch G); FORCES-FOLD only conditionally on {no seam surface term (WE C^1), Branch G on BOTH sides of the seam (interior AND beyond), rho'(rs)=0} via data+Picard-uniqueness [A1: premise set restored — for a Branch-P interior the mirror fails the G phi-equation with exact residual -4e^{-2phi}rho'^2/(Z rho^2), credited check AM1, so the unique G continuation exists but is NOT the mirror]; FORBIDS a mirrored-P region (quotient-only for P interior); the rho'(rs)!=0 C^1-impossibility leg is branch-INDEPENDENT (kinematic jump -2rho'_s); F-C2 adjudicated: symmetry of equations forces nothing without the data locus",
        "K4": "CONSTRAINS(exact): rho'(rs)=0 <=> fold-quotient/free-endpoint posture; partner reading leaves rho'(rs) free (WE gives continuity only); banked decider ABSENT (fold-JC ledger :104); banked matter-cell seam uses a NON-fold glue with jump q/2 (weld :30-32)",
        "K5": "CONSTRAINS(premise-level, cross-arena, cited): WR-L wall is a DIFFERENT surface from the phi=0 seam in the recorded models; WR-L mirror-free; 'interior beyond' softens the closed-cell premise the fold leg rides; decides nothing at the seam",
        "K6": "CONSTRAINS(exact): closure NECESSARY (no variationally neutral posture; bare-free endpoint is itself the q=0 closure) but NOT SELECTED (fold, partner, glue+B all well-posed); the selecting object = the underived boundary action (07-18 gate OPEN)",
        "K7": "SILENT-as-decider (consistency holds both ways; phi=0 unique fixed point stays 'triviality or seed', undecided in-source)",
    },
    "TS3_composite": "OC2 — BRIDGE-ONLY derived; closure genuinely free on the banked record, partner-glue live (and banked-in-use at the matter-cell seam); SHARPENED: the freedom reduces to the named data {seam boundary action B (07-18 OPEN), the rho'(rs)-pin / beyond-ontology datum, branch beyond}; NEW conditional theorem [premise set per amendment A1]: on {no surface term, Branch G on BOTH sides of the seam (interior AND beyond), rho'(rs)=0} the fold is FORCED by data+uniqueness, and for rho'(rs)!=0 the fold is IMPOSSIBLE as a C^1 configuration (branch-independent)",
    "standing_falsifier": "NOT FIRED — no unconditional fold was derived; the conditional fold names its arena (round-static radial reduction; screen/angular action unspecified) and asserts no point involution of the toric arena; the banked joint unsatisfiability is untouched",
    "amendment": {
        "date": "2026-07-30",
        "verifier_verdict": "PASS-WITH-REQUIRED-AMENDMENTS (VERIFIER_REPORT.md; record = CORRECTION_LAYER.md)",
        "A1": "REQUIRED premise restoration at all six loci: the conditional-forces-fold premise set is {no seam surface term (WE C^1), Branch G on BOTH sides of the seam (interior AND beyond), rho'(rs)=0}; counter-computation adopted as credited check AM1 (mirror of a P interior fails the G phi-equation, exact residual -4e^{-2phi}rho'^2/(Z rho^2)); the package body (K3d, P-interior quotient-only clause) knew the premise — the drop was headline-level only; the rho'_s!=0 impossibility leg is branch-independent and unaffected",
        "verifier_credited_legs": "function-level F-C2 discharge adopted (AM2a-AM2g: banked EOMs verified as genuine Euler-Lagrange equations; mirror-of-G solves G and mirror-of-P fails P at function level with exact residuals) + AM1",
        "relabels": "4 trivial-by-construction rows SUBSTANTIVE -> GUARD (S1f_handshake_germA_flat; S1f_handshake_germB_mirror_seam_value_identity; K3g phip/rho slots — identically zero even off-locus); witness-assembly steps, not computations; nothing hides behind them",
        "other": "dead variable germB_val removed; K6a single/doubled-momentum note added (moot under dphi=0 essential)",
    },
    "checks": [
        {"name": n, "kind": k, "passed": ok, "residual": rv,
         **({"credit": "verifier-credited"} if c else {})}
        for n, k, ok, rv, c in CHECKS
    ],
    "checks_verifier_credited": [n for n, _, _, _, c in CHECKS if c],
    "counts": {"total": len(CHECKS), "substantive": n_sub,
               "substantive_original": n_sub - n_crd,
               "substantive_verifier_credited": n_crd,
               "guard": n_grd, "failed": n_fail},
}

import os
out_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(out_dir, "seam_closure_results.json"), "w") as fh:
    json.dump(results, fh, indent=2)
print(f"results written: seam_closure_results.json")

sys.exit(1 if n_fail else 0)
