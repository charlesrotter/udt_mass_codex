# Curvature-principal reciprocal/angular split ownership audit — preregistration

Date: 2026-08-12  
Branch: `grok`  
Question class: **METRIC-LED CHARACTERIZATION**  
Computation class: CPU algebraic curvature/finite-jet audit; no ODE, GPU, action, source, or fit

## Whole question

The complete-coframe work uses a supplied metric-orthogonal reciprocal/angular `2+2` split
`E_pair orthogonal H`. This audit asks whether that registered split is recovered from pointwise
curvature of the supplied metric, rather than supplied independently.

The audit will classify the split against both:

1. the self-dual Weyl bivector operator (full Petrov/Jordan classification); and
2. the mixed Ricci endomorphism (block preservation and spectral separation).

It will not ask which split resembles the desired universe. Every type, ambiguity, degeneracy,
misalignment, and failure of smooth continuation will be retained.

## Exact bounded arena

1. **Founding spherical family.** Analyze
   `ds^2=-exp(-2 phi)c_E^2 dt^2+exp(2 phi)dr^2+r^2 dOmega^2` locally, including the
   conformally-flat degeneracy. The analytic conclusion may be family-conditional; no equation for
   `phi` is supplied.
2. **G63 complete witnesses.** Evaluate all 14 frozen rows in
   `NUMERICAL_SAMPLE_UNIVERSE.tsv` at the registered point `p` and the already defined nearby
   endpoint-atlas points `q,r`: 9 R17 rows and 5 fully time-live local rows. No sample may be
   removed because of its Petrov type or split result.
3. **G85 regular completion classes.** Evaluate the three constructive regular classes
   `A03_RADIAL_SHIFT_TIMELIVE`, `A04_LAPSE_LIFT_TIMELIVE`, and the shift-supported
   `A05_MIXING_TAPER_BEFORE_SEAM` at the generic equatorial seam point, away from the angular
   axis. All 196 frozen polynomial profiles are retained where the class depends on them.
   These are bounded constructive witnesses, not complete parameter families.

G85's zero-shift Kruskal-local A05 subcase is recorded but is not numerically classified unless the
source owns a complete second jet in the regular chart. Missing second-jet ownership must return
`INSUFFICIENT_OWNED_JET`, never a guessed Petrov type.

## Mathematical classifier

Petrov classification will use the complete complex self-dual Weyl operator, not only `I`, `J`, or
their discriminant. The classifier distinguishes:

- three distinct eigenvalues: `I`;
- repeated nonzero eigenvalue with diagonalizable operator: `D`;
- repeated nonzero eigenvalue with a nontrivial Jordan block: `II`;
- nilpotency index three: `III`;
- nilpotency index two: `N`;
- zero Weyl operator: `O`.

`I,J` are diagnostics only. They may not distinguish `D/II` or `O/III/N`.

For the registered split, the oriented orthonormal pair bivector and its self-dual completion are
tested directly against the Weyl operator. A Weyl-owned split requires:

1. eigenbivector residual below tolerance;
2. an isolated, type-appropriate principal eigenspace; and
3. consistent projector recovery under an independent endpoint-frame change.

A Ricci-owned split requires the registered pair/screen decomposition to be invariant under
`Ric^a_b` and the pair and screen spectral sets to be disjoint. Mere block preservation without a
spectral gap is recorded as alignment, not ownership.

The production calculation uses double-precision automatic differentiation of the supplied metric.
The independent calculation uses a separately coded finite-difference curvature route and direct
frame-covariance tests. Analytic founding-family anchors and selected high-precision numerical
anchors are required.

## Preregistered numerical gates

- Metric signature: exactly one negative eigenvalue at every classified point.
- Curvature cross-route agreement: relative Frobenius error `<= 2e-5` for Weyl and Ricci tensors.
- Algebraic-zero threshold: `1e-9 * max(1, curvature_norm)` in the production route.
- Eigenvalue coincidence threshold: relative separation `<= 2e-7`, and confirmation by rank/Jordan
  tests; a near threshold result is `NUMERICALLY_UNRESOLVED`, not forced into a Petrov type.
- Registered Weyl-principal residual: `<= 2e-7` in both routes.
- Ricci block-preservation residual: `<= 2e-7` in both routes.
- Ricci ownership spectral gap: `>= 2e-6 * max(1, ||Ric^a_b||)`.
- Endpoint-frame covariance defect: `<= 2e-8`.

Thresholds are numerical classification gates, not physical acceptance filters.

## Allowed landing classes

Each evaluated point returns exactly one split-owner class:

- `UNIQUE_WEYL_DERIVED_SPLIT`
- `FINITE_WEYL_PRINCIPAL_CANDIDATES__REGISTERED_ONE_ALIGNED`
- `RICCI_DERIVED_WHEN_WEYL_DEGENERATE`
- `WEYL_AND_RICCI_AGREE_ON_SPLIT`
- `CURVATURE_ALIGNED_BUT_NOT_UNIQUE`
- `NO_TESTED_POINTWISE_CURVATURE_OWNER`
- `SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS`
- `NUMERICALLY_UNRESOLVED`
- `INSUFFICIENT_OWNED_JET`

The package-level conclusion must be one of:

1. `CURVATURE_OWNS_REGISTERED_SPLIT_ON_ALL_TESTED_NONDEGENERATE_STRATA`
2. `CURVATURE_OWNS_REGISTERED_SPLIT_ONLY_ON_A_PROPER_SUBSET_OF_TESTED_STRATA`
3. `CURVATURE_REDUCES_SPLIT_TO_FINITE_CANDIDATES_WITHOUT_UNIQUE_GLOBAL_OWNER`
4. `REGISTERED_SPLIT_IS_NOT_RECOVERED_BY_TESTED_POINTWISE_CURVATURE_OPERATORS`
5. `BOUNDED_EVIDENCE_NUMERICALLY_OR_JET_UNRESOLVED`

## Falsification and conclusion ceiling

The optimistic lead is falsified if any regular tested witness has a robustly misaligned registered
split or if Weyl/Ricci degeneracy leaves a continuum without a curvature owner. It is narrowed—not
falsified—if ownership holds only on some strata.

Even a universal positive result in this bounded arena may conclude only that the **registered local
`2+2` split** is curvature-recoverable there. It may not select a metric history, observer query,
pair realization, action, source, `X_max`, CMB history, physical branch, or global smooth section.
Petrov `O` alone may not be used to infer an aether theory.

