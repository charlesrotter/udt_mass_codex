# G225 fresh adversarial review

Date: 2026-08-22

Primary verdict:

```text
G225_ACCEPT_WITH_REPAIRS
```

Scientific grade:

```text
DERIVED_CONDITIONAL__EXTERNALLY_REVIEWED_WITH_REPAIRS
```

## Scientific finding

The bounded theorem survived adversarial review. The reviewer independently accepted:

- the signs in `omega=-g(U,k)` and the rest-screen representative `j_U[X]`;
- the identification of the observer-rest screen with the G188 quotient screen;
- the off-antipodal Rodrigues map as the unique proper least-turning map under the explicit
  common-perpendicular condition;
- passive `O(3)` and screen `O(2)` covariance without a hidden orientation;
- the exact great-circle flat control and octant quarter-turn holonomy witness;
- antipodal nonuniqueness and the global no-flat-cocycle conclusion;
- separation of the G224 scalar carry, the pointwise G225 isometry, and G188 Jacobi transport.

The reviewer found no promotion to physical transport, null-protocol selection, observer
population, or physical-history selection.

## Required repair

The aggregate verifier is correct in the repository but not relocatable to the sealed intake.
`build_review_intake.py` places frozen sources under `frozen_sources/`, while `verify_package.py`
resolves the unchanged source-manifest paths directly under the intake root. The scientific scripts
and independent replay pass, but the registered aggregate sealed replay therefore stops before
their execution.

Required repair: make `verify_package.py` resolve source-manifest rows against the intake-local
`frozen_sources/` root when that root exists, while retaining repository-relative resolution in the
repository. Rebuild a fresh sealed intake and require the aggregate verifier to exit zero there.

## Reviewer replay

- production: `39` symbolic checks, PASS;
- independent: seed `2250822`, `20,000` cases, `580,013` exact-rational assertions, `19,922`
  nontrivial composition defects, PASS;
- hostile controls: `21/21` payload and `4/4` algorithm mutations rejected;
- all three reruns exactly matched their sealed JSON artifacts;
- `31/31` payload hashes matched before and after replay.

The sealed intake remained unchanged.
