# Preregistration — one-relation reciprocal/orchestra regime flow

Date: 2026-08-12
Mode: `MAP -> DERIVE`, metric-led, exact symbolic/CPU
Outcome status at registration: **NOT YET EVALUATED**

## 1. Whole question

For one supplied regular A-calibrated observer-pair relation, the complete pair-first theorem gives

```text
h = h_base + P,
h_base = B^T eta B,
P = C^T q C >= 0,
```

where `B` carries the common-scale, reciprocal-depth, and shift channels and `P` is the complete
angular/mixing/embedding Gram contribution. The terminal reciprocal-`c_E` theorem reads one
`phi_pair` only after this complete `h` has been formed.

The bounded question is whether reciprocal normalization itself supplies an exact regime-response
kernel in which a generic two-sided orchestra contribution is least influential at an intermediate
reciprocal depth and amplified toward both reciprocal extremes.

This is **not** a ranking of the G75/G88 AM lapse-profile family. In this package, `A/M` means the
angular/mixing orchestra. The G88 stationary AM lapse continuation is outside the calculation.

## 2. Exact bounded regime

- one supplied smooth regular A-calibrated pair relation;
- one regular local pair-first `2+2` chart;
- complete zero-order pair metric `h=B^T eta B+P` with no Gram entry removed;
- arbitrary common scale `kappa`, reciprocal depth `phi`, base shift `beta`, and symmetric
  `P=[[a,d],[d,e]]>=0`;
- generic curve parameter `lambda`, not predeclared as time, distance, redshift, or physical scale;
- exact first derivative along `lambda`, retaining `B(lambda)` and `P(lambda)`;
- exact partial reciprocal response at fixed `(P,kappa,beta)` only as a diagnostic decomposition of
  the full derivative, not as a physical frozen-sector trajectory.

No SNe, CMB, `X_max`, microphysics, action, source, matter carrier, bootstrap law, GR equation,
profile fit, boundary condition, or numerical scale enters.

## 3. Objects to derive

Define the dimensionless calibration-relative orchestra-loading operator

```text
Pi = B^(-T) P B^(-1).
```

The production derivation must establish or falsify:

1. `Pi>=0` and `h=B^T(eta+Pi)B` exactly.
2. With

   ```text
   B=[[T,T beta],[0,L]],
   T=sigma exp(-phi),
   L=sigma exp(+phi),
   n_beta=e-2 beta d+beta^2 a,
   m_beta=d-beta a,
   ```

   the exact components are

   ```text
   Pi00 = a exp(+2phi)/sigma^2,
   Pi01 = m_beta/sigma^2,
   Pi11 = n_beta exp(-2phi)/sigma^2.
   ```

3. `det(Pi)=det(P)/sigma^4` is independent of `phi` under the declared partial response.
4. The compact A-calibrated loading diagnostic

   ```text
   A_load=tr(Pi)
         =[a exp(+2phi)+n_beta exp(-2phi)]/sigma^2
   ```

   has

   ```text
   partial_phi A_load = 2(Pi00-Pi11),
   partial_phi^2 A_load = 4 A_load.
   ```

   For positive-definite `P`, it must have one strict minimum at

   ```text
   phi_star=(1/4)log(n_beta/a),
   A_min=2 sqrt(a n_beta)/sigma^2.
   ```

   Rank-deficient and aligned boundaries must be retained and classified rather than rejected.
5. The exact terminal reciprocal response must be expressed through

   ```text
   x=Pi00, y=Pi11, z=Pi01,
   T_pair^2/T^2=1-x,
   L_pair^2/L^2=1+y+z^2/(1-x),
   phi_pair-phi
     =(1/4)log{[(1-x)(1+y)+z^2]/(1-x)^2}
   ```

   on the A-clock stratum `x<1`.
6. Along an arbitrary live relation, with `Gamma=(dB/dlambda)B^-1`,

   ```text
   dPi/dlambda
     =-Gamma^T Pi-Pi Gamma+B^-T(dP/dlambda)B^-1.
   ```

   This full equation must expose, not suppress, the independent evolution of the pair state and
   orchestra Gram matrix.

## 4. Falsification / certification contract

The proposed reciprocal-amplification kernel is falsified in this scope if any of the following
occurs:

- direct matrix multiplication disagrees with the registered component formulas;
- `Pi` is not positive semidefinite whenever `P` is;
- the determinant retains a nonzero `phi` dependence under the declared partial response;
- strict convexity or the stated minimum fails for a positive-definite rational witness;
- the terminal `(T_pair,L_pair,phi_pair)` formula disagrees with direct decomposition of `h`;
- the live derivative disagrees with direct symbolic differentiation;
- an independent implementation fails the frozen rational witness census;
- hostile mutations of a reciprocal exponent, shift completion, cross term, or derivative sign are
  not caught.

Certification gates:

- exact SymPy identities, no floating-point proof;
- independent stdlib `Fraction`/high-precision finite-difference route using no production code;
- positive-definite, rank-one, zero, nonzero-shift, and nonzero-cross-term witnesses;
- package verifier and repository tests before any banked verdict.

## 5. Preregistered landings

The result must land in exactly one primary class:

1. `DERIVED_CONDITIONAL_RECIPROCAL_TWO_SIDED_AMPLIFICATION_KERNEL` — the full-rank partial-response
   theorem and live evolution identity both pass.
2. `BOUNDARY_ONLY_OR_ONE_SIDED_AMPLIFICATION` — the theorem survives only on lower-rank/aligned
   strata.
3. `NO_RECIPROCAL_AMPLIFICATION_KERNEL` — one or more load-bearing exact identities fail.
4. `TYPE_FAILURE` — the proposed loading object is not well-defined in the declared A calibration.

Even landing 1 may conclude only that reciprocal normalization supplies a **conditional response
kernel**. It may not claim that the physical UDT history has a quiet middle, that SNe/CMB/microphysics
are explained, or that a physical sector-weighting/evolution law has been derived. The full
`lambda` equation decides whether the current metric identities determine the actual curve or leave
`dP/dlambda` and `dB/dlambda` as supplied history data.
