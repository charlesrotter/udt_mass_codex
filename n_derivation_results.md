# Deriving n = W_ff — Results

Status: working audit, not canonical. Created: 2026-06-11. Follows
sourced_second_jet_results.md (which left n = W_ff as the single
unknown of the second-jet sector). Process: three data-blind
derivation agents (N1 responsive elimination, N2 gluing/canonical,
N3 nonstationary weld), then two blind adversarial verifiers (VA:
dedicated adjudication of an N1-vs-N3 contradiction, 18+1 checks;
VB: structural claims, ~45 checks, 41 PASS / 4 FAIL all in one
claim-cluster). New files only.

## Headline

n IS DERIVED — AND IT IS NOT A CONSTANT. The verified answer: in the
native responsive reading (the source = the metric's own ell=1 angular
activity), the dilation response W_ff is a channel-resolved,
scale-dependent kernel whose quasi-static character is the n = 1
family to 0.7% (exact pointwise screening + a small positive nonlocal
lifting, rigorously bounded). THE BANKED WELD VALUE n = 0 IS ATTAINED
NOWHERE — no channel, no depth, no probe regime produces the constant
mass 2s (refuted by a factor >= 140 in mu). Independently, it is
PROVEN that no kinematic or consistency structure could ever have
fixed n: the entire second-order static sector (gluing, conservation,
canonical/distributional structure) is slot-covariant — n is a
connection choice on the configuration line, suppliable only by the
source's own dynamics, which have now supplied it.

## The adjudicated contradiction (VA)

N1 claimed total static screening => the n = 1 family; N3 claimed
n_eff(omega->0) = 0 exactly => "the banked n = 0 is derived." VA
resolved this as a BASELINE BOOKKEEPING DISPUTE with no mathematical
disagreement: N3's "induced kernel" subtracted the static screening
before measuring it (any kernel minus its static value vanishes
statically), and its map assigned the residual dispersion to the
n-slot although the banked 2s never appears in the responsive class's
bare operator at all. Correctly booked, N3's own computation CONFIRMS
N1's screening. VA's own from-scratch computation (P1-FEM nonlocal
Schur, grid/BC-robust, two domains + independent symbolic
Born-Oppenheimer reduction):
- Pointwise static screening EXACT (rank-1 null argument,
  nonperturbative — survives any responder-class extension).
- Radial-inclusive lifting: 0 < mu_eff <= mu_BO = 3 y^2 kappa'^2 /
  (3 + kappa^2)^2 (N1's closed form confirmed as exact BO term and
  rigorous upper bound; exact nonlocal value ~ 0.66-0.73 of it);
  n_eff(y) in [0.9930, 1).
- Genuine nonlocality (new): the a-channel correlation length is
  O(y); no parametrically exact local mu exists; fast probes see a
  kinetic renormalization, never a constant mass.
- RULINGS: N1 "n = 0 attained nowhere" SURVIVES. N3 "n = 0 derived"
  REFUTED (and its hedge "radial restoration pushes n <= 0" also
  refuted — the lifting is positive and tiny).

## Consumer split (VA, exact statement)

- TIER-D STATIC DRESSING takes the radial-inclusive static object:
  the nu ~ 3 (n ~ 1) family with small channel-resolved corrections.
  Far-collar exact rationals (full rotation class, kinetic-dressed):
  lambda=2 m=+-1: mu = -1/45, nu^2 = 41/5 (nu = 2.863564212655) —
  CONFIRMED EXACTLY by VA. (N1's lambda=6 m=+-2 value 11/14 was NOT
  reproduced under three readings — refuted as stated, flagged;
  other ladder entries unaudited, carried hypothesis-grade.)
- WELD NORMAL MODES need the energy-dependent two-channel problem:
  the dressed single-channel operator is resonant (pointwise
  -P_FF * W/(1-W) structure, W-algebra verified; the omega0^2 sign
  convention vs the kinetic-flipped banked equation is flagged,
  VB B5). Neither constant-n number applies at mode frequencies.
  CONSEQUENCE: the banked weld mass term (2s) is unsupported by the
  responsive source in every regime — the weld binding analysis
  (incl. the factor-2 interface deficit) was computed with a mass
  term the native reading says does not exist. Re-grade queued (the
  exterior-sourced cavity push, below).

## Proven slot-covariance (N2 + VB, all PASS)

Second-order STATIC structure cannot see n — theorem-grade:
- The completion is ultralocal => gluing-silent (delta p_source = 0);
  the bilinear concomitant is conserved for all mu(n) and across
  sourced interfaces; Calderon idempotence n-blind; the slot-mixing
  contact term n-independent.
- Conservation bookkeeping is mu-FREE (I6, exact): the n-dependent
  mass is constant on the self-similar collar and leaks nothing. The
  exchange term is first-jet (I3).
- The canonical/distributional route is covariant: Pi_phi = -2f Pi_f
  exactly; both slots' EL distributions well-defined (mollifier-
  verified delta-weights -q/2 and +q); "the jump only lives in the
  f-slot" is false.
- THE CONNECTION THEOREM (I7, exact): with the first jet pinned, a
  slot change transforms the second jet affinely (W_gg = F'^2 W_ff +
  F'' V_f); W_ff = (n-1)J/f0, W_phiphi = 4nJf0. n is a connection on
  the configuration line; first-order structure supplies none.
