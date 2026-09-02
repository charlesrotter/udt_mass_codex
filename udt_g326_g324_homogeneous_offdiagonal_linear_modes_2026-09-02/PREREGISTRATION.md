# G326 preregistration — homogeneous off-diagonal linear mode census

Date: 2026-09-02
State: frozen before production outcome

## 1. Exact background and complete bounded sector

Use proper time `T>0` and fixed compact quotient coordinates:

\[
g_0=-dT^2+\sum_{i=1}^3 C_i^2T^{2p_i}(dx^i)^2,
\qquad p=(-1/3,2/3,2/3).
\]

Write the complete homogeneous off-diagonal synchronous first variation as

\[
g_{ij}=\epsilon k_{ij}(T)+O(\epsilon^2),\qquad i<j,
\]

with all three functions `k_12`, `k_13`, and `k_23` free. Linearize

\[
R_{ab}-\frac14R g_{ab}=0
\]

without inserting diagonal perturbations, endpoint data, or a scalar value.

## 2. Proof obligations

The positive classification requires all of the following:

1. derive the exact homogeneous matrix-metric Ricci tensor directly;
2. prove that the off-diagonal sector closes at first order and determine its scalar variation;
3. derive and solve all three second-order ODEs, proving the general solution;
4. treat the repeated transverse root without discarding its logarithmic solution;
5. enumerate every homogeneous synchronous residual gauge vector that descends to the fixed `T3`;
6. derive the image and kernel of constant linear cover-coordinate changes;
7. test those generators against quotient periodicity rather than calling them local gauge;
8. count independent quotient-lattice directions and reconcile the count with G325;
9. exhibit a direct local curvature component for every claimed physical off-diagonal mode;
10. state compact-time validity and refuse endpoint-uniform or full-stability promotion.

## 3. Preregistered landing

If exactly five off-diagonal solutions are locally pure cover-coordinate changes but non-gauge
fixed-quotient lattice modes, while the repeated-root logarithmic solution is one additional local
curvature-changing transverse Kasner shear and no scalar or quotient-legal gauge mode appears, use:

```text
HOMOGENEOUS_OFFDIAGONAL_MODES_CLOSE_AS_FIVE_QUOTIENT_LATTICE_MODULI
__ONE_LOCAL_TRANSVERSE_KASNER_SHEAR__NO_NEW_GAUGE_OR_SCALAR_MODE
__NO_FULL_STABILITY_CLAIM
```

If another independent solution survives, use:

```text
G326_EXTRA_HOMOGENEOUS_OFFDIAGONAL_MODE_SURVIVES
```

If any gauge, quotient, or curvature classification fails, use:

```text
G326_OFFDIAGONAL_MODE_CLASSIFICATION_REFUTED
```

If the equations are solved but completeness or independence is not certified, use:

```text
G326_HOMOGENEOUS_OFFDIAGONAL_CENSUS_OPEN
```

## 4. Falsifiers

- a proposed basis leaves a nonzero raw linearized trace-free Ricci residual;
- the repeated-root logarithmic solution is omitted or is actually quotient-legal gauge;
- one of the five alleged lattice modes has nonzero linearized local curvature;
- a nonzero constant linear generator is a single-valued vector field on the fixed torus;
- the alleged local shear has zero linearized curvature modulo the full legal residual gauge;
- the off-diagonal sector changes scalar curvature at first order;
- the combined G325/G326 parameter count double-counts a gauge or lattice direction;
- the conclusion requires a source, action, observation, scale, physical population, or `X_max`.

## 5. Certification contract

- Production and independent implementations may share only the written background and
  preregistration, never code or generated results.
- Exact symbolic coefficient residuals are load-bearing; sampled near-zero values are insufficient.
- Hostile controls must reject a dropped logarithmic mode, wrong ODE coefficient, falsely periodic
  cover generator, fake curvature-free log mode, and incorrect combined dimension.
- Run the repository premise verifier and full purity suite before banking.
- Require fresh sealed adversarial review before any accepted grade.

## 6. Completeness and maximum conclusion

This covers all three off-diagonal homogeneous synchronous spatial amplitudes on the registered
G324 background. It drops lapse/shift outside the chosen gauge, diagonal modes already classified
by G325, every nonzero Fourier mode, nonlinear coupling, endpoints, other quotients/topologies, and
all physical selection questions. At most it closes the full spatially homogeneous first-variation
census when combined with G325; it cannot establish full linear or nonlinear stability.
