# Full-PDE Stage P1 — The Static Solution-Set Classification

Status: working audit, not canonical. Created: 2026-06-11.
Charles-framed ("it's an equation with limited variables — what
answer solves it?"); metric-led. Process: P1 derivation/build agent
(derivation 29/29, validation 66/0 after collector rerun), collector
agent (independent re-derivation of the key theorems from its own
variation), blind adversarial verifier (VP1: 61/61 from scratch, own
derivation route, own Galerkin stack N=3000, plus a genuinely
different finite-volume discretization as cross-check; zero
refutations). Data-blind. New files only.

## THE THEOREM (verifier-confirmed, triple hostility closed)

Within the static, axisymmetric, even-sector class (areal canon
k = 0; g_rr = 1/f from f = e^{-2phi}; smooth, Lorentzian,
nondegenerate), under the C1 action ALONE, the complete static
solution set is EXACTLY:

   { f spherical, q = 0, w ARBITRARY }

— i.e. FORMED ANGULAR CELLS ARE NOT STATIC SOLUTIONS OF C1.
Chain (all exact): q and w enter the reduced Lagrangian with NO
derivatives at any nonlinear order (structural); the q-equation has
the unique root q* (whose diagonal-point tadpole reproduces the
banked measure-fork value exactly); exact q-elimination via a perfect
square FLIPS the angular gradient sign (the nonlinear completion of
the verified quadratic angular flip — same object); the w-equation
dL/dw = -(c/4) sin(th) f_theta^2/(f(1+w)^3) is then NONZERO on both
branches wherever f_theta != 0 — no smooth nondegenerate stationary
point exists. Parameterization-robust (verified under W = e^{2s} and
under the non-unimodular class with the breathing mode reinstated —
which is strictly MORE constrained, additionally forbidding
f_r != 0). Pointwise-algebraic, so no theta-dependent w evades.
Sharpenings (VP1): the only off-spherical stationary structure is the
NONSMOOTH CORNER at the degenerate-metric locus (D = 0) — C1 drives
the free shape sector toward metric degeneracy, not toward a cell;
and even on the spherical family w is an EXACT FLAT DIRECTION to all
orders — C1 is completely blind to sphere shape.

## The two consistent constrained classes (both validated solvers)

- CLASS A (diagonal, q = w = 0): the entire banked library lives
  here. Elliptic; the radial Cauchy march is continuum-ill-posed
  (regularized only by finite-ell truncation — explains S1's layer
  non-convergence structurally). Deep seals, depth divergence at
  threshold, c*_A steep in gamma. NOTE: the diagonal M2 solution
  crosses the joint-system sonic line (t = 1.2551) BEFORE its own
  seal (2.1345) — banked seals sit outside the q-joint trust branch.
- CLASS B (q on its exact branch, w = 0): the angular sign flips =>
  HYPERBOLIC; characteristics du/dt = +-sqrt((1-u^2)/f); poles
  characteristic; the weld-Cauchy problem is GENUINELY WELL-POSED —
  exterior data propagates inward (the well-posedness form of the
  exterior-field picture). At recorded drivings: NO SEAL (M2 driving
  saturates; ell-robust 1..6; independent finite-volume PDE agrees to
  4e-5). Thresholds: c*_B(ell<=3, gamma=1) = 1.8492 (vs A 0.1417);
  gamma-flat (vs A steep); near-threshold B seals are SHALLOW
  (y_seal ~ 0.46, no depth divergence) and exit the trust branch
  before sealing (mixed-type treatment needed to certify).
- THE COSMIC POINT: c*_A(gamma = q) = 0.02263 vs c*_B = 1.3387 —
  59x gap (ell<=3-tied magnitude; orders-of-magnitude contrast
  ell-robust): DEEP-CELL PRECIPITATION AT COSMIC DRIVING IS A
  DIAGONAL-CLASS PHENOMENON ENTIRELY.

## What the theorem forces (the fork; binary and exhaustive)

Static formed cells in the complete class are ELIMINATED. Either:
(i) FORMED CELLS ARE GENUINELY NONSTATIONARY — matter is motion in
    the shape sector (CANON C-3's redirect; Charles's phi-angular
    hunch's home; the runaway force is PURELY phi-angular sourced,
    prop. f_theta^2); or
(ii) C1 IS INCOMPLETE — a native w-stiffness sector exists (a
    metric-derived term that sees shape). VP1 grades the "same
    species as the EH-remainder target" identification as
    STRUCTURALLY PLAUSIBLE but an unverified forward claim — the
    program's oldest named missing object (the native EH-remainder
    derivation, branch-iii era) is the natural candidate, not a
    result.
Three independent session arrows now point at the nonstationary
sector: this theorem, the single-cell secular-stability flag
(ensembles verifier), and the canon redirect.

## Consequences and re-scopings (registry-relevant)

- ALL banked cell objects (library, seals, thresholds, formation law,
  the E1/E2 ensembles results) are CONSTRAINED-CLASS (diagonal or B)
  flows — physically meaningful as such, but not solutions of the
  full static system. Premise added registry-wide.
- The angular audit's "decisive computation" (corrected-class spectra
  on self-consistent static q,w-on backgrounds) is UNRUNNABLE AS
  POSED — no such backgrounds exist. Rescoped to: trust-bounded
  diagonal/B spectra, or the nonstationary sector.
- Classifier note: with two independent implementations agreeing,
  c*_A(ell<=3) = 0.141653 under the stated classifier; the banked
  0.141644 carries a <= 9e-6 classifier-variant offset (the S1
  ride-exit variant) — convention, not error; figures must carry
  their classifier (rule already standing).
- "Class A gamma^2 law" label retired (A is ~gamma^{1.5-1.7} steep;
  the A-steep/B-flat contrast is the verified content).
- Scale covariance: amplitude is quotiented in the FORCE (P_X
  degree-0), so fate classification must be horizon-based — the
  ride-away classifier defect class is now understood structurally.

## P2 readiness

Validated: both classes' IVP + Newton-Chebyshev BVP (1e-12
agreement), analytic GPU Jacobians, pseudo-arclength continuation,
2D elliptic Newton, closed-form sonic/Q* diagnostics. P2 (branch
classification) can run on the constrained classes with trust
bounds. The full-class static classification is COMPLETE by theorem
— P2's real successor is the nonstationary sector (or the
w-stiffness derivation attempt, which would reopen static
classification with the new term).

## Verifier record

VP1: blind pass 2026-06-11; 61/61; parameterization hostility closed
both ways; finite-volume cross-discretization; the composed logical
chain ruled exactly as recorded above. Collector: independent
re-derivation of q*, the corner calculus, and the Class B PDE from
its own variation of the covariant action; 66/0 ladder. Driver note:
the headline arrived because the question was posed Charles's way —
solution-set, all fields simultaneously, full nonlinearity.
