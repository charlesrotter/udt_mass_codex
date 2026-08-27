# G280 preregistration — no-fit projective/optical bridge

Date: 2026-08-27

## Frozen alternatives

1. `A__CURRENT_PREMISES_FORCE_PROJECTIVE_POSITION_EQUALS_OPTICAL_AREA_RADIUS_UP_TO_ONE_HOMOTHETY`
2. `B__SAME_PROJECTIVE_PAIR_STATE_ADMITS_DIFFERENT_NATIVE_JACOBI_AREA__OPTICAL_BRIDGE_REMAINS_ADDITIONAL`
3. `C__IDENTITY_HOLDS_ONLY_ON_A_SEPARATELY_DECLARED_PRIMARY_AREAL_RADIAL_SUBSTRATUM`

Alternative A requires a derivation from the current metric/pair/Jacobi objects. Merely naming W5
state “physical position,” using a central-spherical coordinate called `R`, or importing `d_A=R`
does not satisfy it.

## Preregistered separator

Use coordinates `(u,v,x,y)` and compare

```text
g0 = -2 du dv + dx^2 + dy^2
ga = -2 du dv + dx^2 + dy^2 + a (x^2-y^2) du^2
```

for `a>0`, on the central null branch

```text
gamma(lambda)=(u=lambda,v=0,x=0,y=0),  0<=lambda<=L,
```

with `0<sqrt(a)L<pi`. Endpoint clocks and frames are assigned identically in the common
orthonormal axis frame, with an arbitrary registered longitudinal rapidity `delta`. The pair
orientation will be fixed once so the common frequency ratio is reported as `exp(delta)`.

The derivation must compute rather than assume:

- inverse metrics, connection, and curvature;
- equality of the metric and first jet along `gamma`;
- equality of parallel transport and the full endpoint frame arrow;
- equality of reciprocal depth, frequency ratio, and W5 projective state for arbitrary `delta`;
- the two screen Jacobi initial-value problems with `D(0)=0`, `D'(0)=I`;
- the endpoint determinants and their small-`a` separation.

The anticipated diagonal ordering of the two wave-screen solutions may swap with curvature sign
convention; the load-bearing criterion is convention-independent: the native Jacobi determinant
must either equal the flat value `L^2` identically or differ for some registered regular `(a,L)`.

## Certification contract

- symbolic derivation from the metric, not a typed-in curvature tensor;
- exact series check through the first nonzero determinant separation;
- at least 1,000 regular parameter cases with positive pre-caustic screen determinant;
- implementation-distinct verification that does not import the production module or result;
- hostile catches for `a=0`, deleting the transverse second jet, replacing Jacobi area by
  `ell*chi`, and promoting the imported `d_A=R` bridge to a metric identity;
- full premise audit and repository gates before banking.

## Decision rule

- Alternative A survives only if no same-projective-state separator exists and the equality is
  derived for the registered complete metric class.
- Alternative B survives if the same completed pair arrow/projective state has two distinct native
  regular Jacobi areas.
- Alternative C may coexist with B only if the equality is proved after an additional declared
  areal-radial identification; it must not be promoted to the complete class.

No observational comparison is authorized unless A survives or C is explicitly adopted later as
a conditional test premise. A B landing stops before SNe fitting.
