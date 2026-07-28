# P02 preregistration: stratified full-local-jet atlas

Date: 2026-07-27

## Whole question

For the registered complete triangular coframe, which exact causal,
coordinate-time, angular-shape, shift-rank, derivative-rank, and collective
Hessian-rank strata admit bounded local two-jet witnesses, and what local
curvature structures occur on those witnesses?

This is a metric-led atlas of local off-shell jets.  It is not a field-equation
solve, physical time evolution, global finite-cell completion, or search for a
particle, lightlike branch, repeated direction, action, or cosmology.

## Local coframe and jet arena

At one regular point in coordinates `(x0,x,y,z)`, use

```text
theta0 = exp(-phi) dx0
theta1 = exp(+phi) dx
(theta2,theta3)^T = D[(dy,dz)^T+S(dx0,dx)^T]

D = [[exp(sigma/2-alpha), k exp(sigma/2-alpha)],
     [0,                       exp(sigma/2+alpha)]].
```

All eight chart amplitudes

```text
(phi,sigma,alpha,k,S10,S11,S20,S21)
```

have independent point values, four-coordinate first jets, and symmetric
four-coordinate second jets, subject only to the exact registered stratum.
The 120 local numbers are a `CHOSE` configuration arena, not 120 physical
fields or degrees of freedom.  Only the reciprocal role of `phi` is founded.

## Frozen Cartesian stratum universe

Cross every value of all eight axes in `AXIS_CONTRACT.tsv`:

```text
shell:                0.30, 1.00
coordinate_time:      DYNAMIC_4D, COORDINATE_STATIC
phi_gradient:         ZERO, TIMELIKE, NULL, SPACELIKE
angular_shape:        ISOTROPIC, DIAGONAL_ANISOTROPIC, SHEARED
shift_value_rank:     0,1,2
angular_first_rank:   0,1,2,3
shift_first_rank:     0,1,2,3,4
collective_Hessian:   0,1,4,8
```

This gives exactly 11,520 strata.  Generate two attempts per stratum, 23,040
attempts total, in the lexicographic order frozen by `SAMPLING_CONTRACT.json`.
No generated record may be omitted.

`COORDINATE_STATIC` means every first derivative in the `x0` coordinate and
every Hessian component containing `x0` is exactly zero.  This is a chart
stratum, not a claim of invariant or physical staticity.

The angular first-rank is the matrix rank of the `(sigma,alpha,k)` first jets.
The shift first-rank is the matrix rank of the four `S` first jets.  Collective
Hessian rank is the matrix rank of the eight amplitude Hessians after symmetric
components are flattened.  These are chart-stratification labels.

## Construction and incompatibility

For dynamic jets, construct `dphi` in the orthonormal coframe with exact norm
`-shell^2`, `0`, or `+shell^2`, then transform it to coordinate components.
For coordinate-static jets require `partial_0 phi=0` and determine from the
spatial inverse-metric block whether the requested causal class has a witness.
If it does not, retain the attempt as `NO_CAUSAL_WITNESS_AT_SAMPLED_VALUE`.

Rank matrices are constructed by deterministic thin factorizations and
verified by singular values.  A coordinate-static shift first-rank 4 and a
coordinate-static collective Hessian rank 8 are structurally impossible
because only three derivative columns and six spatial Hessian components
remain; retain them as `STRUCTURALLY_INCOMPATIBLE_RANK`.

No rank or causal failure may be repaired by changing another registered axis,
retuning a tolerance, or replacing the sampled value.

## Deterministic numerical universe

Use one scrambled Sobol sequence of dimension 256 and seed `20260728`.  Draw
2^15 points and consume the first 23,040 in exact stratum-major,
replicate-minor order.  Map controls to `[-1,+1]` and apply the deterministic
construction in the evaluator.  The unused tail is discarded before outcomes
and is not another candidate set.

Production:

```text
device                  one Tesla V100-PCIE-32GB process
dtype                   float64
batch                   512 attempts
attempts                23,040
estimated peak          below 2 GiB
hard timeout            15 minutes
independent CPU anchors 64 constructed attempts
```

The shells and sampling distribution are `pinned-by-HABIT` exploration
controls, not physical scales or probability measures.

## Computed local objects

For every constructed witness compute the coframe, metric, inverse metric,
complete four-coordinate first and second metric jets, Levi-Civita connection,
Riemann tensor, Ricci tensor, scalar curvature, Kretschmann scalar, frame
Riemann tensor, six-by-six curvature operator, screen-tidal discriminant,
pair/screen Ricci mixing, angular/base sectional components, determinant
control, causal norm, realized ranks, and numerical-finiteness flags.

The assigned pair/screen split and all component ranks are conditional on the
registered triangular chart.  Scalar curvature, Kretschmann, determinant, and
causal norm are metric readouts.

## Controls and certification

Before production:

1. zero jets produce Minkowski metric and zero curvature;
2. arbitrary constant values with zero derivatives produce a constant flat
   metric;
3. `det(g)=-exp(2 sigma)`;
4. every claimed construction reproduces its exact causal and rank labels to
   the frozen tolerances;
5. scalar curvature and `dphi` norm are invariant under an independently
   applied constant Lorentz coframe change;
6. a separate NumPy implementation using fourth-order finite differences on
   local Taylor amplitudes agrees on 64 constructed attempts without importing
   the GPU evaluator; and
7. coefficient/stratum hashes replay deterministically.

Stop for any construction falsely labeled successful, any failed flat or
determinant control, another GPU process on the V100, peak allocation above
2 GiB, CUDA failure/OOM, or more than 1% nonfinite curvature among constructed
shell-0.30 witnesses or 5% among constructed shell-1.00 witnesses.

An incompatible or no-witness stratum is a classified atlas outcome, not a
numerical failure.  A numerical nonfinite is retained and labeled.

## Maximum conclusion

P02 may report:

- the exact constructive/no-witness census in this 11,520-stratum universe;
- observed local curvature and rank structures on constructed witnesses;
- exact algebraic incompatibilities encoded by static column/component count;
- which special causal or repeated-tidal strata have explicit local witnesses;
  and
- descriptive adjacency/correlation across the registered axes.

P02 may not infer a selected extension, global realization, background
equation, physical time evolution, action, source, carrier, boundary law,
bootstrap, density, `Xmax`, mass, physical scale, prediction, or completeness
of the infinite-dimensional metric configuration space.

