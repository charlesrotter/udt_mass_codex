# G75 center-regular axial complete-profile family atlas — preregistration

Date: 2026-08-11

Base commit: `ac01381bf2ec624ec401f1fb13f5db013f0605e0`

## Whole question

Within the already declared stationary axial F01/F02 metric envelope, what globally specified
center-regular profile families exist from `r=0` to the symbolic comparison radius `r=R` when the
lapse, angular collapse, and mixing profile are all kept explicit? Characterize the family before
running another observer-sky solve and without selecting a profile by resemblance to CMB data.

This is a metric-led function-family atlas. It is not a physical profile, source, endpoint,
universe-size, `X_max`, bootstrap, action, matter, spectrum, or polarization calculation.

## Metric and scale

Use the exact conditional axial control metric

```text
ds^2 = -A(x) c_E^2 dt^2 + R^2 dx^2/A(x)
        + R^2 x^2(dtheta^2 + sin^2(theta)dpsi^2)
        + 2 R c_E h(x) sin^2(theta) dt dpsi,
x = r/R,  0 <= x <= 1,
A(x)=1+a x^2,
h(x)=x^2 q(x^2).
```

`R>0` remains symbolic and `c_E` remains the observed clock/ruler calibration. Neither selects a
profile. The metric is a complete four-dimensional control in this axial envelope, not the generic
ten-function complete coframe or a physical cosmological solution.

## Frozen candidate universe

Let `s=x^2`. Freeze every primitive coefficient ray

```text
p(s)=c0+c1 s+c2 s^2,
(c0,c1,c2) in {-2,-1,0,1,2}^3 \ {(0,0,0)},
gcd(nonzero |ci|)=1,
first nonzero coefficient > 0.
```

This gives exactly `49` sign-quotiented shapes. For each shape define

```text
M_p = max_{0<=s<=1} |p(s)|,
q(s) = epsilon p(s)/M_p,
epsilon in {1/20,1/5,1/2,1},
a in {-1/4,0,+1/4}.
```

The negative-`q` partner is retained analytically through the exact axial reflection
`psi -> -psi`; it is not a discarded physical branch. Add the three matched `q=0` F01 controls.
The exact universe therefore contains `49*4*3+3 = 591` profiles.

No coefficient ray, amplitude, or lapse value may be removed after classification. This is a
bounded projective quadratic atlas, not a census of all smooth even functions.

## Exact classification

For every shape/profile record, without numerical root guessing:

- exact normalization `M_p`;
- center and endpoint mixing values;
- center onset order and endpoint zero order;
- every real root in `0<s<1` and its multiplicity;
- interior sign changes versus even-multiplicity touches;
- every interior extremum;
- the exact center jet of `A`, `h`, and `B=h^2/(A x^2)`;
- Lorentz-signature and nondegeneracy conditions on the complete interval;
- reflection partner and coefficient-ray identity;
- role-neutral shape class derived from the above invariants.

Shape names may describe algebraic behavior (`CENTER_OFF`, `ENDPOINT_TAPER`, `INTERIOR_SIGN_CHANGE`,
`INTERIOR_TOUCH`, `PERSISTENT_SIGN`) but may not be labeled particle, force, CMB, micro, macro, or
physical regime.

## Numeric work allowed

Only exact rational/SymPy algebra and bounded high-precision spot checks are authorized in G75.
No geodesic, Jacobi, eigenspectrum, source, survey, ODE/PDE, or GPU solve is authorized. The next
whole-sky calculation must first choose representatives or a complete finite subfamily by an
outcome-independent rule registered after this atlas is known.

## Falsification/certification contract

- Fail if the exact coefficient-ray count is not `49` or the profile count is not `591`.
- Fail if any duplicate ray, missing ray, or nonprimitive ray survives.
- Fail if any profile is not smooth through the center in Cartesian form.
- Fail if `A<=0` anywhere on `[0,1]` or if Lorentz signature is not established.
- Fail if a root, multiplicity, endpoint order, or sign-change class depends on float tolerance.
- Fail if normalization changes the root/multiplicity class or reflection changes topology.
- Fail if a profile is selected, ranked, fitted, or described as physical.
- Fail if the original twelve G74 blocked controls are called repaired; G75 is a new preregistered
  even-in-`r` family.
- Fail if a source, spectrum, endpoint, scale, `X_max`, bootstrap rule, action, or matter law enters.

## Preregistered landings

- `CENTER_REGULAR_GLOBAL_AXIAL_FAMILY_NONEMPTY`;
- `CENTER_REGULAR_FAMILY_HAS_MULTIPLE_EXACT_SHAPE_STRATA`;
- `BOUNDED_QUADRATIC_ATLAS_DEGENERATE_OR_INCOMPLETE`;
- `TYPE_OR_IMPLEMENTATION_FAILURE`.

## Maximum conclusion

An exact role-neutral classification of the 591-member center-regular axial control family and a
principled finite input universe for a later global observer-sky solve. No physical profile or CMB
prediction may be claimed.

