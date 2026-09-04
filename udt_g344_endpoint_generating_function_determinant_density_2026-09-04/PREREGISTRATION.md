# G344 preregistration — endpoint generating function and determinant density

Date: 2026-09-04
Outcome status: analytic, computational, and independent-replay outcomes unseen

## Frozen question and inputs

Freeze the exact G343 `4 x 4` symplectic propagator on the regular `T>0` component, one supplied
fixed labelled null ray and compact lift, one common affine parameter, the G341 parallel quotient
screen, arbitrary distinct positive endpoint pairs and ordered triples, all projective directions
including both axes, arbitrary positive reference events and affine scales, and arbitrary endpoint
screen positions. No screen component is frozen.

The candidate is the type-I homogeneous quadratic endpoint generator in common-affine canonical
coordinates. Its mixed-Hessian determinant must be reported as an oriented bidensity and as an
absolute positive density, with all affine and screen-basis weights visible. Coincident endpoints
are an excluded chart boundary because `B=0` there; their limiting singularity must still be
classified.

No luminosity, electromagnetic transfer, source spectrum, detector, flux law, probability,
observational distance, physical route/population, topology selection, matter model, physical
scale, `X_max`, stability criterion, or canon claim may enter.

## Preregistered primary alternatives

1. `A__GLOBAL_NONCOINCIDENT_TYPE_I_GENERATOR_AND_TYPED_DETERMINANT_DENSITY_CLOSE`:
   the full screen `B` block is invertible for every distinct positive endpoint pair and direction;
   one quadratic generator recovers the exact G343 map; its mixed-Hessian determinant is regular
   and nonzero on that domain and obeys exact typed composition, reversal, and covariance laws.
2. `B__GENERATOR_EXISTS_ONLY_PIECEWISE_BECAUSE_AN_INTERIOR_CAUSTIC_OR_BLOCK_ZERO_OCCURS`:
   one or both screen `B` eigenvalues vanish away from coincidence, so multiple generating charts
   or a caustic index are required.
3. `C__CANONICAL_GENERATOR_CLOSES_BUT_DETERMINANT_REQUIRES_UNOWNED_ENDPOINT_STRUCTURE`:
   the map has a generator, but no honest screen bidensity can be formed without importing an
   endpoint measure, light law, or extra normalization.
4. `D__NO_SINGLE_ENDPOINT_GENERATOR_REPRODUCES_THE_G343_MAP`:
   the block Hessians fail symmetry, reconstruction, reference covariance, or a principal limit.

## Preregistered secondary alternatives

- composition: `C1__EXACT_STATIONARY_GLUE_AND_HESSIAN_DETERMINANT_LAW` or
  `C2__GENERATOR_COMPOSITION_NEEDS_EXTRA_PATH_DATA`;
- reversal: `R1__COMMON_AFFINE_ACTION_ANTISYMMETRY_AND_DENSITY_SYMMETRY` or
  `R2__REVERSAL_FAILS_OR_NEEDS_AN_UNOWNED_PHASE`;
- affine units: `A1__GENERATOR_AND_DENSITY_HAVE_DERIVED_COMMON_AFFINE_WEIGHTS_AND_SEPARATE_ENDPOINT_UNITS_ARE_EXPLICITLY_NONCANONICAL`
  or `A2__A_GAUGE_INVARIANT_SCALAR_DETERMINANT_EMERGES_WITHOUT_ATTACHMENT`;
- screen bases: `S1__GENERATOR_IS_SCALAR_AND_MIXED_HESSIAN_IS_AN_ENDPOINT_BIDENSITY` or
  `S2__AN_ENDPOINT_FRAME_OR_ORIENTATION_DEFECT_REMAINS`;
- principal directions: `P1__BOTH_LIMITS_REGULAR_AWAY_FROM_COINCIDENCE` or
  `P2__ONE_LIMIT_REQUIRES_A_DIFFERENT_GENERATING_CHART`;
- quotient: `Q1__PER_LIFT_GENERATOR_AND_DENSITY_ONLY` or
  `Q2__QUOTIENT_IDENTIFICATION_FORCES_A_SUM_OR_SELECTION`.