- Conditional branch correctly graded NON-NATIVE: a conserved-
  canonical-stress demand closes at n = -2(1-q)/q = -4, but a
  competing bookkeeping gives n = 2, and an exhibited f-jet-invisible
  additive b(y) restores closure at ANY n (all three legs
  VB-verified). No native principle fixes the normalization
  (P_src-norm named).

## The nonstationary weld results (N3 + VB)

- COORDINATE MEASURE (the operationally banked lift): the weld chain
  is SLOT-BLIND — rigorous at ALL orders (the source depends on phi
  only; zero H1/K content). The n-symbolic fluctuation operator is
  exact: r^2 d_t^2 dphi + d_r(r^2 f^2 d_r dphi) - (4-2n) r^2 f^2 E0
  dphi - lambda f dphi = 0 (banked at n=0; halved-E0 at n=1; VB
  corrected the source-term sign in N3's lemma: -c n r^2 f^2 E0
  dphi^2). Collar map re-derives the invariant mu(n) family
  independently, omega^2 term landing on the confining side.
  Criticality of the completion holds on GENERAL static backgrounds
  (VB — stronger than claimed).
- PROPER-MEASURE LIFT: the measure expansion and the n -> 0
  obstruction are REAL (the phi-slot cannot ride sqrt(-g); couplings
  diverge), and the contravariant flux split EL_H1 = +r^2 dT^{tr} is
  real (reduces to the banked -r^2 dT_tr for C1 alone). But N3's
  HEADLINE n* = 4 COINCIDENCE IS REFUTED (VB): the H1^2 loading is
  off by a factor (-2); the corrected special points sit at
  n = -+ 2 E0/phi0'^2 (= -8 consistency / +8 degeneracy at q = 1/3),
  the -8 point conditional on one unverified C1 K-coefficient.
  Recorded, not promoted.
- RUNG-2 n-BLINDNESS (VB PASS): dT^t_theta[src] = 0 under both
  measures — the banked rung-2 CMB weld form and the existing macro
  discriminator record CANNOT constrain n. Named future test stands:
  a sourced-collar weld discriminator (radial structure in E0 != 0
  regions, proper measure only) is the n-sensitive macro channel.

## Corrections to the prior record (print-level, no contamination)

VA settled N1's factor-4 flag: sourced_second_jet_results.md's printed
potential prefactor (3a^2/2F)G1 and "P_a/(4a)" carry a factor 4
relative to the defining integral; the correct orthonormal form is
P = (3a^2/8F)G1 (equivalently P = (pi/2) F kappa^2 G1). Decisive:
every NUMBER in that record (demanded kappa(1) = 0.683095, the
couplings V_a1g1, V_a0g0) matches the corrected form exactly — a
print slip, not a computational error. This doc is the correction
note; the prior doc is untouched (append-never-edit).

## Honest gaps and conditionals (carried forward)

- Everything responsive rides the rotation-closed class and the
  spherical-AVERAGE interface reading (the pointwise-vs-average fork
  remains OPEN and gating — CANON C-2 adjudication flagged for
  Charles).
- The coordinate-vs-proper measure fork is UNDERIVED (coordinate is
  what the banked sector uses and what the slot-blindness proof
  covers; proper forbids n = 0 and carries the corrected -+8 special
  points).
- Anchor-depth (kappa ~ 0.7) numerics carry uncontrolled truncation
  error (demanded kappa(1) is class-relative: 0.683 at ell<=1, 0.768
  at ell<=2); only limits and identities are banked.
- The far-collar rational ladder beyond lambda=2 m=+-1 is
  hypothesis-grade (one member refuted as stated).
- N1's "weld omission is an error" is NOT yet the recorded verdict:
  the statement banked here is conditional — IF the source is the
  responsive angular sector, THEN the weld mass term is unsupported.
  A fixed external source of the (i-phi) character remains logically
  possible (it is the one reading that produces mu = 2s); what is now
  closed is deriving it from the metric's own angular activity.

## Verifier record

- VA (contradiction adjudication): blind pass 2026-06-11; from-scratch
  FEM Schur + symbolic BO; 18 PASS / 1 FAIL (the lambda=6 rational) /
  3 flags; rulings as recorded.
- VB (structural claims): blind pass 2026-06-11; ~45 checks, 41 PASS;
  refuted B3's n* = 4 with the corrected loading; confirmed all of
  N2's theorems and N3's coordinate-measure chain.
- Driver note: the panel-verifier cycle again flipped a headline
  (N3's "n = 0 derived") and a named special point (n* = 4) before
  banking. Three pushes running this discipline have yet to let an
  error into the record.

## Next (Charles-ordered): the exterior-sourced cavity push

Launch criteria met (both verifiers reported). Brief: vacuum
matter-side interior; all source data entering through the interface
balance from the universe side (mirror canon); the medium's response
law = the adjudicated screened object. Pre-declared questions:
(a) supply attribution (is s = q(1-q)/2 forced as the flux the
exterior must deliver — the "chimera test": is interior-vs-exterior
attribution invariant or gauge); (b) formation threshold under
boundary-only driving; (c) the binding threshold under a
matter-conditioned exterior D_+(omega) replacing the vacuum exterior
— including whether the resonant two-channel structure supplies the
negative direction the E0 < 0 window needs; (d) whether the f >= 1
pointwise pathology resolves with activity on the universe side.
