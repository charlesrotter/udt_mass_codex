# Canon-Fork Tests by Compute — Results

Status: working audit, not canonical. Created: 2026-06-11. Charles's
directive: settle the two canon-adjacent forks by computation where
possible; only the residue goes to adjudication. Process: two
data-blind derivation agents (FA exterior fork, FB interface fork),
one blind adversarial verifier over both (VF: ~38 checks, 31 PASS,
4 refuted-as-stated, 1 conditional, 2 unverifiable). New files only.

## Fork 1 verdict — ZERO-TAIL vs MIRROR EXTERIOR: SETTLED, MIRROR FORCED

For any nontrivial embedded matter cell, a zero-tail (flat) exterior
is NOT a legal native configuration; the exterior carries ZERO free
structure — it is the unique smooth continuation of the cell's
interface jet ("mirror-class"). Verifier-confirmed chain:
1. TRIVIAL-CELL LEMMA (theorem, ell<=1 source-free, y>0): the RHS is
   jointly analytic at the flat point (P_a = a/F + (6/5)a^3/F^3 +
   (81/35)a^5/F^5 — series verified); flat continues to flat both
   ways; a flat annulus C1-glued to anything forces the trivial cell.
2. THREE OBSTRUCTIONS to a flat buffer, all verified: no vacuum
   interpolation; the F-kink at a bare buffer edge carries
   first-variation delta weight exactly +q*y_b/2 with NOTHING in the
   reduced action supplying a surface source (P is pointwise
   algebraic); the angular-field jump costs infinite action (exact
   1/epsilon mollified rate, S*eps = y_b^2 a0^2/4 constant over three
   decades).
3. FORCING: deviation modes y^{-q}, y^{-(1-q)}, alpha + beta/y all
   consumed by jet-matching; shape-channel Hessian strictly positive
   on 0 < kappa < 1. The exterior = the jet's continuation, uniquely.
4. THE ZERO-TAIL IS THE q -> 0 IDEALIZATION, with a derived validity
   law (new exact result, verifier-confirmed at O(q)):
   ell+1 - D_+ = q[2 ell/(2 ell+1) - lambda/(4 lambda+1)] + O(q^2).
   At q = 1/3 the reservoir errors are 9.7/7.1/5.6% (ell = 1,2,3;
   D_+ = 1.80622024, 2.78719083, 3.77770570) and the shell error is
   O(1) (2q vs 0).
5. ENSEMBLES HOOK (scoped): ell >= 1 cell hair decays
   stretched-exponentially (K_nu(tau0 y^{q/2})); the monopole/scaling
   channel is UNSCREENED POWER-LAW — robust across readings — but the
   literal exponent (1/y vs y^{-2/3}) is reading-dependent
   (frozen vs responsive source fluctuation; VF conditional). MUST be
   settled before the ensembles route banks on Coulombic
   superposition.

