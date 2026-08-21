# G203 audit report — quiet-overlap parameter ownership

Date: 2026-08-21

## Landing

```text
INVARIANT_AFTER_AREAL_AND_DEPTH_CALIBRATION
__FOUNDING_DOES_NOT_SELECT_ORDER_LOCATION_OR_STEEPNESS
__OBSERVATIONS_MAY_CALIBRATE_A_DECLARED_FAMILY
```

Grade: `INDEPENDENTLY_VERIFIED_WITH_CAVEATS`

## Result first

The three quantities left by G202 are not arbitrary scaffolding once the primary spherical metric
is supplied:

- the crossing order is an invariant analytic-germ order;
- the quiet location is the area of a spherical symmetry orbit;
- the leading steepness is a dimensionless derivative with respect to log orbit area after the
  founded depth unit is fixed.

They are therefore native descriptors of the supplied metric profile. But the founded reciprocal
law does not choose their values. Exact regular counterexamples exist for every odd order at least
three, every positive quiet radius, and every positive steepness.

## Important boundary

This is not a return to an arbitrary “many-metrics” scaffold. The reciprocal kernel remains one
law. The counterfamily asks which allowed realization of the primary metric profile is present.
Observations may calibrate a small declared realization family without being bolted onto the
kernel. What they cannot do is turn finitely many anchors into a derivation of an unrestricted
smooth profile.

Reciprocal observer reversal also does not force the radial score to be globally odd. That would
require a separately owned action reversing the history argument, not merely the arrow depth.

## Evidence

- preregistered and pushed at `f1fa632a`;
- first symbolic run failed closed on brittle expression-order equality in an exact areal
  factorization; the repair changed it to an algebraic-zero check;
- 70/70 production symbolic assertions;
- 20,000 distinct independent exact-arithmetic cases and 280,011 assertions;
- eight frozen-source hash checks;
- ten hostile catches;
- no production import or artifact read in the independent implementation.

## Maximum conclusion

G203 classifies local descriptor ownership only. It does not select the physical profile, adopt a
mass or density bridge, fit observations, derive a global metric completion, insert `X_max`, or add
transfer, dynamics, action, source, matter, bootstrap, or signalling.
