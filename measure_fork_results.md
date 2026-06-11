# The Measure Fork — Settled

Status: working audit, not canonical. Created: 2026-06-11. Process:
two derivation agents (MF1 covariant time sector, 41 checks; MF2
completion character, 27 checks), one joint blind adversarial
verifier (VMF: 62 checks from scratch, 59 PASS as written, 3
verifier-side artifacts fixed, 0 claim refutations — including the
composition test the two halves never ran on each other). New files
only. Data-blind throughout. Charles-ordered: settle this fork before
ensembles.

## Ruling: SETTLED. W_A is the derived weight; the fork dissolves for the native theory.

1. THE TIME WEIGHT IS DERIVED, NOT CHOSEN (MF1 + VMF): the second
   variation of the covariant C1 action on ARBITRARY static angular
   backgrounds, with the full time row of the metric (g_Tr, g_Ttheta,
   g_Tphi) in the scheme, gives after exact Schur elimination the
   flipped time kinetic W = -(c/2) r^2 sin(theta) EXACTLY — pointwise,
   background-independent, channel-uniform, m-unmixed. In the library
   variables: G^(m) = <R R'/f^2> = W_A exactly (independent
   integration agrees with the S2 matrices to 1.3e-13). W_B (1/f^3)
   is RETIRED: structurally unattainable — the flip factor is f-free
   for every completion loading (the kappa_V interface formula,
   verified exact).
2. THE FULL-ROW SCHEME IS MANDATORY, NOT PREFERABLE (MF1 + VMF
   findings F-1/F-2): the spherical-transplant (g_Tr-only) scheme is
   PV-singular not only inside every library member but ON THE
   CRITICAL COLLAR ITSELF at every y (the alpha_aa = 0 locus covers
   76-91% of the sphere; far-collar edges -> +-sqrt(1 - q^2/6s) =
   +-0.9129, analytic). The full row is the only well-defined native
   time-sector reduction. Spherical anchors all reproduce exactly
   (the algebraic weld, the banked alpha, the flipped operator with
   its -4r^2f^2E0 mass, the omega^2 = +7.53 counterexample).
3. THE FORK DISSOLVES FOR THE NATIVE COMPLETION (MF2 + VMF): there is
   no independent source functional to assign a measure to — the
   completion IS the angular sector of the covariant C1 action
   (exact split, no cross term; sqrt(-g) built in; criticality data
   measure-free). Stronger (VMF): the static fork was ALWAYS empty —
   mu(n) is identical under ANY smooth radial measure factor. The
   old free choices (slot n, measure, source character) were shadows
   of one derived object.
4. THE COMPOSITION IDENTITY (VMF's H2-D — the place the halves could
   have collided): the native completion's derived H1^2 loading IS
   alpha_aa of the full second variation restricted to the rotation
   class — the same term, not an addition — and because the native
   angular sector loads alpha AND beta coherently (gradient-aligned),
   the Schur complement is invariant: W_A survives EXACTLY, zero
   dressing. Only a posited potential-type term (alpha without beta)
   deforms the flip — and native kappa_V = 0. (Composing wrongly
   shifts W by +0.89 at the anchor — the collision is real if
   mishandled, exactly absent natively.)
5. NEITHER OLD LIFT SURVIVES (MF2 + VMF): the coordinate lift's
   slot-blindness is refuted for the native completion (Delta-W < 0
   definite); the proper lift's single-n parameterization is refuted
   (the derived loading is channel-resolved with exact far-collar
   rationals 10/3, 5/3, 7/3, 14/5, 14/9, 30/11; sweep range
   [1.556, 4.883]; none of {0, 1, +8, -8} attained; channel
   separation >= 1.677 — no single n exists even within the loading
   alone). The n = +-8 special points are DEAD as native structure.
   The angular sector is exactly K-blind.
6. THE HOLDOUT IS DEAD — THE BANKED WELD MASS IS REFUTED-AS-NATIVE
   (MF2 + VMF re-grade): the fixed-external (i-phi) source has no
   native carrier (volume/boundary-only/Pi_f no-gos; the metric's own
   activity has kernel n ~ 1, never 0; the zero-tail shelter was
   COMPUTE-SETTLED dead by the fork tests — MF2's conditioning on the
   C-2 gloss was stale; only canon WORDING remains with Charles).
   The 2s mass term inherits only the program-wide full-action
   boundary-term caveat. All banked L0 maps keep internal validity as
   posited-family computations; native standing is withdrawn.
7. SEAL BC TABLE, FINAL (derivation-backed): m=0 pole-value direction
   FORCED (Friedrichs/Dirichlet); m=0 complement, every m=1, every
   m>=2: ONE-PARAMETER FAMILY — the theta-family is REAL. W_B's m=1
   kill is refuted. S2's relaxation ladder stands unchanged (its
   primary weight was the derived one). The seal-surface discreteness
   gate now needs exactly one object: A NATIVE SELECTOR for theta
   (e.g. a 4D boundary term at the curvature-singular seal), or the
   controlled true-seal asymptotic.

## New flags (recorded)

- g_rtheta tadpole (c/4) f_r f_theta sin(theta) on formed angular
  backgrounds: REAL; purely a static-sector class flag (the time
  sector is q-robust — g_rtheta decouples from the entire time row,
  VMF's added check). The diagonal-class restriction does real work
  on formed backgrounds; unexamined in the static sector.
- Amendment A-1 (scope): "sqrt(-g) is delta-phi-free at all orders"
  holds in the weld scheme; with the full row on, delta-phi enters at
  O(eps^3) — second-order claims untouched.

## Verifier record

VMF: blind joint pass 2026-06-11; independent 4x4 adjugate jets, own
flow integrator, own GL nodes, own FD eigensolver, symbolic
far-collar limits; GPU (CUDA float64, matmul-only per the recorded
pitfall) for the 2M-point degeneracy maps and the n_H1 sweep,
GPU<->CPU agreement 1e-15; 62 checks, 0 claim refutations; ruling
SETTLED AS STATED with amendments A-1..A-3 (all incorporated above).

## Consequences

- The ENSEMBLES GATE IS OPEN (Charles's ordering): launched, with the
  metric-led reframe (interrogation-discipline rule).
- The seal-surface sector's to-do reduces to the theta-selector
  question (above).
- S2 record unchanged; the dressed-operator concern is closed by the
  composition identity (zero dressing).
- Registry updates in this commit: W_B retired; weld-mass re-grade
  propagated; entry #5 finalized.
