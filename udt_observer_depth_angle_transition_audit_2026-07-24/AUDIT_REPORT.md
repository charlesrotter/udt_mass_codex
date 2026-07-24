# Observer depth–angle transition audit

Date: 2026-07-24

Status: `VERIFIED_WITH_CAVEATS`

Compute: CPU-only exact algebra; no ODE/PDE, fitting, or GPU work

## Result first

The audit found a real exact structure:

```text
reciprocal response: exp(-rho), exp(+rho)
projective radial coordinate: xi=tanh(rho)
observer recentering: xi'=(xi-alpha)/(1-alpha xi)
```

The `tanh` coordinate is unique **given** the already registered anchored
projective interpretation of the reciprocal ray. It is not yet derived as
physical proper observer separation.

The user's exponential-limit expectation is confirmed at the correct
scope. Both bounded registered profiles approach a finite endpoint
exponentially in `rho`:

```text
projective tanh gap ~ 2 Dmax exp(-2 rho)
WR-L proper-distance gap = Dmax exp(-rho)
```

They have the same first-order Taylor approximation at the neutral point.
Thus a simple early Taylor treatment could see the shared reciprocal anchor
while being unable to select the physical profile.

## Metric-led discriminator

The complete metric decides the issue through

```text
B = h^-1(d rho,d rho),   dD/d rho = 1/sqrt(B).
```

The projective `tanh` profile requires
`B=cosh(rho)^4/Dmax^2`. The simple exponential profile requires
`B=exp(2rho)/Dmax^2`. The supplied WR-L radial slice realizes the latter
conditionally with `Dmax=2X`; no selected complete branch presently realizes
either as a universal two-observer law.

This is the precise remaining seam. It is not whether exponential behavior
exists—it does—but which complete metric branch, if any, solders reciprocal
depth to physical nonnegative separation.

## Complete depth–angle structure

The one-dimensional fractional rule cannot be used for arbitrary observer
triples. Exact unit-quaternion controls on the round `S3` branch show that
non-collinear transitions require angular dot and cross products and are
noncommutative. A constant-squashed control retains group-relative
composition while splitting angular lengths. This preserves the angular
sector instead of hiding it inside a scalar radial shortcut.

## Rulings

- reciprocal exponential response:
  `DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS`;
- anchored projective coordinate:
  `UNIQUE_GIVEN_PROJECTIVE_POSITION_INTERPRETATION`;
- fractional recentering on the ordered reciprocal ray: `DERIVED`;
- negative physical distance: `NOT_USED`;
- physical `tanh` distance:
  `OPEN_PROJECTIVE_POSITION_SOLDER`;
- simple exponential proper distance:
  `DERIVED_CONDITIONAL_IN_WRL_RADIAL_SLICE`, not global;
- exponential endpoint approach:
  `DERIVED_FOR_BOTH_BOUNDED_REGISTERED_PROFILES`;
- first-order Taylor selection between them:
  `IMPOSSIBLE_AT_LINEAR_ORDER`;
- round depth–angle transition:
  `DERIVED_CONDITIONAL_ROUND_BRANCH`;
- scalar non-collinear fractional composition:
  `REFUTED_TYPE_MISMATCH`;
- reciprocal depth equals Lorentz rapidity: `NOT_DERIVED`;
- complete coframe product as observer composition: `CHOSE_NOT_DERIVED`;
- `c` as clock–length observational anchor: retained;
- `c` alone selecting a dimensionless distance profile or endpoint:
  `NOT_DERIVED`;
- global physical `X_max`: `OPEN_NOT_PROMOTED`;
- observer-local physics: unchanged, with self-depth zero.

## Evidence

The production implementation passed 70 exact SymPy checks. A separate
stdlib/Fraction implementation, importing neither SymPy nor the production
script, passed 80 checks and 16 exercised catch-proofs. Four profile
families, round and squashed angular controls, Lorentz-algebra comparison,
coframe-gauge obstruction, and 14 hash-pinned source identities were
retained.

Repository, frozen-package, current-path, link/frontier, test, and original
dirty-checkout metadata gates are recorded in `REPOSITORY_GATES.json`.

## Maximum conclusion

`RECIPROCAL_PROJECTIVE_TRANSITION_DERIVED; PHYSICAL_DISTANCE_PROFILE_REMAINS_BRANCH_CONDITIONAL/OPEN.`

This audit does not calculate `X_max`, select a complete action or branch,
derive a signal law, alter local physics, or canonize a physical distance
formula.
