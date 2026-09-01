# G320 map — G319 physical-initial-geometry quotient audit

Date: 2026-09-01
Question type: `METRIC_LED__OBSERVING_NOT_TARGETING`

## Whole bounded question

G319 proves that every smooth positive periodic `psi(x)` can be completed to regular sign-definite
constraint data in its registered flat marked-`T^3`, one-coordinate, diagonal-TT, `B!=0` slice after
a sufficiently large free `J0` is supplied. G320 asks what that breadth means:

```text
Are some distinct psi profiles genuinely different physical initial data (gamma,K),
or are they only spatial-coordinate or conformal-seed rewritings of the same data?
```

The comparison is made only after reconstructing the physical spatial metric
`gamma_ij=psi^4 delta_ij` and physical extrinsic curvature `K^i_j`. Conformal seeds and coordinate
labels are not themselves observables.

## Quotient before comparison

The audit must identify as representation-equivalent:

1. spatial diffeomorphisms carrying the complete pair `(gamma,K)`;
2. phase translations, reflections, and lawful marked-torus isometries as explicit controls;
3. conformal-method seed changes that reconstruct exactly the same physical `(gamma,K)`;
4. auxiliary-vector translation kernels that leave the reconstructed tensor unchanged.

Only diffeomorphism-invariant scalars, their ranges/distributions, or invariant integrals may
separate physical data. A difference between raw `psi` arrays is never evidence.

## Registered physical discriminators

For the intrinsic metric on the dimensionless marked torus,

```text
gamma_ij = psi(x)^4 delta_ij,
R3 = -8 psi^-5 psi''.
```

The primary separator is the scale-free diffeomorphism invariant

```text
Q_R = (integral R3 dmu_gamma) / Vol(gamma)^(1/3).
```

Auxiliary physical checks use invariant contractions and integrals built from `K`, including
`tr(K)`, `tr(K^2)`, and `tr(K^3)`. They characterize the reconstructed data but are not needed to
force a distinction if `Q_R` already separates the intrinsic metrics.

## Chosen controls, not physical pins

The preregistered analytic family is

```text
psi_n(x) = p + a cos(n x),  p=3/2, a=1/5, n in {1,2,3,4},
d=0, Lambda=0, J0=100, epsilon in {-1,+1}.
```

All numbers are `CHOSE_CATEGORY_A_DIAGNOSTIC_CONTROLS`. They are not observations, laws, a scale,
or selected initial data. Integer modes have the same value distribution and volume, while their
derivatives differ; this makes them a hostile test of coordinate-label reasoning rather than a fit.

## Maximum scope

G320 may establish that the G319 family contains genuine physical initial-geometry directions, or
that the registered controls fail to separate after quotient. It may not claim a complete moduli
classification of all `psi`, choose Nature's data, select a history, infer stability, or change the
metric/kernel. Nonflat seeds, multidimensional profiles, `B=0` crossings, evolution, matter,
observations, physical topology, scale, and `X_max` remain outside this tile.
