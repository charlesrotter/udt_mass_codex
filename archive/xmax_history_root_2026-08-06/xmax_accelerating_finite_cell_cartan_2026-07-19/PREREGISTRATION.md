# Accelerating reciprocal-frame finite-cell Cartan audit — preregistration

Date: 2026-07-19

Base: `9f12b97349b09f7392edb4bd7204c52cbc597d10`

Mode: `MAP -> OBSERVE -> PONDER -> DERIVE`; bounded CPU-only exact exterior algebra

## Whole question

For the conditional four-dimensional reciprocal metric representative with arbitrary smooth
time-dependent depth re-centering, compute the torsion-free Cartan connection and every independent
curvature two-form, retain an arbitrary intrinsic two-dimensional angular metric, and integrate the
resulting curvature over symbolic finite-cell faces. Determine whether observer velocity or
acceleration survives as invariant curvature/curvature flux, and whether the metric supplies a
native finite-cell gravity-versus-acceleration crossover rule.

This is metric-led. It does not target GR equivalence, a desired crossover, a round angular sector,
or a vanishing cell defect.

## Declared representative and scope

Write `psi=phi-beta(t)` and use the pulled-back orthonormal coframe

\[
 \theta^0=c e^{-(\phi+\beta)}dt,
 \qquad
 \theta^1=L e^{\phi-\beta}(d\phi-\dot\beta dt),
 \qquad
 \theta^a=e^{\phi-\beta}\bar\theta^a,
 \quad a=2,3.
\]

The seed angular coframe `bar(theta)^a(y)` is arbitrary, stationary, and independent of `phi`; its
intrinsic connection and Gaussian curvature are retained symbolically. This is the full Cartan
curvature of that declared four-dimensional reciprocal warped-product representative. It is not the
most general `2+2` UDT metric: transverse shifts/twist, `phi`-dependent angular shear, time-dependent
angular data, and non-integrable screen distributions remain open and may not be silently set to
zero in a global claim.

## Premise and choice ledger

| Object | Entering status | Treatment |
|---|---|---|
| Positional dilation, dual Reciprocity, CSN | `FOUNDING` with representation choices separately ledgered | permitted inputs |
| Projective/Xmax full-frame realization | `CONDITIONAL` | supplies the bounded reciprocal frame family |
| Dynamic frame map | `EXACT_CONDITIONAL` in fixed-F3 family | exact pullback input |
| Reciprocal warped-product coframe | `CONDITIONAL` | tested representative, not complete UDT metric |
| Angular metric `bar(q)` | `FREE-AND-CHARACTERIZED` | arbitrary stationary intrinsic two-geometry |
| Angular twist/shear dependence on base | `OPEN` | excluded from this representative and retained as an explicit completeness gap |
| `beta(t)` | `FREE-AND-EXPLORED` | arbitrary smooth frame path; no profile pinned |
| `c`, `L` | positive symbolic parameters | no measured or fitted value |
| `L=X_max` | `OPEN / POSSIBLE NORMALIZATION` | not imposed |
| Finite cell | symbolic coordinate faces and an angular patch | no physical cell size selected |
| Curvature flux | exact surface integral in the declared coframe gauge | not equated to finite holonomy |
| Holonomy | path-ordered connection transport | structural classification only unless exactly computed |
| Action, source, carrier, matter, field equation | `OPEN` | excluded |
| GR equivalence principle | comparison idea only | not adopted or used in algebra |

## Registered tests

### C1 — dynamic coframe and torsion

Recompute all `d theta^I` with arbitrary `beta_dot` and `beta_double_dot`. Solve the metric-compatible
antisymmetric spin connection and require all four torsion two-forms to vanish. Do not infer the
connection by importing an observer or geodesic law.

### C2 — complete curvature census in the declared representative

Compute

\[
 \Omega^I{}_J=d\omega^I{}_J+\omega^I{}_K\wedge\omega^K{}_J
\]

for all six independent Lorentz-frame planes `01`, `02`, `03`, `12`, `13`, and `23`. Retain the
intrinsic angular connection and curvature exactly. Verify the first Bianchi identities.

### C3 — acceleration cancellation

Expand the spin connection and curvature in the unprimed coordinate coframe. Any uncancelled
`beta_dot` or `beta_double_dot` in a curvature two-form refutes the claim that acceleration is pure
frame structure in this representative. Coordinate-basis Levi-Civita connection terms are not
themselves curvature.

### C4 — finite-cell face fluxes

For a symbolic rectangular `t-phi` face and symbolic time-angular strips, integrate the exact pulled-
back curvature two-forms where the chosen coframe gauge makes the integral explicit. For an angular
patch `Sigma`, integrate the `23` curvature exactly. Preserve orientation and boundary dependence.

### C5 — angular/global check

For a closed orientable angular surface, use Gauss--Bonnet only as a mathematical identity to rewrite
the integrated `23` flux. Determine what zero flux would imply, but do not impose zero flux, constant
curvature, roundness, topology, or a selected section.

### C6 — flux versus holonomy

Record that a Lie-algebra-valued curvature surface integral is gauge-dependent and is not generally
equal to the finite non-Abelian holonomy. Verify the leading small-loop relation only in its stated
order, or compute an exact holonomy only for a genuinely commuting restricted face.

### C7 — equivalence-window adjudication

Determine whether current metric, CSN, Reciprocity, and finite-cell premises provide an invariant
norm, a selected cell size, and a derived threshold that would turn curvature/holonomy into a unique
gravity-versus-acceleration crossover formula. If any ingredient is absent, the crossover remains
`OPEN`; do not invent a tolerance.

## Falsification and certification contract

`ACCELERATION_PURE_FRAME_IN_THIS_REPRESENTATIVE` requires exact cancellation of every beta derivative
from all six curvature forms and registered face fluxes. It does not require the underlying curvature
to vanish.

`FINITE_CELL_DISTINGUISHES_CURVATURE` means a finite surface can carry nonzero metric curvature even
when observer-frame acceleration contributes none. It does not mean that a unique physical cell,
measurement, or threshold has been selected.

`FULL_CARTAN_CURVATURE` refers only to all six curvature planes of the displayed four-dimensional
warped-product representative. It may not be generalized to omitted twist/shear sectors or called
the complete UDT metric.

Any replacement of exact holonomy by raw curvature flux, any hidden `L=X_max` identification, any
round-`S^2` selection, or any imported GR field equation fails the package.

## Maximum allowed conclusion

At most this audit may:

- derive the complete Cartan connection and six-plane curvature of the declared representative;
- prove or refute beta-derivative cancellation in those forms and finite-cell fluxes;
- expose exact reciprocal/angular curvature contributions and finite-cell boundary dependence;
- state the exact conditions under which a restricted curvature component or flux vanishes; and
- identify the smallest still-missing inputs for a physical equivalence window.

It may not derive or adopt a UDT equivalence principle, a physical cell size, an error threshold,
`c`, `L`, `X_max`, a round angular carrier, an action, a source, matter, mass, or canon.

## Evidence gates and stop line

The package must preserve executable algebra, raw transcripts, exact commands and versions, an
independent implementation, exercised semantic catch-proofs, a fresh adversarial review, a SHA-256
manifest, six frozen-manifest replay, prior-package replay, navigation/frontier checks, the known test
baseline, and untouched original dirty-checkout metadata.

Stop after commit, push, and fast-forward integration to `grok`. Do not edit startup controls or
`CANON.md`. Do not launch GPU work, action construction, carrier work, time-live solves,
canonization, or repository reorganization.
