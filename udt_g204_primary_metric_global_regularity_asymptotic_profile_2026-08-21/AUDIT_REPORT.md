# G204 audit report — primary global regularity and asymptotics

Date: 2026-08-21

## Landing

```text
SMOOTH_CENTER_EXCLUDES_MONOTONE_TWO_SIDED_LOG_EXTENSION
__EVEN_AREAL_INNER_TROUGH_AND_OUTER_RECIPROCAL_ASYMPTOTE_FAMILY_SURVIVES
__GLOBAL_REGULARITY_DOES_NOT_SELECT_N_R0_OR_A
```

Grade: `INDEPENDENTLY_VERIFIED_WITH_CAVEATS__POST_FAILURE_REPAIR_PREREGISTERED`

## Result first

Global regularity strengthens the cohesive metric picture, but not as a unique profile selector.

The naive extension \(\phi=a[\log(r/r_0)]^n\) is singular at the areal center. A smooth center
requires \(\phi=O(r^2)\) and returns to zero depth. Therefore a genuine negative inner regime
cannot run monotonically into the center: it must form a finite trough or live on another branch.

An exact smooth-center family exists for every odd crossing order, quiet radius, and steepness:

\[
\phi=\frac{a}{2^n}(r/r_0)^2\big[(r/r_0)^2-1\big]^n.
\]

It starts at a quiet regular center, reaches one negative inner minimum, returns through the G202
quiet crossing, and grows toward a curvature-decaying outer reciprocal asymptote. This proves that
the connected behavior is mathematically available inside the primary metric without bolting on a
regime switch.

## Repair ledger

The first registered replacement had finite curvature but odd powers of \(r\), so it was not a
smooth Cartesian center. That claim was failed closed. The even-areal repair was preregistered in
`CORRECTION_PREREGISTRATION.md` at `785b0447` before its evaluation. The repair passes, but remains a
counterfamily witness rather than a selected physical profile.

## Outer boundary caution

For the surviving controls, \(f=e^{-2\phi}\to0\), curvature tends to zero, and both radial spatial
distance and null affine reach are infinite. This is not standard asymptotic flatness, because
\(f\) does not approach one. It does not derive a horizon, finite wall, `X_max`, or completion.

## Evidence

- original preregistration pushed at `ea91f45e`;
- smoothness failure and one repair preregistered at `785b0447`;
- direct full-metric Christoffel/Riemann reconstruction;
- 113/113 symbolic assertions;
- independent exact-rational sectional-curvature route: 10,000 distinct cases and 160,010
  assertions;
- 80-digit inner/outer curvature diagnostics, controlled by symbolic limits;
- 13 hostile catches and seven frozen-source hashes;
- no independent import of production code or artifacts.

## Maximum conclusion

G204 proves necessary center regularity and supplies an exact infinite survivor family. It does not
select \(n,r_0,a\), the physical profile, outer completion, observations, transfer, `X_max`,
dynamics, action, source, matter, bootstrap, mass emergence, or signalling.
