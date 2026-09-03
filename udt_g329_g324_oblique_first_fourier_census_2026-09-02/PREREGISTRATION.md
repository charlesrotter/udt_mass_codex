# G329 preregistration — first genuinely oblique Fourier census

Date: 2026-09-02
State: frozen before production outcome

## 1. Background and complete bounded perturbation

Use the G324 proper-time metric in fixed quotient coordinates,

\[
g_0=-dT^2+C_1^2T^{-2/3}dX^2+C_\perp^2T^{4/3}(dy^2+dz^2),
\qquad T>0.
\]

Let `L_X,L_y` be registered periods and choose the primitive oblique lattice covector

\[
q=k_XdX+k_y dy,
\qquad
k_X=2\pi/L_X>0,
\qquad
k_y=2\pi/L_y>0.
\]

Begin with

\[
\delta g_{ab}=h_{ab}(T)e^{i(k_XX+k_yy)},
\qquad h_{ab}=h_{ba},
\]

with all ten functions independent. Linearize only

\[
S_{ab}:=R_{ab}-\frac14R g_{ab}=0.
\]

All four smooth same-mode periodic vectors are legal infinitesimal gauges. No synchronous gauge,
TT condition, polarization count, decoupling, special-function basis, or endpoint condition is
assumed as a scientific result.

## 2. Required production classification

Production must:

1. derive all ten components of `delta S_ab` directly from the unrestricted perturbation;
2. verify the complete linearized Bianchi identity and determine exactly when nonzero `q` forces
   `delta R=0`;
3. derive the complete Lie image of four arbitrary same-mode periodic gauge functions;
4. use the exact `z -> -z` parity split, or prove an alternative complete block decomposition;
5. establish a gauge fixing or gauge-invariant quotient valid on every compact interval inside
   `T>0`, including every rank and exceptional-component case;
6. solve every constraint and reduce the physical quotient to a minimal exact ODE system without
   presuming the two polarizations decouple;
7. prove the exact physical solution-space dimension and the real cosine/sine count;
8. construct a representative full perturbation for every physical solution and verify every
   field-equation component exactly;
9. give nonzero local gauge-invariant curvature witnesses separating each physical family from
   periodic Lie derivatives;
10. recover the G327 axial and G328 transverse systems under the corresponding component limits
    only as regression checks, never as inputs replacing the oblique derivation;
11. classify all controlled independent branches as `T -> 0+` and `T -> infinity`; if an endpoint
    asymptotic cannot be closed exactly, mark it open rather than fitting or discarding it;
12. state whether the algebra extends from `(1,1,0)` to arbitrary registered `k_X k_y != 0`;
13. refuse promotion to full Fourier or nonlinear stability.

## 3. Predeclared outcomes

If the quotient closes as two coupled physical second-order amplitudes per complex phase, with
complete compact-time reconstruction and controlled endpoint classification, use:

```text
PRIMITIVE_OBLIQUE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE
__TWO_COUPLED_PHYSICAL_AMPLITUDES__EXACT_COMPACT_TIME_CENSUS
__NO_FULL_STABILITY_CLAIM
```

If it closes with a different finite physical dimension, use:

```text
PRIMITIVE_OBLIQUE_FOURIER_SECTOR_CLOSES_WITH_UNEXPECTED_PHYSICAL_DIMENSION
__EXACT_COMPACT_TIME_CENSUS__NO_FULL_STABILITY_CLAIM
```

If exact compact-time closure succeeds but one or both endpoint asymptotic classifications remain
unresolved, append:

```text
__ENDPOINT_ASYMPTOTICS_PARTIALLY_OPEN
```

If an undetermined non-gauge function, inconsistent constraint, unresolved rank change, incomplete
representative reconstruction, or unclassified exceptional branch remains, use:

```text
G329_PRIMITIVE_OBLIQUE_FOURIER_CENSUS_OPEN
```

If the exact equations contradict the registered background or bounded field equation, use:

```text
G329_OBLIQUE_LINEARIZATION_INCONSISTENT_WITH_REGISTERED_BACKGROUND
```

## 4. Falsifiers and hostile controls

The positive classification is falsified by any of the following:

- a dropped metric or field-equation component changes the quotient;
- a claimed physical amplitude is a periodic Lie derivative;
- a gauge choice fails for regular data on a compact positive-time interval;
- an instantaneous rotation of the physical wave direction silently drops its time derivative;
- either `k_X` or `k_y` is set to zero during the oblique derivation;
- `delta R` is removed without a valid nonzero-mode Bianchi argument;
- the reduced system loses a constraint, exceptional branch, or one physical polarization;
- a reconstructed representative has any nonzero exact residual;
- a claimed endpoint basis has zero Wronskian or filters a singular/logarithmic branch;
- the real phase or integration-constant count is wrong;
- a claimed physical family has no nonzero local curvature witness;
- the result imports an action, source, matter model, observation, fit, distance/scale, selected
  history/topology/population, or physical `X_max`.

Hostile tests must at minimum reject an omitted lapse/shift equation, one zeroed oblique component,
a nonperiodic affine gauge, a frozen instantaneous propagation angle, a false decoupled-polarization
claim, a fake `delta R=0` statement at the zero mode, a discarded endpoint branch, an incorrect real
dimension, and a sign-flipped reconstruction.

## 5. Certification contract

- Production and verification may share only this frozen question, background, and registered
  premises; they may not share implementation or generated results.
- Production may use direct four-dimensional first variation. Verification must use an
  implementation-distinct route such as ADM/Gauss--Codazzi plus a separate quotient, or exact
  epsilon-dependent metric differentiation.
- Exact symbolic identities carry algebraic zero, constraint rank, and reconstruction claims.
- If the reduced ODE lacks elementary closed forms, certify its coefficient matrix, regular
  compact-time initial-value map, dimension, limits, and controlled asymptotics instead of fitting.
- Independently verify every load-bearing curvature witness and hostile catch.
- Run the exact current-premise verifier and repository regressions before banking.
- Require a fresh sealed adversarial review before an externally accepted grade.

## 6. Completeness boundary

This is the primitive `(1,1,0)` oblique nonzero Fourier eigenspace at first order on a fixed G324
quotient. It excludes other integer pairs and signs beyond the real conjugate representation,
simultaneous harmonics, nonlinear coupling, endpoint-uniform stability, other backgrounds and
topologies, physical occupancy, observations, source/matter/mass, scale, history selection,
singularity avoidance, and physical `X_max`.
