# G345 preregistration — observer-calibrated endpoint screen scalar

Date: 2026-09-04
Outcome status: analytic, computational, and independent-replay outcomes unseen

## Frozen question and domain

Freeze the G340 normal-observer frequency ratio, the G343 common-affine endpoint typing, and the
G344 mixed-Hessian screen bidensity on one supplied exact Taub/Kasner spacetime and one supplied
fixed labelled null ray. Cover every distinct positive endpoint pair, every nonidentity ordered
triple, every projective direction including both axes, arbitrary marked events, arbitrary common
positive affine rescalings, arbitrary invertible endpoint screen-coordinate changes with the
metric screen forms transformed covariantly, and every supplied compact lift separately.

The tested object is a scalar contraction of already-derived metric data. It is not a new response
law. No electromagnetic transfer, luminosity, flux, probability, observational distance, source,
detector, route weighting, matter, scale, `X_max`, or observational outcome may enter.

## Preregistered primary alternatives

1. `A__ENDPOINT_CLOCKS_AND_METRIC_SCREEN_AREAS_CLOSE_ONE_AFFINE_AND_SCREEN_INVARIANT_SCALAR`:
   `Dhat=Delta/(omega_1 omega_0)` in orthonormal screens has exact affine, reference, screen,
   reversal, stationary-composition, and principal-limit closure on the full bounded domain.
2. `B__COMMON_AFFINE_WEIGHT_CANCELS_BUT_ENDPOINT_RESET_OR_REVERSAL_FAILS`:
   the frequency product removes common affine units but the separately normalized endpoint maps
   cannot be reconciled without extra operational structure.
3. `C__CLOCK_WEIGHT_CANCELS_BUT_GENERAL_SCREEN_SCALARIZATION_REQUIRES_UNOWNED_STRUCTURE`:
   orthonormal coefficients agree but the metric screen area forms do not furnish a coordinate
   scalar under general endpoint frame changes.
4. `D__NO_METRIC_OWNED_ENDPOINT_CONTRACTION_CLOSES_ALL_REQUIRED_TYPES`:
   at least one affine, reference, composition, reversal, principal, or compact-label gate fails.

## Preregistered secondary alternatives

- monomial classification:
  `U1__UNIQUE_IN_SYMMETRIC_FIRST_POWER_DETERMINANT_MONOMIAL_CLASS` or
  `U2__EVEN_THAT_RESTRICTED_CLASS_RETAINS_AN_EXPONENT_FREEDOM`;
- physical uniqueness:
  `N1__COORDINATE_SCALAR_ONLY_NOT_A_UNIQUE_PHYSICAL_OBSERVABLE` or
  `N2__EXISTING_PREMISES_SELECT_A_UNIQUE_LIGHT_OR_DISTANCE_READOUT`;
- composition:
  `C1__NORMALIZED_STATIONARY_HESSIAN_SEWING_CLOSES` or
  `C2__NO_TYPED_THREE_ENDPOINT_SEWING_LAW_EXISTS`;
- reversal:
  `R1__NORMALIZED_TENSOR_TRANSPOSE_AND_SCALAR_SYMMETRY_CLOSE` or
  `R2__A_DIRECTIONAL_DEFECT_REMAINS`;
- screen covariance:
  `S1__METRIC_AREA_CONTRACTION_CLOSES_UNDER_GENERAL_GL2_COORDINATES` or
  `S2__ONLY_ORTHONORMAL_O2_COVARIANCE_IS_AVAILABLE`;
- quotient:
  `Q1__PER_LIFT_SCALAR_ONLY` or `Q2__QUOTIENT_FORCES_A_SUM_OR_SELECTION`.

`N2` and `Q2` require an actual derivation from the sealed inputs; they may not be inferred from a
successful scalarization.

## Frozen candidate formulas

For endpoint screen metrics `q_i`, frequencies `omega_i`, G344 mixed Hessian `K_10`, and stationary
Hessian `H_1`, test

```text
Khat_10 = K_10 / sqrt(omega_1 omega_0),
Dhat_10 = abs(det K_10)
          / (omega_1 omega_0 sqrt(det q_1 det q_0)),
hhat_1  = abs(det(H_1 / omega_1)) / det(q_1),
Dhat_20 = Dhat_21 Dhat_10 / hhat_1.
```