## Frozen candidate formulas to test

For `M=[[A,B],[C,D]]`, if `B` is invertible, test rather than assume

```text
S10(x1,x0) = 1/2 x1^T D B^-1 x1
            - x0^T B^-1 x1
            + 1/2 x0^T B^-1 A x0,

p1 = +dS10/dx1,
p0 = -dS10/dx0,
K10 = -d^2 S10/(dx1 dx0) = B^-T,
Delta10 = abs(det K10) = 1/abs(det B).
```

These formulas are candidates frozen before evaluation. Symmetry of `D B^-1` and `B^-1 A`, the
identity `C-D B^-1 A=-B^-T`, and all covariance laws must be derived from or checked against G343.

For composition through `x1`, preregister the candidate stationary Hessian

```text
H1 = B21^-1 A21 + D10 B10^-1
   = B21^-1 B20 B10^-1,
```

and candidate density law

```text
Delta20 = Delta21 Delta10 / abs(det H1).
```

Any sign, transpose, or endpoint-order correction revealed after execution is a failed frozen
candidate and requires a recorded repair before rerun.

## Required derivation and evidence

1. Prove analytically from G343's positive scalar solutions and signed reduction-of-order
   integrals that each `B_j` vanishes only at coincidence. Do not infer this from sampled grids.
2. Derive the generator, its three endpoint Hessians, and exact recovery of `A,B,C,D`. Establish
   uniqueness up to one additive constant in each connected endpoint-order component.
3. Prove stationary composition and determinant gluing for all triples whose total endpoints are
   distinct. Explicitly classify the singular identity case `T2=T0` rather than hiding it.
4. Prove common-affine reversal, the affine weights of `S` and `Delta`, reference-event covariance,
   and independent endpoint `O(2)` screen-basis covariance. Classify separately normalized endpoint
   frequency units; do not call a conformally symplectic map canonical.
5. Recover G342's source-vertex `det B` and derive exact longitudinal and transverse principal
   formulas. Retain compact lifts as labels without summing or selecting them.
6. Production must cover at least 8,000 checks over logarithmic endpoint pairs/triples, reference
   events, mixed/near-axis/exact-axis directions, affine rescalings, endpoint vectors, and endpoint
   screen rotations/reflections.
7. Independent code may not import production or G343 implementation. It must rebuild the G343
   scalar fundamental bases and verify generator derivatives, stationary composition, density,
   reversal, and covariance through a distinct route for at least 3,000 checks.
8. Raw double-precision relative tolerance is `5e-9` for exact-block/quadrature comparisons and
   `3e-7` for any independent finite-difference derivative or ODE control. Exact algebraic
   identities are required where available.
9. Hostile mutations must catch at least: wrong cross-Hessian transpose, wrong source sign,
   swapped `A/D`, missing inverse on `B`, dropped absolute value, false affine invariance, treating
   independent endpoint frequency resets as canonical, broken composition order, omitted stationary
   Hessian, hidden reference scale, lost principal limit, injected screen mixing, deleted compact
   label, and promotion to luminosity/distance/probability/scale.
10. Every executable must run with `python3 -S`, support `UDT_NO_WRITE=1`, and preserve package
    evidence bytes during no-write replay.

## Premise and completeness gate

This is one exact-spacetime, one-observer-congruence, one-null-ray-family tile. The complete linear
two-screen phase space and full noncoincident endpoint domain are live. Generic G332 developments,
perturbed metrics, accelerated observers, nonlinear finite beams, physical route population,
matter, and radiative transfer are omitted and may carry additional structure. The test
characterizes every member of the stated tile; it does not select solutions by optical merit.

## Maximum conclusion

The maximum allowed landing is an exact, independently checked, globally noncoincident endpoint
generator and typed screen determinant-density classification on the supplied G343 spacetime and
supplied labelled null rays. No result may be called a light action, luminosity/flux prediction,
probability amplitude, observational distance, selected signal path, generic UDT spacetime,
physical scale, `X_max`, stability theorem, or canon.
