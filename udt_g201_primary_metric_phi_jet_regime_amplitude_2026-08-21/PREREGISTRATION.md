# G201 preregistration — phi-jet regime-amplitude classification

Date: 2026-08-21

Status: `PREREGISTERED_BEFORE_CONFIRMATORY_IMPLEMENTATION`

## Predicted landing

```text
TWO_SIDED_RECIPROCAL_MAGNITUDE
__ANGULAR_VOLUME_IS_PHI_JET_DEPENDENT
__NO_LOCKSTEP_LOUDNESS_FORCED
```

## Exact candidate formulas

Starting from G200,

```text
T_parallel=L^2 (r f''-f')/(2 r^3)
T_perp=L^2 (r f'-2f+2)/(2 r^4)
```

substitute `f=exp(-2 phi)` and at the normalized source set

```text
p=r phi'
q=r^2 phi''
L=r sin(alpha).
```

Preregister the dimensionless amplitudes

```text
A_parallel = r^2 T_parallel/sin(alpha)^2
A_perp     = r^2 T_perp/sin(alpha)^2.
```

## Required symbolic checks

1. Derive both `A` expressions exactly from the metric without inserting a profile.
2. Confirm the flat overlap point `phi=p=q=0` gives both modes zero.
3. Exhibit a `phi=0` jet with nonzero angular tide, proving `phi=0` alone is not quietness.
4. Exhibit arbitrary-`phi` local jets making both modes zero, proving no pointwise lower bound from
   `abs(phi)` alone.
5. Prove the exact smooth family `f=1+C r^2` has both screen tides zero wherever `f>0`, including
   sequences approaching either signed extreme when the domain permits.
6. Classify bounded-jet positive and negative extreme subclasses without promoting them to the
   general law.
7. Retain the scalar distinction: `abs(Delta phi)` is intrinsically two-sided on supplied completed
   pairs even when angular modes cancel.

## Independent verification

Use no SymPy and import no production code or artifacts.  Reconstruct the formulas from exact
`Fraction` values of `(r,f,f',f'')` and independently from exact `(phi-symbol, p, q)` algebraic
surrogates.  Require at least 10,000 arbitrary exact jet comparisons plus exact `f=1+C r^2`
controls for both signs of `C` on positive-`f` domains.

## Hostile catches

The package must catch at least:

- erasing `p` or `q`;
- forcing evenness in `phi`;
- calling `phi=0` sufficient for quietness;
- claiming either signed extreme forces nonzero angular tide;
- confusing scalar reciprocal magnitude with angular focusing;
- importing a fitted profile, `X_max`, transfer, or the G191--G198 chiral coframe.

## Falsification

The predicted landing fails if the exact G200 substitution makes both modes functions of
`abs(phi)` alone, if arbitrary-jet cancellation is impossible, if `f=1+C r^2` fails the full
metric formulas, or if independent exact replay disagrees.

## Maximum conclusion

At most classify the local primary-metric relationship among reciprocal magnitude and angular
screen amplitudes.  Do not derive the physical radial profile, a universal regime score,
observational transfer, `X_max`, time-live completion, source, matter, mass, bootstrap, or
signalling.