In endpoint-0 unit-frequency convention, with
`alpha_01=omega_1/omega_0`, freeze the candidate comparison

```text
Dhat_forward^[0] = Delta_forward^[0] / alpha_01,
Dhat_reverse^[1] = Delta_reverse^[1] / (1/alpha_01),
Delta_reverse^[1] = Delta_forward^[0] / alpha_01^2.
```

For mixed direction `lambda`, define

```text
h(T)  = sqrt(T^2 + lambda^2),
Jp    = integral[T0,T1] u^(4/3)/(u^2+lambda^2)^(3/2) du,
Jz    = integral[T0,T1] u^(-2/3)/(u^2+lambda^2)^(1/2) du.
```

Freeze the reference-free candidate

```text
Dhat_10 = (T0 T1)^(1/3)
          / ((T0^2+lambda^2)(T1^2+lambda^2) abs(Jp Jz)).
```

and principal candidates

```text
Dhat_X = 4 / (9 (T0 T1)^(1/3) (T1^(2/3)-T0^(2/3))^2),
Dhat_perp = 7 (T0 T1)^(1/3)
            / (9 abs((T1^(7/3)-T0^(7/3))
                     (T1^(1/3)-T0^(1/3)))).
```

Any correction to these frozen formulas after execution is a preregistered failure and must be
recorded before rerun.

## Required derivation and evidence

1. Derive the affine exponents algebraically. For `Delta omega_0^a omega_1^b`, common-affine
   invariance and reversal symmetry must be solved as equations, not sampled.
2. Derive general `GL(2)` endpoint coordinate covariance with canonical momentum transformation
   and transformed metric screen forms. Oriented signs and the absolute scalar must be separated.
3. Derive common-gauge reversal and separately source-normalized reversal from G343, including the
   exact `alpha_01` factors.
4. Derive stationary composition with the normalized joined Hessian. Test all six endpoint
   orderings and classify the `T_2=T_0` identity singularity rather than hiding it.
5. Production must execute at least 9,000 checks over logarithmic endpoint pairs/triples,
   mixed/near-axis/exact-axis directions, reference events, affine scales, general well-conditioned
   `GL(2)` endpoint frames, and endpoint normalization resets.
6. An implementation-distinct verifier may not import production or G343/G344 code. It must rebuild
   frequencies, scalar fundamental solutions, `B`, and determinant contractions from the metric
   formulas through a distinct route for at least 3,000 checks.
7. Raw double-precision relative tolerance is `7e-9` for quadrature/block comparisons and `5e-8`
   for ill-conditioned but preregistered general-frame determinant checks. Exact algebraic identities
   are required where available.
8. Coincidence must satisfy `Dhat abs(T1-T0)^2 -> 1`; both exact principal formulas must agree with
   mixed-direction limits. No sampled absence of a defect may replace analytic positivity.
9. Hostile mutations must catch at least: omit either endpoint frequency, use only a frequency
   ratio, divide `Delta` by `sqrt(omega_0 omega_1)`, multiply instead of divide, omit either metric
   screen determinant, use the wrong general-frame transformation, drop the absolute value, assert
   naive multiplicative composition, omit `omega_1^2` from the joined Hessian, mix independently
   normalized segment gauges, hide `T_*=1`, select/sum compact lifts, and promote the scalar to
   flux, luminosity, probability, distance, scale, or a light law.
10. Every executable must run with `python3 -S`, support `UDT_NO_WRITE=1`, and preserve package
    evidence bytes during no-write replay.

## Premise and completeness gate

This is one exact-spacetime, one-normal-observer-congruence, one-fixed-ray-family endpoint tile.
The complete linear two-screen determinant and full positive noncoincident endpoint domain are
live. Generic G332 developments, accelerated observers, nonlinear finite beams, emission and
detection, path/observer populations, matter, and radiative transfer are omitted and may carry
additional structure.

## Maximum conclusion

The maximum landing is an exact, independently checked observer-calibrated endpoint screen
determinant scalar on the supplied bounded G340--G344 family, with uniqueness only in the stated
symmetric first-power monomial class. It remains conditional on the supplied spacetime, normal
observers, ray, and compact label. No result may be called a luminosity, flux, probability,
amplitude, observational distance, native light law, physical route/population, scale, `X_max`,
generic UDT prediction, or canon.
