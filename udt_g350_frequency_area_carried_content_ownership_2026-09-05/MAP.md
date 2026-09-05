# G350 map — frequency/area carried-content ownership

Date: 2026-09-05
Status: outcome-unseen preregistration

## Whole question

Starting only from G346--G349's metric-derived frequency ratios, finite sheet-area Jacobians,
observer covariance, reversal, and sewing, determine whether the metric uniquely fixes any
nonzero scalar carried-content or transfer law between supplied regular cuts of the same labelled
null-ray family.

This is `METRIC_LED` and observing rather than targeting. It does not ask the metric to reproduce
brightness, photon number, energy flux, luminosity, probability, or an observational distance.
It asks exactly which positive local multiplicative transfer factors the existing geometry permits,
and whether their weights or source values are selected.

## Exact bounded arena

- an arbitrary supplied smooth time-oriented four-dimensional Lorentzian metric;
- a supplied labelled regular future-null family and a common celestial source presentation;
- any ordered finite cuts `i,j,k` on the same labelled rays;
- the common screen-rank-two stratum where the metric two-Jacobians `J_i,J_j,J_k` are positive;
- positive measured endpoint frequencies `omega_i,omega_j,omega_k` from supplied finite timelike
  observers, with one common affine normalization along each ray;
- local transfer factors depending only on the two positive dimensionless ratios

  ```text
  R_ji = omega_j / omega_i,
  A_ji = J_j / J_i.
  ```

The candidate is required to be positive, continuous, local on each retained label, normalized at
identity, and multiplicative under exact cut sewing. Reversal is tested rather than separately
assumed. Candidate weights are free and explored.

The restriction to the two-ratio local class is `CHOSE_BOUNDED_CLASSIFICATION`, not a UDT premise.
Endpoint curvature invariants, nonlocal memory, additive or interacting transfer, polarization,
field phase, interference, source terms, and cross-label aggregation remain outside this first
classification and are used to test whether any apparent uniqueness survives enlargement.

## Pure and easy routes

- Pure route used here: solve the continuous character equation on the full positive ratio group,
  then construct explicit endpoint-coboundary and source-normalization counterfamilies and classify
  the zero-area boundary.
- Easier but insufficient route: choose inverse area or one power of redshift because it resembles
  familiar radiation. That would import the physical type of the carried quantity.
- Forbidden route: assume photon number, energy per quantum, arrival-rate loss, inverse-square flux,
  transparent propagation, Maxwell/QED, Etherington reciprocity, detector response, or luminosity.

The logarithm, continuous Cauchy equation, finite-dimensional linear algebra, and numerical identity
checks are category-A mathematical methods.

## Candidate structure

Write a local multiplier as

```text
C_j = T(R_ji,A_ji) C_i.
```

The geometry itself gives

```text
R_ki = R_kj R_ji,
A_ki = A_kj A_ji.
```

Test whether positivity, continuity, identity, and sewing force one transfer, only the identity, or
the full character family

```text
T_(p,q)(R,A) = R^p A^q.
```

Under independent endpoint-observer changes `omega_i -> D_i omega_i`, test whether covariance fixes
`p` or merely says that the undefined carried scalar must be assigned observer weight `p`.

If conservation of a scalar sheet measure is separately imposed, test whether it fixes `q=-1` and
whether that conservation statement is metric-derived or an additional radiative premise. Also
test whether any homogeneous multiplicative law can create nonzero content from zero source data.

## Singular and global branches

- At a caustic or null sheet `J=0`, the positive-ratio group no longer contains the point. Classify
  the limits for all area weights rather than deleting the ray or calling the spacetime singular.
- Keep every path label separate. No equality, sum, interference, or probability across labels is
  assumed.
- For a supplied source measure, a pushforward through the complete G349 map is a mathematical
  construction. Whether the source measure exists, is conserved, or how repeated images combine is
  not supplied by metric area alone.
- Permit arbitrary positive endpoint-local metric coboundaries as an explicit enlargement test.

## Maximum conclusion

At most G350 may classify the complete continuous positive local multiplicative transfer family on
the common regular two-ratio stratum, its observer typing, source-normalization freedom, and its
caustic/path-label limitations. It may determine whether G346--G349 select a unique transfer factor
or instead mark the precise boundary where a new carried-field or conservation premise is needed.

It may not derive nonzero emission, content, photon number, energy, amplitude, phase, intensity,
brightness, flux, luminosity, probability, detector response, absorption, cross-label aggregation,
observational distance, a metric history, occupancy, stability, matter/mass, scale, `X_max`, or
canon.
