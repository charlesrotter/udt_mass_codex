# G346 preregistration — directional angular-area reciprocity

Date: 2026-09-04
Outcome status: analytic, computational, and independent-replay outcomes unseen

## Frozen question and domain

Freeze the G340 endpoint metric frequencies, G342 source-sky Jacobi normalization, G343 common-
affine and endpoint-reset typing, G344 stationary endpoint algebra, and G345 accepted symmetric
scalar on one supplied exact Taub/Kasner spacetime and one supplied fixed labelled null ray. Cover
every distinct positive endpoint pair, every nonidentity ordered triple, every projective direction
including both axes, arbitrary marked events, arbitrary common positive affine rescalings,
arbitrary well-conditioned invertible endpoint screen coordinates, separately unit-frequency
source conventions, and every supplied compact lift separately.

This is an infinitesimal metric screen-area per metric sky-solid-angle question. No finite-beam,
brightness, flux, luminosity, probability, electromagnetic transfer, detector, observational-
distance selection, source, route weighting, matter, scale, `X_max`, or observational outcome may
enter.

## Preregistered primary alternatives

1. `A__TWO_DIRECTIONAL_METRIC_ANGULAR_AREA_JACOBIANS_CLOSE_WITH_FREQUENCY_RECIPROCITY`:
   both Jacobians are positive and coordinate/affine invariant, their ratio is the squared endpoint
   frequency ratio, their geometric mean is exactly `1/Dhat`, and stationary sewing closes with
   the G345 normalized join Hessian.
2. `B__DIRECTIONAL_JACOBIANS_EXIST_BUT_FREQUENCY_REVERSAL_OR_GEOMETRIC_MEAN_FAILS`:
   the metric areas are well typed, but at least one proposed exact relation to endpoint frequency
   or G345 fails.
3. `C__ORTHONORMAL_DIRECTIONAL_FORM_EXISTS_BUT_GENERAL_SCREEN_COORDINATES_REQUIRE_EXTRA_STRUCTURE`:
   a coefficient can be written only after an unowned frame choice.
4. `D__NO_TWO_ENDPOINT_METRIC_ANGULAR_AREA_JACOBIAN_CLOSES_ON_THE_FULL_BOUNDED_DOMAIN`:
   at least one affine, reference, composition, reversal, principal, or compact-label gate fails.

## Preregistered secondary alternatives

- reversal: `R1__SQUARED_METRIC_FREQUENCY_RATIO` or `R2__OTHER_OR_UNCLOSED_FACTOR`;
- symmetric scalar: `G1__INVERSE_G345_IS_EXACT_GEOMETRIC_MEAN` or
  `G2__AGREEMENT_ONLY_PARTIAL_OR_FALSE`;
- composition: `C1__NORMALIZED_STATIONARY_HESSIAN_SEWING_CLOSES` or
  `C2__NO_TYPED_DIRECTIONAL_SEWING_LAW`;
- screen covariance: `S1__GENERAL_GL2_METRIC_AREA_CONTRACTION_CLOSES` or
  `S2__ONLY_ORTHONORMAL_O2_FORM_EXISTS`;
- physical typing: `N1__INFINITESIMAL_CAUSAL_GEOMETRY_ONLY` or
  `N2__EXISTING_PREMISES_SELECT_BRIGHTNESS_OR_OBSERVATIONAL_DISTANCE`;
- quotient: `Q1__PER_LIFT_JACOBIANS_ONLY` or `Q2__QUOTIENT_FORCES_A_SUM_OR_SELECTION`.

`N2` and `Q2` require an actual derivation from the frozen inputs. They may not be inferred from a
successful angular-area construction.

## Frozen definitions and candidate formulas

Under passive endpoint coordinate changes

```text
x_i'     = R_i x_i,
theta_i' = R_i theta_i,
p_i'     = R_i^-T p_i,
q_i'     = R_i^-T q_i R_i^-1,
B_10'    = R_1 B_10 R_0^T.
```

Freeze the metric attachment

```text
p_i      = omega_i q_i theta_i,
dOmega_i = sqrt(det q_i) d^2 theta_i,
dA_i     = sqrt(det q_i) d^2 x_i.
```

and test

```text
J_1<-0 = omega_0^2 abs(det B_10) sqrt(det q_1 det q_0),
J_0<-1 = omega_1^2 abs(det B_01) sqrt(det q_0 det q_1).
```

In one common affine gauge, with `r_10=omega_0/omega_1`, freeze

```text
J_1<-0 / J_0<-1 = r_10^2,
G_10 := sqrt(J_1<-0 J_0<-1) = 1/Dhat_10.
```

In endpoint-0 unit-frequency convention put `alpha_01=omega_1/omega_0`. G343 freezes

