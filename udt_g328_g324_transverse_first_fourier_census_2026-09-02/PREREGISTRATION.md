# G328 preregistration — primitive transverse Fourier census

Date: 2026-09-02
State: frozen before production outcome

## 1. Background and unrestricted perturbation in the bounded tile

Use the G324 proper-time metric in fixed quotient coordinates,

\[
g_0=-dT^2+C_1^2T^{-2/3}dX^2+C_\perp^2T^{4/3}(dy^2+dz^2),
\qquad T>0.
\]

Let `L_y` be the registered period of the chosen transverse circle and

\[
k_y=\frac{2\pi}{L_y}>0.
\]

Begin with the full complex shorthand

\[
\delta g_{ab}=h_{ab}(T)e^{ik_y y},\qquad h_{ab}=h_{ba},
\]

with all ten functions independent before solving. Its real and imaginary parts are the cosine and
sine sectors. Linearize only

\[
S_{ab}:=R_{ab}-\frac14R g_{ab}=0.
\]

The legal gauge generators are all smooth periodic vectors
`xi^a(T) exp(i k_y y)` in the same eigenspace. No gauge condition, physical polarization count, or
time basis is assumed as a scientific result.

## 2. Required production classification

The production route must:

1. derive all ten components of `delta S_ab` directly from the metric perturbation;
2. verify the linearized Bianchi consequence for this nonzero Fourier covector and determine
   whether `delta R` must vanish on shell;
3. derive the complete same-mode Lie-derivative image of four arbitrary periodic gauge functions;
4. split the system into invariant parity blocks under `z -> -z`, or give an exact alternative
   block decomposition;
5. construct a gauge fixing or a complete set of gauge invariants valid on every compact interval
   `I` contained in `(0,infinity)`, and prove that it loses no solutions;
6. solve every constraint and evolution equation in each block, including exceptional or repeated
   branches;
7. determine the exact dimension of the physical solution space after quotient by gauge, and then
   double the complex-phase count correctly to obtain the real cosine/sine count;
8. exhibit a nonzero gauge-invariant curvature response for every claimed physical family;
9. reconstruct a representative full metric perturbation for every physical solution and verify
   all ten field-equation components exactly;
10. classify the independent time branches near `T -> 0+` and `T -> infinity` without imposing an
    endpoint acceptance condition;
11. state whether any result is special to the primitive harmonic or extends algebraically to
    arbitrary nonzero transverse wavenumber;
12. refuse promotion to full Fourier or nonlinear stability.

## 3. Predeclared classification outcomes

If the quotient system closes with exactly two second-order physical mode families per complex
phase, use:

```text
PRIMITIVE_TRANSVERSE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE
__TWO_PHYSICAL_MODE_FAMILIES__EXACT_BRANCH_CLASSIFICATION
__NO_FULL_STABILITY_CLAIM
```

If it closes with a different finite physical dimension, use:

```text
PRIMITIVE_TRANSVERSE_FOURIER_SECTOR_CLOSES_WITH_UNEXPECTED_PHYSICAL_DIMENSION
__EXACT_BRANCH_CLASSIFICATION__NO_FULL_STABILITY_CLAIM
```

If an undetermined non-gauge function, inconsistent constraint, unresolved rank change, or
unclassified exceptional branch remains, use:

```text
G328_PRIMITIVE_TRANSVERSE_FOURIER_CENSUS_OPEN
```

If the exact equations contradict the proposed bounded field equation or the registered
background, use:

```text
G328_TRANSVERSE_LINEARIZATION_INCONSISTENT_WITH_REGISTERED_BACKGROUND
```

## 4. Falsifiers and hostile controls

The positive classification is falsified by any of the following:

- a dropped metric component or field-equation component changes the quotient solution space;
- a claimed physical mode is a periodic Lie derivative;
- a claimed gauge choice fails for regular data on a compact positive-time interval;
- `delta R` is set to zero without the nonzero-mode Bianchi argument or direct constraint;
- a reconstructed representative leaves a nonzero exact residual;
- a time basis has a vanishing Wronskian or omits a repeated/logarithmic branch;
- the real phase and integration-constant count is wrong;
- a claimed physical family has no nonzero local curvature witness;
- endpoint behavior is used to discard a solution;
- the result requires an imported action, source, matter model, observation, fitted profile,
  selected scale/history/topology/population, or physical `X_max`.

Hostile tests must at minimum reject: an omitted lapse/shift equation, a nonperiodic affine gauge
generator, a deliberately altered gradient power, a fake zero-scalar assertion at `k_y=0`, a
discarded singular/logarithmic branch, an incorrect real-dimension count, and a reconstruction with
one sign-flipped component.

## 5. Certification contract

- The production and independent routes may share this frozen background and question, but no
  implementation or generated result.
- The production route may use an exact first-variation engine; the independent route must use a
  distinct derivation, such as ADM constraints/evolution plus invariant reconstruction or an exact
  epsilon-dependent metric route.
- Exact symbolic identities are load-bearing. Numerical samples may diagnose but cannot certify
  zero residuals or rank.
- The independent route must verify the full reconstructed ten-component residual, not only a
  reduced master equation.
- Run hostile controls, the exact current-premise verifier, and repository regressions before
  banking.
- Require a fresh sealed adversarial review before an externally accepted grade.

## 6. Completeness boundary

This is the full primitive `y`-directed nonzero Fourier eigenspace at first order on a fixed G324
quotient. It excludes the zero mode already handled by G325/G326, the axial tensor tile of G327,
oblique covectors, higher or simultaneous harmonics, nonlinear coupling, endpoint-uniform control,
other backgrounds and topologies, physical occupancy, observations, sources/matter/mass, scale,
history selection, and physical `X_max`.
