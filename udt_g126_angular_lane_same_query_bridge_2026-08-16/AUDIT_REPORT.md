# G126 angular-lane/same-query bridge audit

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_REPAIRS__NO_CURRENT_R5_TO_K_OR_PHASE_BRIDGE`

## Result

The banked R5 angular curve atlas does not currently provide an independent constraint on G125's
`K(R)` or complete screen phase on the exact G119 central-spherical observer query.

This is an exact object-type result, not a failed fit:

1. G119's spherical screen is `D_sky=R O`, with `O` orthogonal. It preserves normalized angles,
   has area magnitude `R^2`, generator `(K/R)I`, and zero shear.
2. G106's ideal per-depth reference cancels a purely radial multiplier relative to any registered
   angular footprint. Therefore that spherical branch supplies no nontrivial angular pattern to
   compare with R5.
3. Even exact `R(Z)` owns only endpoint screen position. The chain
   `K=(dR/dZ)(dZ/dlambda)` still requires the affine-frequency rate. Two explicitly
   observer-normalized positive rates preserve the same `R(Z)` and satisfy `K(1)=1`, yet produce
   different finite-depth `K` and phase.
4. R5 is a Landy--Szalay reference-projected two-point catalog-coordinate curve atlas. It is not a
   measurement of `D_sky`, `D_sky'`, `K`, or Jacobi phase, and its quadratic output cannot be
   uniquely inverted to a one-point modulation.

## Evidence gates

- preregistered in commit `33ff75f4` before executable evaluation;
- bounded to banked reports and exact finite-dimensional algebra; no observational arrays or
  protected packages were opened;
- 15/15 production symbolic checks pass;
- 12/12 independent standard-library Fraction checks pass;
- 10/10 source hashes pass, including R2's exact estimator/window construction;
- isolated replays reproduce both result JSON files byte for byte;
- fresh blind review returned `PASS_WITH_REPAIRS`; all repairs were implemented and the follow-up
  returned `PASS`.

## Lawful remaining route

An angular constraint can still arise from a metric-owned nonspherical or displaced query on the
same complete history, with its source/branch/reference semantics and affine or phase-sensitive
observable supplied. G126 does not say that future angular evidence cannot constrain UDT. It says
that fitting R5 directly to the exact spherical endpoint screen would manufacture a bridge that the
current objects do not own.

SNe is only a comparison/non-regression data set in this chain. It checks a combined predicted
redshift/brightness relation (with the registered transfer assumptions); it does not define, own,
or select a metric branch or complete history, and current SNe comparisons do not isolate a tiny
high-redshift angular contribution.

## Maximum conclusion

```text
NO_LAWFUL_CURRENT_R5_TO_K_OR_PHASE_BRIDGE
__EXACT_G119_SPHERICAL_SCREEN_IS_ANGLE_PRESERVING_AND_RADIAL_ONLY
__G106_REFERENCE_REMOVES_PURE_RADIAL_MODULATION
__PROCESSED_Z_AND_R_OF_Z_DO_NOT_OWN_AFFINE_RATE
__R5_TWO_POINT_OUTPUT_DOES_NOT_INVERT_TO_SCREEN_PHASE
__CONDITIONAL_NONSPHERICAL_HISTORY_SOURCE_REFERENCE_BRIDGE_OPEN
```

No feature, rank, BAO origin, ruler, physical history, transfer, `X_max`, CMB relation, action,
bootstrap, matter, mass, or signalling result follows.
