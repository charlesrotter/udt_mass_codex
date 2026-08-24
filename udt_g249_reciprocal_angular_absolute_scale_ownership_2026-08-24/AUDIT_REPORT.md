# G249 audit report

## Result

Preregistered alternatives B and C both survive:

```text
CE_AND_RECIPROCAL_REDSHIFT_FIX_DIMENSIONLESS_CLOCK_RATIOS_NOT_ABSOLUTE_LENGTH
__POSITIVE_HOMOTHETY_PRESERVES_COMPLETE_DIMENSIONLESS_PHI_HISTORY_CAUSAL_STRUCTURE_AND_NORMALIZED_SHAPE_WHILE_JACOBI_AREA_SCALES_AS_LENGTH_SQUARED
__PHI_VALUE_ALONE_DOES_NOT_FIX_NORMALIZED_ANGULAR_RESPONSE
__FULL_DIMENSIONLESS_METRIC_AND_BRANCH_FIX_NORMALIZED_JACOBI_RESPONSE_CONDITIONALLY
__ONE_INDEPENDENT_DIMENSIONFUL_ANCHOR_REMAINS_FOR_ABSOLUTE_SCALE
```

## Positive result

The reciprocal and angular sectors are not independent fitted mechanisms. Once a complete
dimensionless metric history and a regular normalized null branch are supplied, the metric fixes
the complete normalized Jacobi response. There is no additional angular amplitude coefficient.

For the exact homothetic family,

\[
\mathcal D_\ell(\lambda)=\ell\bar{\mathcal D}(\lambda/\ell),
\qquad
A_\ell=\ell^2\bar A,
\qquad
C_\ell=\bar C,
\qquad
r_\ell=\bar r.
\]

Consequently the G248 coefficient scales as

\[
(r/A)_\ell=\ell^{-2}(r/A)_1.
\]

The interlock is therefore sensitive to absolute scale and could calibrate it from one independent
dimensional anchor after the dimensionless history is fixed.

## Negative boundary

`c_E` has dimensions length/time, while redshift and reciprocal depth are dimensionless. They
cannot alone create a length or area. The full positive homothety preserves the complete
dimensionless `phi` history, clock ratios, null cones, and normalized angular shape while changing
absolute area. The current identities therefore do not select the homothetic scale.

Moreover, equal `phi` does not fix normalized angular response: the G201 exact amplitudes depend on
the first two radial jets, and finite response depends on the full branch tidal history. A literal
single-valued `A(phi)` exists only on a declared injective branch.

## Evidence

- Production: 4,096 exact symbolic/rational cases; 61,448 assertions.
- Repaired independent: 10,000 claim-directed standard-library Fraction cases; 248,310 assertions;
  no SymPy, production import, or production-output read.
- Exact claim-class coverage: 10,000 homothety, 10,000 same-`phi` jets, 10,000 noninjective
  branches, 10,000 anchor recoveries, and 512 degree-16 two-method IVPs.
- Genuine off-diagonal Jacobi cases: 3,491 production and 8,868 independent.
- Nonunit-scale area changes: 3,888 production and 9,599 independent.
- Formula-level hostile mutations and controls: 23/23 caught; no phrase matching.
- Fitted coefficients: zero.
- Observational outcomes: closed and unread.

## Scope

This result does not select a physical history, numerical scale, observational anchor, source or
observer population, detector/transfer/luminosity law, branch aggregation, caustic completion,
`X_max`, action, source, matter, bootstrap, mass, or signalling.

External review retained the scientific landing and required claim-directed certification repairs.
The first repair-only follow-up confirmed the scientific scope and most repaired evidence, but
found that the equal-`phi` two-witness comparison and exact 23-entry hostile-ledger lock remained
incomplete. Both were separately preregistered at commit `24d0dee1`, are now implemented, and pass
the full no-write replay. Current status:
`DERIVED_CONDITIONAL__SECOND_REPAIR_COMPLETE__FOLLOWUP_PENDING`.
