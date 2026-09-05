# G348 map — generic Lorentzian null-screen area theorem

Date: 2026-09-04
Status: preregistration stage

## Whole question

Starting from the metric alone, determine whether G343--G347's quotient-screen propagation,
symplectic reversal, two directional infinitesimal angular-area maps, and arbitrary endpoint-
observer covariance hold on every supplied smooth affinely parameterized null geodesic segment in
an arbitrary time-oriented four-dimensional Lorentzian spacetime.

This is `METRIC_LED` and observing rather than targeting. It tests whether the previous exact
Taub/Kasner calculation exposed a general metric theorem. It does not select a spacetime, ray,
observer, history, topology, distance, scale, or physical population.

## Exact bounded arena

- a supplied smooth time-oriented four-dimensional Lorentzian metric `g`;
- a supplied regular affinely parameterized future null geodesic `gamma` with nonzero tangent `k`;
- arbitrary ordered finite endpoints on that one segment;
- arbitrary finite future unit timelike observers at the endpoints;
- the full rank-two quotient screen `Q=k^perp/span(k)` and all of its Jacobi directions;
- every rank of the endpoint position block `B`: two, one, or zero;
- arbitrary positive common affine rescaling and arbitrary endpoint screen coordinates.

“Regular segment” means the metric and nonzero geodesic tangent are regular. It does not exclude
conjugate points or rank loss.

## Pure and easy routes

- Pure route used here: construct the quotient connection and curvature endomorphism from the
  Levi-Civita connection, derive the Jacobi phase flow and all endpoint laws directly.
- Easier but forbidden as proof: quote geometric-optics, Etherington, brightness, flux, luminosity,
  detector, or observational-distance theorems.

Standard ODE, linear algebra, and symplectic methods are category-A mathematical tools. They do not
add physics to the metric.

## Candidate structure

For quotient classes `x,y` along `gamma`, test whether the metric defines

```text
D[x]/dlambda = [nabla_k X],
T[x] = [R(X,k)k],
D^2 x/dlambda^2 + T x = 0.
```

With `p=Dx/dlambda`, test whether the phase propagator

```text
(x_1,p_1) = M_10 (x_0,p_0),
M_10 = [[A,B],[C,D]]
```

is symplectic, composes, reverses by inverse, and obeys `B_01=-B_10^*` in one common affine gauge.
For endpoint frequency `omega_i=-g(k,u_i)>0`, test

```text
A_(1<-0) = omega_0^2 |det B_10|,
A_(0<-1) = omega_1^2 |det B_01|,
A_(1<-0)/A_(0<-1) = (omega_0/omega_1)^2.
```

The determinant is intrinsic only after using the endpoint quotient metrics; in arbitrary frames
their area forms must be retained exactly.

## Singular and orientation branches

The theorem must not assume `det B>0` or delete conjugate endpoints.

- `rank B=2`: the type-I endpoint generator, inverse determinant scalar, and stationary determinant
  sewing may be used on that chart.
- `rank B=1` or `0`: the directional area is zero and the inverse determinant scalar/type-I
  generator is singular, while the full symplectic phase map remains invertible.
- the sign of oriented `det B` is meaningful only after compatible endpoint orientations are
  supplied; the orientation-free area uses `|det B|`;
- across a finite-order zero, the oriented sign changes exactly when the determinant's zero order
  is odd. Rank alone does not settle a degenerate crossing. A simple rank-one crossing flips sign;
  a transverse rank-zero double crossing does not.

## Required classifications

1. Prove the quotient connection is well defined and its metric curvature operator self-adjoint.
2. Derive the full phase-space symplectic law without a coordinate or field-equation ansatz.
3. Derive composition, reversal, affine typing, and screen-coordinate covariance.
4. Derive both directional areas and arbitrary endpoint-observer factors.
5. Retain and classify rank-two, rank-one, rank-zero, coincidence, and noncoincident conjugate cases.
6. State exactly where generator, inverse determinant, and stationary sewing charts fail.
7. Separate oriented sign from positive metric area and avoid a false global positivity claim.
8. State all supplied spacetime, geodesic, endpoint, observer, path, and operational dependence.

## Maximum conclusion

At most G348 may establish that G343--G347's infinitesimal quotient-screen, reversal, area, and
observer-covariance structure is a coordinate-free consequence of any supplied regular Lorentzian
null geodesic, with explicit conjugate/rank-loss qualifications. It may not establish finite-beam
evolution, a light or transfer law, brightness, flux, luminosity, probability, observational
distance, preferred observer/route/population, generic spacetime evolution, occupancy, stability,
matter/mass, scale, `X_max`, or canon.