```text
B_01^[1] = -alpha_01 (B_10^[0])^T,
J_0<-1^[1] = alpha_01^2 J_1<-0^[0],
sqrt(J_1<-0^[0] J_0<-1^[1]) = alpha_01 J_1<-0^[0] = 1/Dhat_10.
```

For a three-endpoint stationary join, freeze

```text
hhat_1 = abs(det H_1)/(omega_1^2 det q_1),
J_2<-0 = hhat_1 J_2<-1 J_1<-0.
```

For the reference-free mixed direction define

```text
h_i = sqrt(T_i^2 + lambda^2),
Jp  = integral[T0,T1] u^(4/3)/(u^2+lambda^2)^(3/2) du,
Jz  = integral[T0,T1] u^(-2/3)/(u^2+lambda^2)^(1/2) du,
G_10 = h_0^2 h_1^2 abs(Jp Jz)/(T_0 T_1)^(1/3),
r_10 = (T_1/T_0)^(2/3) h_0/h_1,
J_1<-0 = G_10 r_10,
J_0<-1 = G_10/r_10.
```

Freeze the principal formulas, with `du=T_1^(2/3)-T_0^(2/3)`,

```text
J_1<-0,X = (9/4) T_0^(2/3) du^2,
J_0<-1,X = (9/4) T_1^(2/3) du^2,

P = abs((T_1^(7/3)-T_0^(7/3))(T_1^(1/3)-T_0^(1/3))),
J_1<-0,perp = (9/7) P T_1^(1/3)/T_0,
J_0<-1,perp = (9/7) P T_0^(1/3)/T_1.
```

At coincidence both directional Jacobians must satisfy

```text
J_directional / abs(T_1-T_0)^2 -> 1.
```

Any correction to these frozen formulas after execution is a preregistered failure and must be
recorded before rerun.

## Required derivation and evidence

1. Derive `p=omega q theta` from fixed-frequency null-direction variation and derive the two metric
   area forms; do not identify them through a borrowed optical theorem.
2. Derive general `GL(2)` covariance with canonical momentum transformation. Oriented and absolute
   Jacobians must be distinguished.
3. Derive common-gauge and separately source-normalized reversal from G343, including every
   `alpha_01` power.
4. Derive the exact relation to G345 algebraically for general positive `q_i`, not only in
   orthonormal or principal cases.
5. Derive stationary composition from `H_1=B_21^-1 B_20 B_10^-1`; test all six endpoint orderings
   and classify the `T_2=T_0` identity singularity rather than hiding it.
6. Production must execute at least 10,000 checks over logarithmic endpoint pairs/triples,
   mixed/near-axis/exact-axis directions, reference events, affine scales, general well-conditioned
   `GL(2)` endpoint frames, and endpoint normalization resets.
7. An implementation-distinct verifier may not import production or G342--G345 code. It must rebuild
   the frequencies, scalar fundamental solutions, `B`, sky musical map, and metric area ratios by a
   distinct route for at least 4,000 checks.
8. Raw double-precision relative tolerance is `8e-9` for quadrature/block comparisons and `6e-8`
   for preregistered general-frame determinant checks. Exact algebraic identities are required where
   available.
9. Both principal limits must agree with the frozen formulas; analytic positivity must cover the
   full noncoincident bounded domain. Coincidence is a limit, not an included type-I chart point.
10. Hostile mutations must catch at least: omit one `omega_0` power, use `omega_1` in the forward
    map, omit either endpoint metric area, use a frequency product instead of ratio for reversal,
    reverse the frequency ratio, replace the geometric mean by an arithmetic mean, compare to
    `Dhat` instead of its inverse, transpose `B` without the endpoint reset factor, use the wrong
    `GL(2)` transformation, assert bare multiplicative sewing, invert `hhat_1`, hide `T_*=1`, delete
    one principal direction, sum/select compact lifts, and promote the result to brightness, flux,
    luminosity, probability, distance, scale, or a light law.
11. Every executable must run with `python3 -S`, support `UDT_NO_WRITE=1`, and preserve package
    evidence bytes during no-write replay.

## Premise and completeness gate

This is one exact-spacetime, one-normal-observer-congruence, one-fixed-ray-family infinitesimal
endpoint tile. Both screen directions and the full positive noncoincident endpoint domain remain
live. Generic G332 developments, accelerated observers, finite beams, emission and detection,
path/observer populations, matter, and radiative transfer are omitted and may carry additional
structure.

## Maximum conclusion

The maximum landing is two exact, independently checked directional infinitesimal metric angular-
area Jacobians on the supplied bounded G340--G345 family, together with their frequency reversal,
G345 geometric mean, and stationary sewing. No result may be called brightness, flux, luminosity,
probability, amplitude, a selected observational distance, a native light law, physical route or
population, scale, `X_max`, generic UDT prediction, or canon.
