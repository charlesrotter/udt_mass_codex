# G106 audit report — complete sky/depth reference projection

Date: 2026-08-15

## Result

```text
COMPLETE_SKY_DEPTH_REFERENCE_PROJECTOR_DERIVED_CONDITIONALLY
__PURE_RADIAL_MODULATION_REMOVED
__DEPTH_DEPENDENT_ANGULAR_RESPONSE_SURVIVES
__ONE_HISTORY_CROSS_WINDOW_TEST_DEFINED
__PHYSICAL_HISTORY_AND_OUTCOMES_OPEN
```

G106 derives the full regular sky/depth Jacobian and an ideal BOSS-style random-reference projection
from the frozen G105 evaluator and documented survey construction. The reference absorbs the
observed depth marginal and registered angular footprint/completeness. It removes pure radial
abundance but retains zero-angular-mean conditional structure at each depth.

For `m(zeta,n)=sum_l a_l(zeta)u_l(n)`, every redshift-window curve is a quadratic form in window
averages of the same functions `a_l`. This makes cross-window and cross-dataset variation a
falsifier of one history rather than permission to retune each window.

## Exact constructive witness

A smooth pole-fixing full-sky map has density ratio

```text
1+[(2t-1)^2/4] P2(cos theta),
```

bounded between `7/8` and `5/4`. Three equal depth windows have amplitudes

```text
13/108, 1/108, 13/108,
```

and outer/middle pair-amplitude ratio `169`. This is an outcome-blind mathematical witness, not a
selected UDT history or BAO template.

## Ownership ceiling

Open: the physical complete history, angular mode basis, source density, actual finite random
projection, global branches, nonfactorizing `H`, coefficients, and all BOSS/CMB comparisons. G106
also does not prove that the G105 all-sector local witness and the G106 global map occur in one
metric-selected completion.

## Evidence gates

1. Preregistered: PASS (`403221dc`).
2. Bounded scope: PASS; exact regular map/reference class only.
3. Independent verification: PASS WITH CAVEATS; Fraction-only replay, 12/12 hostile mutations, and
   fresh sealed read-only replay of all four executables.
4. External semantic review: `PASS_WITH_CAVEATS`; exact landing retained.
5. Premise audit: PASS; 93-row registry, bounded startup route, and repository suite
   (`90 passed, 1 xfailed`) verified.

The external caveats preserve the existing ceiling: the reference is an ideal per-stratum operator,
the scripts certify exact witnesses rather than every smooth map, and one-history consistency is a
falsifier rather than a selected cosmology.

No observational outcome was opened.