Residues (the honest boundary of the verdict): (a) the
no-surface-source audit covers the banked reduced action only — a
boundary term native to the FULL UDT action would reopen the
bare-edge question (same hole as the standing "jet realizability
untested" caveat); (b) canon wording for Charles: canonize "the
embedded-cell exterior is the unique smooth continuation of the
interface jet (mirror-class)", NOT "the exterior is exactly y^{-q}"
(the exact exponent stays open under the over-determination negative).
Bookkeeping: both exteriors give the shut window; no banked verdict
flips; NEGATIVES_REGISTRY entry 3's mirror reading is now DERIVED.

## Fork 2 verdict — POINTWISE vs AVERAGE f >= 1: SETTLED IN WEAKENED FORM

CROSSING-INDIFFERENCE (clean, fully verified): for the metric class
ds^2 = -f dt^2 + f^{-1}dy^2 + y^2 dOmega^2 with arbitrary smooth
f(y,theta), the exact invariants have denominators 2y^2 f^2 (R) and
4y^4 f^4 sin^2(theta) (K, Ric^2 — FB's quoted tan^2 was a
stated-form error, corrected by VF; content unchanged): NO (f-1)
factor exists; the only degenerate loci are f = 0 and y = 0. At
actual pointwise f = 1 crossings of real flows, all invariants are
finite, smooth, spike-free (max relative second difference 6e-6),
Lorentzian both sides. f = 1 is clock bookkeeping (moves under
constant clock rescaling); f = 0 is geometry. NEW: the seal is
CURVATURE-SINGULAR within the ansatz class — exact on-axis law
f^2 K -> 12 a^2/y^4 (symbolic + flow-verified) — unlike spherical
f -> 0. The seal is real structure; the f = 1 line is nothing.

METRIC-VIOLATED (certified in-model; near-threshold gap flagged):
every terminating flow crosses pointwise f = 1 before sealing (no
seal-without-crossing exists: kappa_cross = 1 - 1/F, F > 1 always);
SAT flows are exactly clean. VF REFUTED the "inside the controlled
region" qualifier: for c < 1.3 c* the crossing sits at kappa =
0.97-1.0000, beyond the truncation's own trust boundary — on the
near-threshold band the inevitability rests on extrapolation
(ell<=2 sharpening pushes the right way but does not close it).
CERTIFICATION GAP: ell<=3 or a controlled kappa -> 1 asymptotic —
now merged into the sealed-cavity push prerequisite (below).

CANON AUDIT (verified): C-2's monotone-dilation language is
1D-profile; "pointwise" appears nowhere; NEITHER reading is
canonical — both were glosses. The monopole phi stays FINITE at any
actual seal (F_seal = 14.6 at c = 0.30, phi_mono = -1.34) and
diverges only in the threshold limit — FB's -inf/+inf symmetry was
overstated (VF correction).

THE RESIDUE FOR CHARLES (low-stakes, definitional): what "inside a
matter cell" means — (i) the weld-sphere interior (formed cells then
contain harmless slow-time patches and, when strongly driven, a polar
channel), or (ii) the f >= 1 region itself (the cell boundary is the
non-spherical f = 1 level set). The metric expresses no preference;
nothing physical rides on the choice; it sets documentation
vocabulary only.

## ell<=2 seal facts (verifier-confirmed signs)

Tadpole dP/db|_0 = sqrt(5)(2 kappa - L)/(4 kappa) =
-sqrt(5) kappa^2/6 - ... (exact); the seal PERSISTS AND SHARPENS
under ell-extension: y_seal moves out (0.0757 -> ~0.114-0.123,
convention-level spread), t_seal drops ~19%, c*(gamma=1) drops
0.207 -> 0.159 +- 0.001 (formation ~24% easier), the violating shell
GROWS (direction confirmed; FB's +52% magnitude not reproduced —
convention), the ell=2 amplitude is driven negative as the tadpole
sign demands. The ell<=1 class is conservative for termination.

## Bookkeeping corrections (record hygiene)

- exterior_cavity_results.md's seal-shell figure "0.747% of
  log-depth" is NOT reproducible as quoted under any gamma = 1
  convention tested; FB's 0.085% is exactly the relative-eps
  convention (c = c*(1 + 1e-4)). RULE: seal-shell figures must carry
  (gamma, eps-convention, cutoff) to be citable. The qualitative
  statement (shell always violates, thin near threshold) is fully
  confirmed.
- FB's K-denominator stated form: sin^2(theta), not tan^2(theta).
- FB's gamma0-sign claim: unverifiable (no definition recovered) —
  not banked.

## Verifier record

VF: blind pass 2026-06-11; ~38 independent checks from scratch
(including full general-f curvature derivation, own flow engine
validated on five banked anchors, Richardson small-q extrapolation);
31 PASS / 4 refuted-as-stated / 1 conditional / 2 unverifiable;
rulings as recorded. Driver note: VF again did its job against the
convenient story — the near-threshold certification gap and the
reading-dependent monopole exponent are exactly the kind of items
that would have silently propagated.

## Hand-off

Both canon adjudications are now compute-settled up to: one sentence
of canon wording (mirror-class continuation), one low-stakes
vocabulary choice (the meaning of "inside"), and two technical items
folded into the next push: the near-threshold seal certification
(ell<=3 / kappa -> 1 asymptotics) and the monopole-exponent reading
(gates ensembles). Next: the sealed-cavity spectrum push (S1 seal
control, then S2 the compact-domain mode problem) — launched on
Charles's order in this session.
