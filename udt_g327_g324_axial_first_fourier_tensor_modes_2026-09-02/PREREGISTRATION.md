# G327 preregistration — primitive axial Fourier tensor modes

Date: 2026-09-02
State: frozen before production outcome

## 1. Exact background and declared sector

Use the proper-time G324 metric in fixed quotient coordinates,

\[
g_0=-dT^2+C_1^2T^{-2/3}dX^2+C_\perp^2T^{4/3}(dy^2+dz^2),
\qquad T>0,
\]

where the compact axial coordinate has the G323 primitive period `L_X`. Define

\[
k_1=\frac{2\pi}{L_X},\qquad \nu=\frac{|k_1|}{C_1}>0.
\]

The first real axial eigenspace is spanned by `cos(k_1 X)` and `sin(k_1 X)`. For either phase,
write the complete transverse-tracefree perturbation as

\[
\delta g_{AB}=2C_\perp^2T^{4/3}H_{AB}(T)e(X),
\qquad A,B\in\{y,z\},\qquad H^A{}_A=0,
\]

with the plus and cross entries of the symmetric matrix `H_AB` both free. All other perturbation
components vanish in this declared tensor sector. Linearize only the already active bounded law

\[
R_{ab}-\frac14R g_{ab}=0.
\]

No endpoint condition, amplitude, wavelength, scalar-curvature variation, or preferred solution is
inserted.

## 2. Positive-classification obligations

The positive landing requires all of the following:

1. directly linearize every spacetime component of Ricci and the scalar from the metric ansatz;
2. prove the sector closes: lapse, shift, scalar, vector, and constraint residuals vanish rather
   than being silently omitted;
3. prove periodic infinitesimal diffeomorphisms cannot generate the transverse-tracefree tensor;
4. derive, for each polarization and phase, the same exact equation

   \[
   \ddot H+\frac1T\dot H+\nu^2T^{2/3}H=0;
   \]

5. with `z=3 nu T^(4/3)/4`, verify that the full time basis is `J_0(z),Y_0(z)` and that its
   Wronskian is nonzero;
6. count the real solution space: two polarizations times two real phases times two time constants;
7. exhibit a nonzero local transverse-tracefree curvature response, so the modes are not lattice
   moduli or zero metric images;
8. define the diagnostic compact-time norm

   \[
   \|H\|_{I,1}=\sup_{T\in I}
   \left(\|H(T)\|_F+\frac{\|\dot H(T)\|_F}{\nu T^{1/3}}\right),
   \qquad I=[T_-,T_+]\Subset(0,\infty),
   \]

   and prove it is finite for all declared solutions on every such interval;
9. classify, without filtering, the two endpoint behaviors: one finite past branch and one
   logarithmic past branch per polarization/phase, while both oscillatory branches decay in this
   relative phase-space norm as `T^(-2/3)` toward the expanding end;
10. refuse promotion to the full Fourier spectrum or any stability theorem.

## 3. Preregistered landings

If all obligations pass, use:

```text
PRIMITIVE_AXIAL_TENSOR_MODE_CLOSES_AS_TWO_GAUGE_INVARIANT_POLARIZATIONS
__BESSEL_ZERO_TIME_BASIS__FINITE_AND_LOGARITHMIC_PAST_BRANCHES
__OSCILLATORY_T_MINUS_TWO_THIRDS_FUTURE_DECAY__NO_FULL_STABILITY_CLAIM
```

If the tensor ansatz sources another perturbation component or constraint, use:

```text
G327_AXIAL_TENSOR_SECTOR_DOES_NOT_CLOSE
```

If the sector closes but the proposed ODE, solution basis, gauge classification, dimension, or
endpoint behavior fails, use:

```text
G327_PRIMITIVE_AXIAL_TENSOR_CLASSIFICATION_REFUTED
```

If algebra closes but completeness or independent certification remains unresolved, use:

```text
G327_PRIMITIVE_AXIAL_TENSOR_CENSUS_OPEN
```

## 4. Falsifiers

- any raw linearized trace-free Ricci component outside the transverse-tracefree block is nonzero;
- `delta R` or the connected scalar mode is nonzero at this Fourier covector;
- a legal periodic gauge vector produces a nonzero transverse-tracefree `H_AB`;
- either Bessel basis element leaves a nonzero exact ODE residual;
- the basis Wronskian vanishes for positive `T`;
- the real parameter count is not eight;
- every local curvature component vanishes for a nonzero on-shell mode;
- the stated endpoint powers or norm behavior are false;
- the result requires an action, source, matter model, observation, fit, new scale, history,
  physical population, or `X_max`.

## 5. Certification contract

- Production and independent implementations may share only this written background and contract,
  not code or generated results.
- Exact symbolic residual coefficients are load-bearing; numerical near-zero samples are not.
- The independent route must reconstruct the tensor equations from the metric rather than import
  the production ODE.
- Hostile controls must reject at least: a wrong gradient power, a missing Hubble-damping term, a
  fake gauge origin, a discarded logarithmic branch, a wrong real dimension, and a false future
  endpoint power.
- Run the repository premise verifier and purity suite before banking.
- Require fresh sealed adversarial review before an externally accepted grade.

## 6. Completeness boundary

This is the full primitive axial transverse-tracefree tensor eigenspace and no more. It drops the
scalar/vector sectors, lapse/shift outside this invariant block, modes directed along `y` or `z`,
oblique modes, higher Fourier harmonics, nonlinear coupling, endpoint-uniform control of the full
system, other backgrounds/topologies, and every physical selection question.

